from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#recipe model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    cuisine = db.Column(db.String(100), nullable=False)
    cost_range = db.Column(db.String(20), nullable=False)
    ingredients = db.Column(db.JSON, nullable=False)
    allergens = db.Column(db.JSON, nullable=False)
    steps = db.Column(db.JSON, nullable=False)
    image = db.Column(db.String(100), nullable=True)


