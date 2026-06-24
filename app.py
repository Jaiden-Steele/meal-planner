import streamlit as st
from pantry import Pantry
from recipes import RecipeBook
from grocery import GroceryList
from utils import conversions
import json

# Initialize the Pantry, RecipeBook, and GroceryList
pantry = Pantry()
rb = RecipeBook()
grocery_list = GroceryList()

# Flatten all units from conversions dict
units = [unit for category in conversions.values() for unit in category.keys()]

st.title("Meal Planner")

page = st.sidebar.selectbox("Navigate", [
    "Weekly Planner",
    "Recipes",
    "Pantry",
    "Grocery List"
])

if "meal_plan" not in st.session_state:
    try:
        with open("data/meal_plan.json", "r") as f:
            st.session_state.meal_plan = json.load(f)
    except FileNotFoundError:
        st.session_state.meal_plan = []


if page == "Weekly Planner":
    st.header("Weekly Meal Planner")
    st.subheader("Find Recipes")
    max_time = st.slider("Maximum Cooking Time (minutes)", 0, 120, 30)
    max_cost = st.slider("Maximum Cost ($)", 0, 50, 20)
    keyword = st.text_input("Search Keywords")
    results = rb.search(keyword=keyword, max_time=max_time, max_cost=max_cost)
    if results:
        st.subheader("Search Results")
        for recipe in results:
            recipe_name = recipe['name']
            if recipe_name not in st.session_state:
                st.session_state[recipe_name] = recipe_name in st.session_state.meal_plan
            checked = st.checkbox(
                f"{recipe_name} - {recipe['cook_time']} min - ${recipe['cost']}",
                key=recipe_name
            )
            if checked and (recipe_name not in st.session_state.meal_plan):
                st.session_state.meal_plan.append(recipe_name)
                grocery_list.add_items_from_recipe(recipe)
                st.toast(f"Calculated missing ingredients for {recipe_name} and added to Grocery List!")
            elif not checked and (recipe_name in st.session_state.meal_plan):
                st.session_state.meal_plan.remove(recipe_name)
    else:
        st.write("No recipes found matching the criteria.")

    st.subheader("This Week's Meals")
    if st.session_state.meal_plan:
        for meal in st.session_state.meal_plan:
            st.write(f"✓ {meal}")
    else:
        st.write("No meals planned yet!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Meal Plan"):
            with open("data/meal_plan.json", "w") as f:
                json.dump(st.session_state.meal_plan, f)
            st.success("Meal plan saved!")
    with col2:
        if st.button("Reset Week"):
            st.session_state.meal_plan = []
            with open("data/meal_plan.json", "w") as f:
                json.dump([], f)
            grocery_list.items = grocery_list.items.iloc[0:0]
            grocery_list._save_grocery_list()
            st.success("Week reset!")

if page == "Recipes":
    st.header("Recipes")
    action = st.selectbox("Choose an action", ["Add Recipe", "Remove Recipe", "Update Recipe", "View Recipe", "List Recipes"])

    if action == "Add Recipe":
        with st.form("add_recipe_form"):
            name = st.text_input("Recipe Name")
            if "add_ingredients" not in st.session_state:
                st.session_state.add_ingredients = []

            col1, col2, col3 = st.columns(3)
            with col1:
                ing_name = st.text_input("Ingredient", key="add_ing_name")
            with col2:
                ing_qty = st.number_input("Quantity", min_value=0.0, step=0.1, key="add_ing_qty")
            with col3:
                ing_unit = st.selectbox("Unit", units, key="add_ing_unit")

            def handle_add_ingredient():
                name_val = st.session_state.add_ing_name
                qty_val = st.session_state.add_ing_qty
                unit_val = st.session_state.add_ing_unit
                if name_val.strip():
                    st.session_state.add_ingredients.append({
                        "name": name_val,
                        "quantity": qty_val,
                        "unit": unit_val
                    })

            st.form_submit_button("Add Ingredient", on_click=handle_add_ingredient)
            st.write("Current ingredients:", st.session_state.add_ingredients)

            category = st.text_input("Category")
            cook_time = st.number_input("Cook Time (minutes)", min_value=0)
            cost = st.number_input("Cost ($)", min_value=0.0, format="%.2f")
            serving = st.number_input("Serving Size", min_value=1)
            tags_input = st.text_area("Tags (comma-separated)")
            tags = [t.strip() for t in tags_input.split(',')] if tags_input else []

            if st.form_submit_button("Add Recipe"):
                success = rb.add_recipe(name, st.session_state.add_ingredients, cook_time, category, cost, serving, tags)
                if success:
                    st.session_state.add_ingredients = []
                    st.success(f"Recipe '{name}' added successfully!")
                else:
                    st.error(f"Recipe '{name}' already exists!")

    elif action == "Remove Recipe":
        with st.form("remove_recipe_form"):
            name = st.text_input("Recipe Name to Remove")
            if st.form_submit_button("Remove"):
                if rb.remove_recipe(name):
                    st.success(f"Recipe '{name}' removed successfully!")
                else:
                    st.error(f"Recipe '{name}' not found.")

    elif action == "Update Recipe":
        with st.form("update_recipe_form"):
            name = st.text_input("Recipe Name to Update")
            if "update_ingredients" not in st.session_state:
                st.session_state.update_ingredients = []

            col1, col2, col3 = st.columns(3)
            with col1:
                ing_name = st.text_input("Ingredient", key="update_ing_name")
            with col2:
                ing_qty = st.number_input("Quantity", min_value=0.0, step=0.1, key="update_ing_qty")
            with col3:
                ing_unit = st.selectbox("Unit", units, key="update_ing_unit")

            def handle_update_ingredient():
                name_val = st.session_state.update_ing_name
                qty_val = st.session_state.update_ing_qty
                unit_val = st.session_state.update_ing_unit
                if name_val.strip():
                    st.session_state.update_ingredients.append({
                        "name": name_val,
                        "quantity": qty_val,
                        "unit": unit_val
                    })

            st.form_submit_button("Add Ingredient", on_click=handle_update_ingredient)
            st.write("New ingredients:", st.session_state.update_ingredients)

            category = st.text_input("New Category")
            cook_time = st.number_input("New Cook Time (minutes)", min_value=0)
            cost = st.number_input("New Cost ($)", min_value=0.0, format="%.2f")
            serving = st.number_input("New Serving Size", min_value=1)
            tags_input = st.text_area("New Tags (comma-separated)")
            tags = [t.strip() for t in tags_input.split(',')] if tags_input else []

            if st.form_submit_button("Update Recipe"):
                ing_to_pass = st.session_state.update_ingredients if st.session_state.update_ingredients else None
                if rb.update_recipe(name, ing_to_pass, category or None, cook_time or None, cost or None, serving or None, tags or None):
                    st.session_state.update_ingredients = []
                    st.success(f"Recipe '{name}' updated successfully!")
                else:
                    st.error(f"Recipe '{name}' not found.")

    elif action == "View Recipe":
        with st.form("view_recipe_form"):
            name = st.text_input("Recipe Name to View")
            if st.form_submit_button("View"):
                recipe = rb.get_recipe(name)
                if recipe:
                    st.write(f"**Category:** {recipe['category']}")
                    st.write(f"**Cook Time:** {recipe['cook_time']} minutes")
                    st.write(f"**Cost:** ${recipe['cost']}")
                    st.write(f"**Serving Size:** {recipe['serving']}")
                    st.write(f"**Tags:** {recipe['tags']}")
                    st.write(f"**Ingredients:** {recipe['ingredients']}")
                else:
                    st.error(f"Recipe '{name}' not found.")

    elif action == "List Recipes":
        recipes = rb.list_recipes()
        if recipes:
            st.subheader("All Recipes")
            for recipe in recipes:
                with st.expander(f"{recipe['name']} - {recipe['cook_time']} min - ${recipe['cost']}"):
                    st.write(f"Category: {recipe['category']}")
                    st.write(f"Serving Size: {recipe['serving']}")
                    st.write(f"Tags: {recipe['tags']}")
                    st.write(f"Ingredients: {recipe['ingredients']}")
        else:
            st.write("No recipes available.")

if page == "Pantry":
    st.header("Pantry Inventory")
    action = st.selectbox("Choose an action", ["Add Item", "Remove Item", "Update Item", "View Inventory"])

    if action == "Add Item":
        with st.form("add_item_form"):
            item_name = st.text_input("Item Name")
            quantity = st.number_input("Quantity", min_value=0.0, step=0.1)
            unit = st.selectbox("Unit", units)
            if st.form_submit_button("Add Item") and item_name:
                pantry.add_item(item_name, quantity, unit)
                st.success(f"Added {quantity} {unit} of '{item_name}' to pantry.")

    elif action == "Remove Item":
        with st.form("remove_item_form"):
            item_name = st.text_input("Item Name to Remove")
            quantity = st.number_input("Quantity to Remove", min_value=0.0, step=0.1)
            unit = st.selectbox("Unit", units)
            if st.form_submit_button("Remove Item") and item_name:
                if pantry.remove_item(item_name, quantity, unit):
                    st.success(f"Removed {quantity} {unit} of '{item_name}' from pantry.")
                else:
                    st.error(f"'{item_name}' not found or units could not be converted.")

    elif action == "Update Item":
        with st.form("update_item_form"):
            item_name = st.text_input("Item Name to Update")
            quantity = st.number_input("New Quantity", min_value=0.0, step=0.1)
            unit = st.selectbox("New Unit", units)
            if st.form_submit_button("Update Item") and item_name:
                if pantry.update_item(item_name, quantity, unit):
                    st.success(f"Updated '{item_name}' to {quantity} {unit}.")
                else:
                    st.error(f"'{item_name}' not found. Use 'Add Item' to create it.")

    elif action == "View Inventory":
        inventory = pantry.inventory
        if inventory:
            for item, values in inventory.items():
                # Fixed: access dict keys instead of tuple indices
                qty = values["quantity"]
                unit = values["unit"]
                st.write(f"- **{item.capitalize()}**: {qty} {unit}")
        else:
            st.write("Pantry is empty.")

if page == "Grocery List":
    st.header("Grocery List")
    action = st.selectbox("Choose an action", ["Add Item", "Remove Item", "View List"])

    if action == "Add Item":
        with st.form("add_grocery_item_form"):
            item_name = st.text_input("Item Name")
            quantity = st.number_input("Quantity", min_value=0.0, step=0.1)
            unit = st.selectbox("Unit", units)
            if st.form_submit_button("Add to Grocery List") and item_name:
                grocery_list.add_item(item_name, quantity, unit)
                st.success(f"Added {quantity} {unit} of '{item_name}' to grocery list.")

    elif action == "Remove Item":
        with st.form("remove_grocery_item_form"):
            item_name = st.text_input("Item Name to Remove")
            if st.form_submit_button("Remove from Grocery List") and item_name:
                # Remove row from DataFrame where name matches
                mask = grocery_list.items['name'].str.lower() == item_name.lower()
                if mask.any():
                    grocery_list.items = grocery_list.items[~mask]
                    grocery_list._save_grocery_list()
                    st.success(f"Removed '{item_name}' from grocery list.")
                else:
                    st.error(f"'{item_name}' not found in grocery list.")

    elif action == "View List":
        items = grocery_list.items.to_dict(orient='records')
        if items:
            for item in items:
                st.write(f"- **{str(item['name']).capitalize()}**: {item['quantity']} {item['unit']}")
        else:
            st.write("Grocery list is empty.")