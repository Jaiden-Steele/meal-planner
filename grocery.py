import json
import pandas as pd
from utils import convert

class GroceryList:
    def __init__(self):
        # 1. Load the Grocery List JSON
        try:
            # We reset the index to move the item name from the index back into a true column
            self.items = pd.read_json("data/grocery_list.json", orient="index").reset_index(names=["name"])
        except (FileNotFoundError, ValueError):
            self.items = pd.DataFrame(columns=["name", "quantity", "unit"])

        # 2. Load the Pantry JSON (FIXED: points to root 'inventory.json' used by your Pantry class)
        try:
            # We reset the index here as well to cleanly expose a 'name' column for masks
            self.pantry = pd.read_json("inventory.json", orient="index").reset_index(names=["name"])
        except (FileNotFoundError, ValueError):
            self.pantry = pd.DataFrame(columns=["name", "quantity", "unit"])

    def _save_grocery_list(self):
        # Move 'name' to the index temporarily so orient="index" formats cleanly
        save_df = self.items.set_index("name")
        save_df.to_json(
            "data/grocery_list.json", orient="index", indent=4
        )

    def add_item(self, name, quantity, unit):
        name_lower = str(name).lower().strip()
        match_mask = self.items["name"].astype(str).str.lower() == name_lower
        
        if match_mask.any():
            existing_quantity = self.items.loc[match_mask, "quantity"].values[0]
            existing_unit = self.items.loc[match_mask, "unit"].values[0]
            converted_quantity = convert(quantity, unit, existing_unit)
            
            if converted_quantity is not None:
                new_quantity = existing_quantity + converted_quantity
                self.items.loc[match_mask, "quantity"] = new_quantity
        else:
            new_row = pd.DataFrame(
                [{"name": name, "quantity": quantity, "unit": unit}]
            )
            self.items = pd.concat([self.items, new_row], ignore_index=True)
            
        self._save_grocery_list()
        return True

    # FIXED: Added missing method required by your Streamlit interface
    def remove_item(self, item_name):
        name_lower = str(item_name).lower().strip()
        match_mask = self.items["name"].astype(str).str.lower() == name_lower
        
        if match_mask.any():
            self.items = self.items[~match_mask].reset_index(drop=True)
            self._save_grocery_list()
            return True
        return False

    # FIXED: Added missing method required by your Streamlit interface
    def list_items(self):
        # Converts the internal DataFrame to records so the frontend for-loop doesn't break
        return self.items.to_dict(orient="records")

    def add_items_from_recipe(self, recipe_row):
        """Expects a pandas Series or dict containing an 'ingredients' JSON string."""
        # Reload pantry database to ensure calculations are based on fresh data
        try:
            self.pantry = pd.read_json("inventory.json", orient="index").reset_index(names=["name"])
        except (FileNotFoundError, ValueError):
            self.pantry = pd.DataFrame(columns=["name", "quantity", "unit"])

        try:
            if isinstance(recipe_row, dict):
                ingredients_list = json.loads(recipe_row["ingredients"])
            else:
                ingredients_list = json.loads(recipe_row["ingredients"])
        except (json.JSONDecodeError, TypeError, KeyError):
            print("Error: Invalid or missing ingredients format in recipe.")
            return

        for item in ingredients_list:
            ingredient = item.get("name")
            req_qty = item.get("quantity")
            req_unit = item.get("unit")
            
            if ingredient is None or req_qty is None or req_unit is None:
                continue
                
            ing_lower = str(ingredient).lower().strip()
            pantry_mask = self.pantry["name"].str.lower() == ing_lower
            
            if pantry_mask.any():
                pantry_qty = self.pantry.loc[pantry_mask, "quantity"].values[0]
                pantry_unit = self.pantry.loc[pantry_mask, "unit"].values[0]
                converted_pantry_qty = convert(pantry_qty, pantry_unit, req_unit)
                
                if converted_pantry_qty is not None:
                    needed_qty = req_qty - converted_pantry_qty
                    if needed_qty > 0:
                        self.add_item(ingredient, needed_qty, req_unit)
                else:
                    self.add_item(ingredient, req_qty, req_unit)
            else:
                self.add_item(ingredient, req_qty, req_unit)
