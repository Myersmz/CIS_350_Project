from encounter import *
from item import *
import character


class Room:
    """
    This is the class for representing and storing information about the room. The rooms work similar to a linked list
    with adjacent rooms holding what rooms there are for being adjacent. Uses the encounter class to make the type of
    room. Uses the item class for any items dropped in the room.
    """

    def __init__(self, name, left=None, up=None, right=None, down=None, item_list=None, position=None,
                 encounter_type=None):
        if position is None:
            position = [0, 0]
        self.position = position

        if item_list is None:
            item_list = []
        self.items = item_list

        if encounter_type is None:
            encounter_type = random.randint(1, max_generation_rooms)
        self.encounter_type = encounter_type

        self.name = name
        self.adjacentRooms = [left, up, right, down]
        self.encounter = None
        self.monsters = []
        self.visited = False

    def initiate(self):
        """
        Initiates the room, creates the encounter, generates monsters and items.
        :return:
        """
        self.encounter = Encounter(self.encounter_type)
        self.generate_monsters()
        self.generate_items()

    def generate_monsters(self):
        """
        Generates monsters in the room
        :return:
        """
        if self.encounter_type in (EncounterTypes.BOSS, EncounterTypes.TRAP, EncounterTypes.SHOP):
            return

        for i in range(random.randint(0, 3)):
            self.monsters.append(character.get_monster())

    def generate_items(self):
        """
        Generates items within the room
        :return:
        """
        # Does not generate in boss or shop rooms.
        if self.encounter_type in (EncounterTypes.BOSS, EncounterTypes.SHOP):
            return

        # Room can have 1 to 3 items, or none.
        count = random.randint(-1, 2)

        for i in range(count):
            new_item = Item()
            new_item_type = ItemTypes(random.randint(0, max_item_types - 1))
            new_item.generateItem(new_item_type)
            self.items.append(new_item)

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
        else:  # direction == 3
            pointerY += 1
        room.position = [self.position[0] + pointerX, self.position[1] + pointerY]

        room.adjacentRooms[(direction + 2) % 4] = self

    # 0 is West, 1 is North, 2 is East, 3 is South
    def is_dead_end(self, direction: int):
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

    def remove_item(self, item: Item):
        """
        Removes an item from the inventory.
        :param item: Item from the inventory.
        """
        if item not in self.items:
            raise ValueError("This item is not in the inventory.")

        self.items.remove(item)
        # for i in range(len(self.items)):
        #     if self.items[i] == item:
        #         self.items.pop(i)
        #         return
        # raise ValueError("Could not locate the item in the inventory.")

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
