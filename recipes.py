import pandas as pd
import json


class RecipeBook:
    def __init__(self):
        # Store directly as a DataFrame, do not convert to a dictionary
        try:
            self.recipes = pd.read_csv('data/recipes.csv', index_col=0)
        except FileNotFoundError:
            self.recipes = pd.DataFrame(columns=['name', 'ingredients', 'category', 'cook_time', 'cost', 'serving', 'tags'])
    
    def add_recipe(self, name, ingredients, cook_time, category, cost, serving, tags=None):
        if name.lower() in self.recipes['name'].values:
            print(f"{name} already exists in recipe book.")
            return False
        if not isinstance(ingredients, str):
            ingredients = json.dumps(ingredients)  # Convert list to JSON string if necessary
        # Create a new row DataFrame
        new_row = pd.DataFrame([{
            'name': name, 
            'ingredients': ingredients, 
            'category': category, 
            'cook_time': cook_time,
            'cost': cost,
            'serving': serving,
            'tags': tags
        }])
        
        # Append the new row to the main DataFrame
        self.recipes = pd.concat([self.recipes, new_row], ignore_index=True)
        self._save_recipes()
        return True

    def remove_recipe(self, name):
        # Check if the recipe name exists in the 'name' column
        if name.lower() in self.recipes['name'].values:
            # Drop the row where the name matches
            self.recipes = self.recipes[self.recipes['name'] != name]
            self._save_recipes()
            return True
        else:
            print(f"{name} not found in recipe book.")
            return False

    def update_recipe(self, name, ingredients=None, cook_time=None, category=None, cost=None, serving=None, tags=None):
        # Check if the recipe name exists in the 'name' column
        if name.lower() in self.recipes['name'].values:
            if ingredients is not None:
                # FIXED: Convert list to JSON string so it fits inside a single DataFrame cell
                if not isinstance(ingredients, str):
                    ingredients = json.dumps(ingredients)
                self.recipes.loc[self.recipes['name'] == name, 'ingredients'] = ingredients
                
            if cook_time is not None:
                self.recipes.loc[self.recipes['name'] == name, 'cook_time'] = cook_time
            if category is not None:
                self.recipes.loc[self.recipes['name'] == name, 'category'] = category
            if cost is not None:
                self.recipes.loc[self.recipes['name'] == name, 'cost'] = cost
            if serving is not None:
                self.recipes.loc[self.recipes['name'] == name, 'serving'] = serving
                
            if tags is not None:
                # FIXED: If tags is a list, convert it to a JSON string or comma-separated string
                if not isinstance(tags, str):
                    tags = json.dumps(tags)
                self.recipes.loc[self.recipes['name'] == name, 'tags'] = tags
                
            self._save_recipes()
            return True
        else:
            print(f"{name} not found in recipe book.")
            return False
    
    def get_recipe(self, name):
        # Check if the recipe name exists in the 'name' column
        if name.lower() in self.recipes['name'].values:
            recipe_row = self.recipes[self.recipes['name'] == name].iloc[0]
            return recipe_row.to_dict()
        else:
            print(f"{name} not found in recipe book.")
            return None
    
    def list_recipes(self):
        return self.recipes.to_dict(orient='records')
    
    def search(self, keyword=None, max_time=None, max_cost=None, **kwargs):
        """
        Search recipes with explicit handling for cook time and cost filters.
        """
        filtered_df = self.recipes.copy()

        if keyword:
            keyword_lower = str(keyword).lower()
            filtered_df = filtered_df[
                filtered_df['name'].str.contains(keyword_lower, case=False, na=False) | 
                filtered_df['ingredients'].str.lower().str.contains(keyword_lower, na=False)
            ]

        if max_time is not None:
            filtered_df = filtered_df[filtered_df['cook_time'].astype(float) <= float(max_time)]


        if max_cost is not None:
            filtered_df = filtered_df[filtered_df['cost'].astype(float) <= float(max_cost)]

        for column, value in kwargs.items():
            if column in filtered_df.columns:
                if isinstance(value, str):
                    filtered_df = filtered_df[filtered_df[column].str.contains(value, case=False, na=False)]
                else:
                    filtered_df = filtered_df[filtered_df[column] == value]

        return filtered_df.to_dict(orient='records')