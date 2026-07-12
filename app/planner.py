import random

def budget_converter(budget):
    try:
        budget = int(budget)
    except (TypeError, ValueError):
        return None
    if budget < 100:
        return "cheap"
    elif budget < 200:
        return "moderate"
    return "expensive"

def filter_by_budget(recipes, cost_range):
    allowed_ranges = {
        "cheap": ["cheap"],
        "moderate": ["cheap", "moderate"],
        "expensive": ["cheap", "moderate", "expensive"],
    }
    budget_recipes = []
    for recipe in recipes:
        if recipe.cost_range in allowed_ranges[cost_range]:
            budget_recipes.append(recipe)

    return budget_recipes

def filter_by_cuisine(recipes, selected_cuisine):
    if not selected_cuisine:
        return recipes

    cuisine_recipes = []
    for recipe in recipes:
        if recipe.cuisine in selected_cuisine:
            cuisine_recipes.append(recipe)
    return cuisine_recipes

def filter_by_allergens(recipes, selected_allergens):
    if not selected_allergens:
        return recipes

    allergens_recipes = []
    for recipe in recipes:
        contain_allergens = any(allergen in selected_allergens for allergen in recipe.allergens)
        if not contain_allergens:
            allergens_recipes.append(recipe)
    return allergens_recipes

def apply_filters(recipes, budget, selected_cuisines, selected_allergens):
    converted_budget = budget_converter(budget)
    if converted_budget is None:
        return []
    budget_recipes = filter_by_budget(recipes, converted_budget)
    cuisine_recipes = filter_by_cuisine(budget_recipes, selected_cuisines)
    filtered_recipes = filter_by_allergens(cuisine_recipes, selected_allergens)
    return filtered_recipes

def group_by_type(recipes):
    grouped_recipes = {
        "breakfast": [],
        "lunch": [],
        "dinner": [],
    }
    for recipe in recipes:
        if recipe.type in ["breakfast", "lunch", "dinner"]:
            grouped_recipes[recipe.type].append(recipe)
    return grouped_recipes


def generate_day_plan(grouped_recipes):
    breakfast = random.choice(grouped_recipes["breakfast"]) if grouped_recipes["breakfast"] else None
    lunch = random.choice(grouped_recipes["lunch"]) if grouped_recipes["lunch"] else None
    dinner = random.choice(grouped_recipes["dinner"]) if grouped_recipes["dinner"] else None

    day_plan = {
        "breakfast": breakfast,
        "lunch": lunch,
        "dinner": dinner,
    }

    return day_plan

def generate_weekly_plan(grouped_recipes):
    weekly_plan = {
        "Monday": generate_day_plan(grouped_recipes),
        "Tuesday": generate_day_plan(grouped_recipes),
        "Wednesday": generate_day_plan(grouped_recipes),
        "Thursday": generate_day_plan(grouped_recipes),
        "Friday": generate_day_plan(grouped_recipes),
        "Saturday": generate_day_plan(grouped_recipes),
        "Sunday": generate_day_plan(grouped_recipes),
    }
    return weekly_plan


if __name__ == "__main__":
    from app import app
    from models import db, Recipe

    with app.app_context():
        recipes = Recipe.query.all()

        grouped_recipes = group_by_type(recipes)

        weekly_plan = {
            "Monday": generate_day_plan(grouped_recipes),
            "Tuesday": generate_day_plan(grouped_recipes),
            "Wednesday": generate_day_plan(grouped_recipes),
            "Thursday": generate_day_plan(grouped_recipes),
            "Friday": generate_day_plan(grouped_recipes),
            "Saturday": generate_day_plan(grouped_recipes),
            "Sunday": generate_day_plan(grouped_recipes),
        }

        for day, meals in weekly_plan.items():
            print(day)

            for meal_type, recipe in meals.items():
                print(f"  {meal_type}: {recipe.name if recipe else 'No recipe'}")
