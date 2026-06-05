import streamlit as st
import json
from ibm_watsonx_ai.foundation_models import ModelInference

# Page Config (must be first Streamlit command)
st.set_page_config(
    page_title="Smart Recipe Preparation Agent",
    page_icon="🍳",
    layout="wide"
)

API_KEY = "V6wH0hjHkZZ5KscEZGxT1b78zm_GUy8aJpNsYUhYYCUA"
PROJECT_ID = "36a8681f-76fb-46d7-a1a7-b2e443717295"

credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": API_KEY
}

# Load Recipes
with open("recipes.json", "r") as f:
    recipes = json.load(f)

def generate_ai_recipe(ingredients):

    model = ModelInference(
        model_id="meta-llama/llama-3-3-70b-instruct",
        credentials=credentials,
        project_id=PROJECT_ID
    )

    prompt = f"""
    Create a recipe using:

    {ingredients}

    Give:
    1. Recipe Name
    2. Ingredients
    3. Cooking Steps
    4. Nutrition Tips
    """

    response = model.generate_text(prompt=prompt)

    return response

# Title
st.title("🍳 Smart Recipe Preparation Agent")

st.markdown("""
### AI Powered Recipe Preparation Agent

Find recipes using ingredients available at home.

✅ Recipe Suggestions  
✅ Nutrition Insights  
✅ Ingredient Substitutions  
✅ Food Waste Reduction
""")

# Sidebar
st.sidebar.title("Preferences")

diet = st.sidebar.selectbox(
    "Diet Type",
    ["Any", "Vegetarian", "Vegan", "High Protein"]
)

# User Input
ingredients_input = st.text_input(
    "Enter ingredients separated by commas",
    placeholder="rice, egg, onion"
)
if st.button("🤖 Generate AI Recipe"):

    ai_recipe = generate_ai_recipe(
        ingredients_input
    )

    st.subheader("Granite AI Recipe")

    st.write(ai_recipe)
# Search Button
if st.button("Find Recipes"):

    user_ingredients = [
        ingredient.strip().lower()
        for ingredient in ingredients_input.split(",")
        if ingredient.strip()
    ]

    matches = []

    for recipe in recipes:

        score = len(
            set(user_ingredients)
            & set(recipe["ingredients"])
        )

        if score > 0:
            matches.append((score, recipe))

    matches.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    if matches:

        st.success("Recipes Found!")

        for score, recipe in matches:

            st.subheader(recipe["name"])

            st.write(
                f"⭐ Matched Ingredients: {score}"
            )

            # Ingredients
            st.write("### Ingredients")
            st.write(", ".join(recipe["ingredients"]))

            # Steps
            st.write("### Cooking Steps")

            for step_no, step in enumerate(
                recipe["steps"],
                start=1
            ):
                st.write(
                    f"{step_no}. {step}"
                )

            # Substitutions
            st.write("### Ingredient Substitutions")

            substitutions = {
                "egg": "paneer",
                "milk": "soy milk",
                "butter": "olive oil",
                "cream": "coconut cream",
                "sugar": "honey"
            }

            found_sub = False

            for ing in recipe["ingredients"]:

                if ing in substitutions:

                    st.write(
                        f"✅ {ing} → {substitutions[ing]}"
                    )

                    found_sub = True

            if not found_sub:
                st.write(
                    "No substitutions needed."
                )

            # Nutrition
            st.write("### Nutrition Estimate")

            nutrition = {
                "egg": 70,
                "rice": 130,
                "tomato": 20,
                "onion": 30,
                "chicken": 239,
                "paneer": 265,
                "milk": 60,
                "cream": 120,
                "potato": 77,
                "bread": 80
            }

            total_calories = 0

            for ing in recipe["ingredients"]:

                total_calories += nutrition.get(
                    ing,
                    50
                )

            st.success(
                f"Estimated Calories: {total_calories} kcal"
            )

            # Sustainability Score
            st.write("### Sustainability Score")

            matched = len(
                set(user_ingredients)
                & set(recipe["ingredients"])
            )

            total_needed = len(
                recipe["ingredients"]
            )

            sustainability_score = round(
                (matched / total_needed) * 100,
                2
            )

            st.progress(
                int(sustainability_score)
            )

            st.write(
                f"Ingredients Available: {sustainability_score}%"
            )

            st.divider()

    else:

        st.error(
            "No matching recipes found."
        )