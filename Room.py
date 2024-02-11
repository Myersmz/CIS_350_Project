from EncounterClass import Encounter
from Item import Item


class Room:

    def __init__(self, name, left=None, up=None, right=None, down=None, items=None):
        if items is None:
            items = []
        self.name = name
        self.adjacentRooms = [left, up, right, down]
        self.items = items
        self.encounter = Encounter()

    def enter_room(self):
        print(f'You have entered {self.name}')
        return self.encounter

    # 1 is left, 2 is up, 3 is right, 4 is down
    def is_dead_end(self, direction:int):
        if self.adjacentRooms[direction]:
            return True
        else:
            return False

    def grab_item(self, item_name : str):
        for i in self.items:
            if i.name == item_name:
                self.items.remove(i)
                return i

    def add_item(self, item: Item):
         if isinstance(item, Item):
             self.items.append(item)
         else:
             raise(TypeError, "Not a valid item")



