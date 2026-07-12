from flask import Flask, render_template, request
from models import db, Recipe
from planner import create_plan

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

#home page route
@app.route("/")
def home():
    return render_template("index.html")

#onboarding route
@app.route("/onboarding")
def onboarding():
    return render_template("onboarding.html")

@app.route("/plan", methods=["POST"])
def plan():
    if request.method == "POST":
        cuisines = request.form.getlist("cuisine")
        cost_range = request.form.get("cost_range")
        allergens = request.form.getlist("allergens")
        cuisines = [cuisine.lower() for cuisine in cuisines]
        allergens = [allergen.lower() for allergen in allergens]

        recipes = Recipe.query.all()

        weekly_plan = create_plan(recipes,
                                  cost_range,
                                  cuisines,
                                  allergens
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