from flask import Flask, render_template
from models import db, Recipe

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/onboarding")
def onboarding():
    return render_template("onboarding.html")

if __name__ == '__main__':
    app.run(debug=True)