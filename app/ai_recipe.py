from typing import Literal
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()
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

def generate_recipe(
    meal_type: str,
    cuisines: list[str],
    budget: str,
    excluded_allergens: list[str],
) -> GeneratedRecipe:
    cuisine_text = ", ".join(cuisines) if cuisines else "any allowed cuisine"
    allergen_text = (
        ", ".join(excluded_allergens)
        if excluded_allergens
        else "none"
    )
    response = client.responses.parse(
        model="gpt-5-mini",
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