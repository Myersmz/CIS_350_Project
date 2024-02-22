import json
import random
from enum import Enum


class ItemTypes(Enum):
    MELEE = 0
    RANGED = 1
    STAFF = 2
    SPELLBOOK = 3
    POTION = 4
    ITEM = 5
    SHIELD = 6
    ARMOUR = 7
    KEY = 10


# Represents an item. Assignable values: name, description, item_type, attribute_value. No argument is required.
class Item:
    def __init__(self, name="Unknown Item", description="Indescribable", item_type=ItemTypes.ITEM, attribute_value=0):
        self.name = name
        self.description = description
        self.type = item_type

        # attributeValue contains the attribute of the item, based on the item type.
        # For a sword this value would be the attack buff, and a shield / armour it would be the defense buff.
        # If potions are implemented this could also be used as the health that it would heal.
        self.attributeValue = attribute_value

    def generateItem(self, item_type=ItemTypes.ITEM):
        # Will set values of this object randomly using pre-defined lists of names,
        # descriptions, and attribute values for a given itemType

        # item json format
        # {"NAME": "", "DESCRIPTION": "", "ATTRIBUTE": int, "RARITY": int}
        typeString = str(item_type)[10:]
        this_item = None

        file = None
        try:
            file = open("items.json", "r")
        except:
            print("Failed to load items.")
            raise FileNotFoundError

        items = json.load(file)
        item_list = items.get(typeString, None)

        weight_sum = 0
        for item in item_list:
            weight_sum += item.get("RARITY", 0)

        choice = random.randint(1, weight_sum)

        for item in item_list:
            choice -= item.get("RARITY", 0)

            if choice <= 0:
                this_item = item
                file.close()
                break

        self.name = this_item.get("NAME")
        self.description = this_item.get("DESCRIPTION")
        self.attributeValue = this_item.get("ATTRIBUTE")
        self.type = item_type

    def display(self):
        printStr = f"--~= {self.name} =~--\n{self.description}\n"
        if self.type in [ItemTypes.MELEE, ItemTypes.RANGED]:
            printStr += f"\nAttack: {self.attributeValue}"
        elif self.type in [ItemTypes.SHIELD, ItemTypes.ARMOUR]:
            printStr += f"\nDefense: {self.attributeValue}"

        return printStr

    def __str__(self):
        return f"{self.name}: {self.description} ({self.type.name})"
