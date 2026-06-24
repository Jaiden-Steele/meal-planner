# Meal Planner

> Tired of staring into your fridge wondering what you can make with half a bag of pasta and some questionable leftovers? Meal Planner has you covered. Add your recipes, track what's in your pantry, filter meals by cook time and budget, and let the app figure out exactly what you need to buy this week. No more buying ingredients you already have, no more realizing halfway through cooking that you're out of something.

Built with Python and Streamlit, with pandas powering the recipe filtering under the hood.

---

## Features

- **Weekly Meal Planner** — filter recipes by max cook time and cost, pick your meals for the week with checkboxes, and save your plan
- **Automatic Grocery List** — checks your pantry against each recipe and only adds what you're actually missing
- **Recipe Book** — add, update, remove, and browse recipes with full ingredient tracking
- **Pantry Tracker** — keep your inventory up to date with add, remove, and update operations
- **Smart Unit Conversion** — automatically converts between units (cups, ml, g, oz, etc.) when comparing pantry stock to recipe requirements
- **Reset Week** — clears your meal plan and grocery list at the end of the week so you can start fresh

---

## Project Structure

```
meal_planner/
├── app.py              # Streamlit web interface
├── pantry.py           # Pantry class — inventory management
├── recipes.py          # RecipeBook class — recipe management (pandas DataFrame)
├── grocery.py          # GroceryList class — grocery list generation
├── utils.py            # Unit conversion dictionary and helper functions
└── data/
    ├── pantry.json        # Pantry inventory (auto-created)
    ├── recipes.csv        # Recipe database (auto-created)
    ├── grocery_list.json  # Current grocery list (auto-created)
    └── meal_plan.json     # Current week's meal plan (auto-created)
```

---

## Setup

### 1. Create a conda environment

```bash
conda create -n meal-planner python=3.11
conda activate meal-planner
```

### 2. Install dependencies

```bash
pip install streamlit pandas
```

### 3. Run the app

```bash
streamlit run app.py
```

The app will open automatically in your browser. All data files are created automatically in the `data/` folder on first run.

---

## Usage

### Weekly Planning
1. Navigate to **Weekly Planner** in the sidebar
2. Use the sliders to filter by max cook time and cost
3. Optionally search by keyword
4. Check the recipes you want to make this week — the grocery list updates automatically
5. Click **Save Meal Plan** to persist your selections
6. Head to **Grocery List** to see exactly what you need to buy
7. After shopping, update your pantry and hit **Reset Week** to start fresh

### Managing Recipes
1. Navigate to **Recipes** in the sidebar
2. Use **Add Recipe** to create a new recipe — add ingredients one at a time using the ingredient form
3. Use **List Recipes** to browse your full collection with expandable detail cards
4. Use **View Recipe**, **Update Recipe**, or **Remove Recipe** as needed

### Managing Your Pantry
1. Navigate to **Pantry** in the sidebar
2. **Add Item** when you buy something new
3. **Remove Item** to reduce quantity after using an ingredient
4. **Update Item** to set a new quantity directly
5. **View Inventory** to see everything you currently have

---

## Supported Units

The app handles automatic unit conversion across four categories:

| Category | Units |
|----------|-------|
| Volume | ml, l, tsp, tbsp, fl oz, cup, pt, qt, gal |
| Weight | mg, g, kg, oz, lb |
| Count | whole, clove, slice, piece, can, bottle, package, box, bag, jar, container, pcs |
| Length | mm, cm, m, km, in, ft, yd, mi |

Units within the same category convert automatically. Attempting to convert across categories (e.g. cups to grams) will return a helpful message suggesting alternative units.

---

## Data Storage

All data is stored locally in the `data/` directory as JSON and CSV files. Nothing is sent to any external server.

---

## Known Issues

- `grocery.py` currently loads the pantry from `inventory.json` in the root directory instead of `data/pantry.json`. This means the grocery generator may not correctly reflect your current pantry stock. Fix by updating the path in `grocery.py` to `data/pantry.json`.

---

## Future Ideas

- PDF recipe import using an LLM API to automatically parse and structure recipes
- Nutritional tracking per recipe and per week
- Meal history and favourites
- Weekly cost estimates and budget tracking
- Random recipe picker for the indecisive
