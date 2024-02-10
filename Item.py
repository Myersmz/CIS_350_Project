from enum import Enum


class ItemTypes(Enum):
    SWORD = 0
    BOW = 1
    SHIELD = 2
    POTION = 3
    ITEM = 4
    ARMOUR = 5
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

    # TODO
    def generateItem(self, item_type=ItemTypes.ITEM):
        # Will set values of this object randomly using pre-defined lists of names,
        # descriptions, and attribute values for a given itemType
        pass