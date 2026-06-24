
import json
from utils import convert, find_category


class Pantry:
    def __init__(self):
        self.inventory = {}
        # Load and save file in /data directory to avoid cluttering the main project directory
        # load inventory from a JSON file if it exists
        try:
            with open('data/pantry.json', 'r') as f:
                self.inventory = json.load(f)
        except FileNotFoundError:
            pass

    def _save_inventory(self):
        with open('data/pantry.json', 'w') as f:
            json.dump(self.inventory, f)

    def add_item(self, item_name, quantity, unit):
        # Normalize key names to lowercase for case-insensitivity
        item_key = item_name.lower().strip()
        
        if item_key in self.inventory:
            existing_quantity, existing_unit = self.inventory[item_key]
            converted_quantity = convert(quantity, unit, existing_unit)
            if converted_quantity is not None:
                self.inventory[item_key] = [existing_quantity + converted_quantity, existing_unit]
        else:
            # Save original casing display name or just use lowercase consistently
            self.inventory[item_key] = [quantity, unit]
        self._save_inventory()
        return True

    def remove_item(self, item_name, quantity, unit):
        item_key = item_name.lower().strip()
        
        if item_key in self.inventory:
            existing_quantity, existing_unit = self.inventory[item_key]
            converted_quantity = convert(quantity, unit, existing_unit)
            
            if converted_quantity is not None:
                new_quantity = existing_quantity - converted_quantity
                self.inventory[item_key] = [new_quantity, existing_unit]
                
                if self.inventory[item_key][0] <= 0:
                    del self.inventory[item_key]
                self._save_inventory()
                return True
        return False

    def update_item(self, item_name, quantity, unit):
        item_key = item_name.lower().strip()
        
        if item_key in self.inventory:
            self.inventory[item_key] = [quantity, unit]
            self._save_inventory()
            return True
        return False