from EncounterClass import Encounter
from Item import Item


class Room:

    def __init__(self, name, left=None, up=None, right=None, down=None, items=None, position=None):
        if position is None:
            position = [0, 0]
        if items is None:
            items = []
        self.name = name
        self.adjacentRooms = [left, up, right, down]
        self.items = items
        self.encounter = Encounter()
        self.position = position

    def assignRoom(self, room, direction):
        self.adjacentRooms[direction] = room

        pointerX = 0
        pointerY = 0
        if direction == 0:
            pointerX += -1
        elif direction == 1:
            pointerY += -1
        elif direction == 2:
            pointerX += 1
        elif direction == 3:
            pointerY += 1
        room.position = [self.position[0] + pointerX, self.position[1] + pointerY]

        room.adjacentRooms[(direction + 2) % 4] = self

    # def assignRoom(self, room, direction):
    #     self.adjacentRooms[direction] = room
    #     room.adjacentRooms[(direction + 2) % 4] = self

    # 0 is West, 1 is North, 2 is East, 3 is South
    def is_dead_end(self, direction:int):
        if self.adjacentRooms[direction]:
            return False
        else:
            return True

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
         
    def directions(self):
        direction_string = ''
        if self.adjacentRooms[0]:
            direction_string += 'West, '
        if self.adjacentRooms[1]:
            direction_string += 'North, '
        if self.adjacentRooms[2]:
            direction_string += 'East, '
        if self.adjacentRooms[3]:
            direction_string += 'South'    
        return direction_string



