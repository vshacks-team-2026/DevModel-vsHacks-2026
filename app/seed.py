from app import app
from models import db, Recipe

#test recipes
recipes = [
    Recipe(
        name="Banana Oatmeal",
        type="breakfast",
        cuisine="french",
        cost_range="cheap",
        ingredients=["oats", "banana", "milk", "honey"],
        allergens=["dairy", "gluten"],
        steps=[
            "Heat the milk in a saucepan",
            "Add the oats and cook until soft",
            "Top with banana and honey"
        ],
        image=None
    ),

    Recipe(
        name="Vegetable Omelet",
        type="breakfast",
        cuisine="french",
        cost_range="moderate",
        ingredients=["eggs", "bell pepper", "spinach", "cheese"],
        allergens=["eggs", "dairy"],
        steps=[
            "Whisk the eggs",
            "Cook the vegetables in a pan",
            "Add the eggs and cheese",
            "Cook until the omelet is firm"
        ],
        image=None
    ),

    Recipe(
        name="Vegetable Fried Rice",
        type="lunch",
        cuisine="chinese",
        cost_range="cheap",
        ingredients=["rice", "carrots", "peas", "soy sauce"],
        allergens=["soy"],
        steps=[
            "Cook the rice",
            "Fry the vegetables",
            "Add the rice and soy sauce",
            "Mix and cook for several minutes"
        ],
        image=None
    ),

    Recipe(
        name="Chicken Pasta",
        type="lunch",
        cuisine="italian",
        cost_range="moderate",
        ingredients=["pasta", "chicken", "tomato sauce", "parmesan"],
        allergens=["gluten", "dairy"],
        steps=[
            "Cook the pasta",
            "Cook the chicken in a pan",
            "Add the tomato sauce",
            "Combine with the pasta and parmesan"
        ],
        image=None
    ),

    Recipe(
        name="Peanut Noodles",
        type="dinner",
        cuisine="thai",
        cost_range="cheap",
        ingredients=["noodles", "peanut butter", "soy sauce", "vegetables"],
        allergens=["nuts", "soy", "gluten"],
        steps=[
            "Cook the noodles",
            "Mix peanut butter and soy sauce",
            "Cook the vegetables",
            "Combine everything together"
        ],
        image=None
    ),

    Recipe(
        name="Garlic Shrimp Rice",
        type="dinner",
        cuisine="mediterranean",
        cost_range="expensive",
        ingredients=["shrimp", "rice", "garlic", "olive oil", "lemon"],
        allergens=["shellfish"],
        steps=[
            "Cook the rice",
            "Heat olive oil and garlic",
            "Cook the shrimp until pink",
            "Serve the shrimp over rice with lemon"
        ],
        image=None
    )
]

#seed the database
with app.app_context():
    if Recipe.query.count() == 0:
        db.session.add_all(recipes)
        db.session.commit()