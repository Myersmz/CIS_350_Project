import json
import random
from enum import Enum


file = open("items.json", "r")
items = json.load(file)
file.close()


# Easily represents an item type.
class ItemTypes(Enum):
    MELEE = 0
    RANGED = 1
    STAFF = 2
    SPELLBOOK = 3
    POTION = 4
    ITEM = 5
    SHIELD = 6
    ARMOUR = 7
    KEY = 8


# Must be set for other code to work
max_item_types = 8


class Item:
    """
    Represent an item object to be utilized in the context of inventory and within environments.
    Supports creating an item from scratch, or randomly selecting a predefined item from "items.json".
    """
    def __init__(self, name="Unknown Item", description="Indescribable", item_type=ItemTypes.ITEM, attribute_value=0):
        self.name = name
        self.description = description
        self.type = item_type
        self.price = None

        # 'attributeValue' contains the attribute of the item, based on the item type.
        # For a sword this value would be the attack buff, and a shield / armour it would be the defense buff.
        # If potions are implemented this could also be used as the health that it would heal.
        # It is possible for this value to be a list of 2 values to represent a range of its value.
        self.attributeValue = attribute_value

    def generateItem(self, item_type=ItemTypes.ITEM):
        """
        Will set values of this object randomly using a pre-defined list.
        :param item_type: Type of item to get.
        :return:
        """

        # item json format
        # {"NAME": "", "DESCRIPTION": "", "ATTRIBUTE": int, "RARITY": int}
        typeString = str(item_type)[10:]
        this_item = None

        item_list = items.get(typeString, None)

        # Sums the total weight of items from the list of a single type.
        weight_sum = 0
        for item in item_list:
            weight_sum += item.get("RARITY", 0)

        choice = random.randint(1, weight_sum)

        # Run through the list until the value of choice reaches 0 or below.
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
        """
        A slightly decorated way of displaying an item. Uses 3+ lines.
        Intended to be used when picking up an item from a room or a monster.
        :return:
        """
        printStr = f"--~= {self.name} =~--\n{self.description}\n"
        if self.type in [ItemTypes.MELEE, ItemTypes.RANGED]:
            printStr += f"\nAttack: {self.attributeValue}"
        elif self.type in [ItemTypes.SHIELD, ItemTypes.ARMOUR]:
            printStr += f"\nDefense: {self.attributeValue}"

        return printStr

    def get_attribute(self) -> int:
        """
        Returns a value for this items attribute. Since attributeValue can be a list for a range,
        this method standardizes how that is handled.
        :return:
        """
        if type(self.attributeValue) == list:
            return random.randint(self.attributeValue[0], self.attributeValue[1])
        return self.attributeValue

    def __str__(self):
        """
        Single-line representation.
        :return:
        """
        return f"{self.name}: {self.description} ({self.type.name})"
