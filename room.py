from encounter import Encounter
from item import Item


class Room:
    """
    This is the class for representing and storing information about the room. The rooms work similar to a linked list with adjacent rooms holding what rooms
    there are for being adjacent. Uses the encounter class to make the type of room. Uses the item class for any items dropped in the room.
    """
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
        """
        This function is for assigning room for specific directions of the room.
        """
        if not isinstance(room, Room):
            raise TypeError("Not a valid room")
        
        if not isinstance(direction, int):
            raise TypeError("direction should be an int")
        
        if direction < 0 or direction > 3:
            raise ValueError("Invalid direction value")

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
        """
        This function is for returning if a direction of the room is a dead end or not.
        """
        if not isinstance(direction, int):
            raise TypeError("Direction should be an int")

        if direction < 0 or direction > 3:
            raise ValueError("Invalid direction value")

        if self.adjacentRooms[direction]:
            return False
        else:
            return True

    # def grab_item(self, item_name : str):
    #    """
    #    This function is for checking for and taking an item out of a room. currently not implemented.
    #    """
    #
    #   if not isinstance(item_name, str):
    #        raise TypeError("Item_name should be a string")
    #
    #   for i in self.items:
    #      if i.name == item_name:
    #           self.items.remove(i)
    #          return i

    #def add_item(self, item: Item):
    #     """
    #     This function is for adding an item to a room will be used in future release.
    #     """
    #     if isinstance(item, Item):
    #         self.items.append(item)
    #     else:
    #         raise(TypeError, "Not a valid item")
         
    def directions(self):
        """
        This function returns a string with the direction of adjacent rooms to be printed to the console.
        """
        direction_string = ''
        if self.adjacentRooms[0]:
            direction_string += 'West'
            if self.adjacentRooms[1] or self.adjacentRooms[2] or self.adjacentRooms[3]:
                direction_string += ', '
        if self.adjacentRooms[1]:
            direction_string += 'North'
            if self.adjacentRooms[2] or self.adjacentRooms[3]:
                direction_string += ', '
        if self.adjacentRooms[2]:
            direction_string += 'East'
            if self.adjacentRooms[3]:
                direction_string += ', '
        if self.adjacentRooms[3]:
            direction_string += 'South'    
        return direction_string
