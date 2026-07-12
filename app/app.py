from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Recipe,User, FavoriteRecipe
from planner import create_plan, budget_converter
from ai_recipe import generate_recipe_batch
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-secret-key")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

#home page route
@app.route("/")
def home():
    return render_template("index.html")

#onboarding route
@app.route("/onboarding")
def onboarding():
    return render_template("onboarding.html")

#signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if User.query.filter_by(email=email).first():
            return render_template("signup.html", error="An account with this email already exists.")

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for("home"))

    return render_template("signup.html")

#login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        print("Submitted email:", repr(email))
        print("Stored emails:", [u.email for u in User.query.all()])
        print("User found:", user is not None)

        if user:
            print("Password valid:", user.check_password(password))
        if user is None or not user.check_password(password):
            return render_template(
                "login.html",
                error="Incorrect email or password."
            )
        login_user(user)
        return redirect(url_for("home"))

    return render_template("login.html")

#logout route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

#profile route
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

#favorite route
@app.route("/favorites")
@login_required
def favorites():
    saved_recipes = FavoriteRecipe.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "favorites.html",
        favorites=saved_recipes
    )

#added to favorites route
@app.route("/favorites/add", methods=["POST"])
@login_required
def add_favorite():
    data = request.get_json()
    existing = FavoriteRecipe.query.filter_by(
        user_id=current_user.id,
        name=data["name"]
    ).first()
    if existing:
        return jsonify({"status": "duplicate"})

    favorite = FavoriteRecipe(
        user_id=current_user.id,
        name=data["name"],
        type=data["type"],
        cuisine=data["cuisine"],
        cost_range=data["cost_range"],
        ingredients=data["ingredients"],
        allergens=data.get("allergens", []),
        steps=data["steps"]
    )

    db.session.add(favorite)
    db.session.commit()

    return jsonify({"status": "saved", "id": favorite.id})

#remove favorites
@app.route("/favorites/<int:favorite_id>/remove", methods=["POST"])
@login_required
def remove_favorite(favorite_id):
    favorite = FavoriteRecipe.query.filter_by(
        id=favorite_id,
        user_id=current_user.id
    ).first_or_404()
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"status": "removed"})

#plan route
@app.route("/plan", methods=["POST"])
def plan():
    if request.method == "POST":
        cuisines = request.form.getlist("cuisine")
        cost_range = request.form.get("cost_range")
        allergens = request.form.getlist("allergens")
        cuisines = [cuisine.lower() for cuisine in cuisines]
        allergens = [allergen.lower() for allergen in allergens]

        budget_range = budget_converter(cost_range)
        try:
            recipes = generate_recipe_batch(cuisines, budget_range, allergens)
            plan_source = 'AI'
        except Exception as e:
            print(f"AI failed: {e}")
            recipes = Recipe.query.all()
            plan_source = 'fallback'
        print("Plan source: ", plan_source)

        weekly_plan = create_plan(
            recipes,
            cost_range,
            cuisines,
            allergens,
        )

        week_plan = []
        for day, recipe in weekly_plan.items():
            week_plan.append({
                "name": day.lower(),
                "breakfast": recipe["breakfast"],
                "lunch": recipe["lunch"],
                "dinner": recipe["dinner"]
            })


    return render_template("plan.html", week_plan=week_plan)

if __name__ == '__main__':
    app.run(debug=True)