# Make Conversion Dictionary
conversions = {
    "volume": {
        "ml": 1,
        "l": 1000,
        "tsp": 4.92892,
        "tbsp": 14.7868,
        "fl oz": 29.5735,
        "cup": 236.588,
        "pt": 473.176,
        "qt": 946.353,
        "gal": 3785.41
    },
    "weight": {
        "mg": 0.001,
        "g": 1,
        "kg": 1000,
        "oz": 28.3495,
        "lb": 453.592
    },
    "length": {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1,
        "km": 1000,
        "in": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
        "mi": 1609.34
    },
    "count": {
        "whole": 1,
        "clove": 1,
        "slice": 1,
        "piece": 1,
        "can": 1,
        "bottle": 1,
        "package": 1,
        "box": 1,
        "bag": 1,
        "jar": 1,
        "container": 1,
        "pcs": 1
    }
}
# Helper Functions
def convert(quantity, from_unit, to_unit):
    from_unit_cat = find_category(from_unit)
    to_unit_cat = find_category(to_unit)

    if from_unit_cat is None:
        print(f"{from_unit} is not a recognized unit, please try a different unit.")
        return None
    if to_unit_cat is None:
        print(f"{to_unit} is not a recognized unit, please try a different unit.")
        return None
    if from_unit_cat == to_unit_cat:
        return quantity * (conversions[from_unit_cat][from_unit] / conversions[to_unit_cat][to_unit])
        
    else:
        from_unit_features = conversions[from_unit_cat].keys()
        print(f"Units are not in the same category, try and find any of these units on the package: {', '.join(from_unit_features)}")
        print("insert corrected value and unit if found:")
        return None
    
def find_category(unit):
    for category in conversions.keys():
        if unit in conversions[category]:
            return category
    return None
