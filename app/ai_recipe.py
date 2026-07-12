from typing import Literal
from pydantic import BaseModel, Field
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor

class GeneratedRecipe(BaseModel):
    name: str
    type: Literal["breakfast", "lunch", "dinner"]
    cuisine: Literal["italian",
        "mexican",
        "chinese",
        "thai",
        "indian",
        "french",
    ]
    cost_range: Literal["cheap", "moderate", "expensive"]
    ingredients: list[str]
    allergens: list[
        Literal["dairy", "gluten", "shellfish", "eggs", "nuts", "soy"]
    ]
    steps: list[str]

#generation model
class GeneratedMealBatch(BaseModel):
    recipes: list[GeneratedRecipe] = Field(
        min_length=3,
        max_length=3,
    )

def generate_recipe(
    meal_type: str,
    cuisines: list[str],
    budget: str,
    excluded_allergens: list[str],
) -> GeneratedRecipe:
    client = OpenAI()
    cuisine_text = ", ".join(cuisines) if cuisines else "any allowed cuisine"
    allergen_text = (
        ", ".join(excluded_allergens)
        if excluded_allergens
        else "none"
    )
    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Generate one simple, dorm-friendly recipe. "
                    "Follow every requested restriction exactly."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Meal type: {meal_type}\n"
                    f"Allowed cuisines: {cuisine_text}\n"
                    f"Budget category: {budget}\n"
                    f"Excluded allergens: {allergen_text}\n"
                    "Do not use any excluded allergen."
                ),
            },
        ],
        text_format=GeneratedRecipe,
    )

    if response.output_parsed is None:
        raise ValueError("The AI did not return a valid recipe.")

    return response.output_parsed

#check to validate the recipe
def validate_recipe(
    recipe: GeneratedRecipe,
    meal_type: str,
    cuisines: list[str],
    budget: str,
    excluded_allergens: list[str],
) -> bool:

    if recipe.type != meal_type:
        return False
    if cuisines and recipe.cuisine not in cuisines:
        return False
    if recipe.cost_range != budget:
        return False
    if set(recipe.allergens) & set(excluded_allergens):
        return False

    return True

#generates 3 meals for all meal types
def generate_meal_group(
    meal_type: str,
    cuisines: list[str],
    budget: str,
    excluded_allergens: list[str],
) -> list[GeneratedRecipe]:
    client = OpenAI()

    cuisine_text = ", ".join(cuisines) if cuisines else "any allowed cuisine"

    allergen_text = (
        ", ".join(excluded_allergens)
        if excluded_allergens
        else "none"
    )

    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": (
                        "Generate simple, realistic, dorm-friendly recipes. "
                        "Each recipe must have exactly 4 ingredients and 3 short steps. "
                        "Keep every ingredient and step concise. "
                        "Follow every requested restriction exactly."
                    ),
            },
            {
                "role": "user",
                "content": (
                        f"Generate exactly 3 {meal_type} recipes.\n"
                        f"Allowed cuisines: {cuisine_text}\n"
                        f"Budget category: {budget}\n"
                        f"Excluded allergens: {allergen_text}\n\n"
                        "Do not include excluded allergens. "
                        "Avoid duplicate or nearly identical recipes."
                    ),
            },
        ],
        text_format=GeneratedMealBatch,
    )

    recipes = response.output_parsed.recipes

    for recipe in recipes:
        if not validate_recipe(
                recipe,
                meal_type,
                cuisines,
                budget,
                excluded_allergens,
        ):
            raise ValueError("AI returned a recipe that failed validation.")

    return recipes

#each meal type runs in separate thread
def generate_recipe_batch(
    cuisines: list[str],
    budget: str,
    excluded_allergens: list[str],
) -> list[GeneratedRecipe]:

    mean_types = ['breakfast', 'lunch', 'dinner']

    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = [
            ex.submit(
                generate_meal_group,
                meal_type,
                cuisines,
                budget,
                excluded_allergens,
            ) for meal_type in mean_types
        ]

        recipes = []

        for future in futures:
            recipes.extend(future.result())

        return recipes