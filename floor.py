from room import *
from statistic import Statistic, multipliers


class Floor:
    """
    Represents a whole game floor, and can be regenerated without creating a new object.
    Also handles increasing the difficulty when clearing floors.
    """
    def __init__(self):
        self.dungeon_size = 8
        self.cleared_floors = 0

        self.current_room = self.generate_floor()

    def generate_new_floor(self):
        """
        Generates a new floor and increases the difficulty.
        :return:
        """
        self.cleared_floors += 1
        self.increase_difficulty()
        self.current_room = self.generate_floor()

    def room(self) -> Room:
        """
        Accessor for self.current_room
        :return:
        """
        return self.current_room

    def increase_difficulty(self):
        """
        Increases the games difficultly by applying global stat buffs for monsters and increases the floor size.
        Also increases the effectiveness of items.
        """

        # Returns a multiplier value
        def random_buff_value():
            return (random.randint(10, 35) + 100) / 100

        # Checks for this being the first floor of the game.
        if self.cleared_floors == 0:
            return

        self.dungeon_size += 4

        attack_buff = random_buff_value()
        defense_buff = random_buff_value()
        health_buff = random_buff_value()
        item_buff = max(attack_buff, defense_buff, health_buff) + ((attack_buff + defense_buff + health_buff) / 3)

        # # Sets stats for monsters
        multipliers["attack"].append(Statistic("Dark Aura", multiplier=attack_buff))
        multipliers["defense"].append(Statistic("Dark Aura", multiplier=defense_buff))
        multipliers["health"].append(Statistic("Dark Aura", multiplier=health_buff))

        # Sets stats for item spawns. This is an attempt to balance difficulty.
        multipliers["item"].append(Statistic("Mystical Aura", multiplier=item_buff))

    def generate_floor(self, room_count: int = None):
        """
        Generates all rooms for a playable game.
        :param room_count: Number of rooms to generate. Default: follows difficulty increase.
        :return:Room - Entrance to the floor
        """
        if room_count is None:
            room_count = self.dungeon_size

        if room_count < 3:
            raise ValueError("Must be three or larger")

        entrance = Room("Floor Entrance")
        entrance.encounter_type = EncounterTypes.EMPTY
        rooms = [entrance]
        roomMap = {0: {0: entrance}}
        createdRooms = 1

        # Generate rooms
        while createdRooms < room_count:
            parent_room = rooms[random.randint(0, len(rooms) - 1)]
            direction = random.randint(0, 3)

            # The direction does not lead to a room, meaning one can be placed there.
            if parent_room.adjacentRooms[direction] is None:
                createdRooms += 1
                new_room = Room("Room " + str(createdRooms))

                parent_room.assignRoom(new_room, direction)
                rooms.append(new_room)

                # Assigns the room to the map dictionary for linking rooms together.
                if roomMap.get(new_room.position[0], None) is None:
                    roomMap[new_room.position[0]] = {new_room.position[1]: new_room}
                else:
                    roomMap[new_room.position[0]][new_room.position[1]] = new_room

                new_room_position = new_room.position

                # Checks for neighboring rooms and links to them.
                rm = roomMap.get(new_room_position[0] - 1, {}).get(new_room_position[1], None)
                if rm is not None and rm != parent_room:
                    rm.assignRoom(new_room, 2)
                rm = roomMap.get(new_room_position[0], {}).get(new_room_position[1] - 1, None)
                if rm is not None and rm != parent_room:
                    rm.assignRoom(new_room, 3)
                rm = roomMap.get(new_room_position[0] + 1, {}).get(new_room_position[1], None)
                if rm is not None and rm != parent_room:
                    rm.assignRoom(new_room, 0)
                rm = roomMap.get(new_room_position[0], {}).get(new_room_position[1] + 1, None)
                if rm is not None and rm != parent_room:
                    rm.assignRoom(new_room, 1)

        other_rooms = [rooms.pop(0)]  # removes the entrance for the list because we want it to be empty.

        # Add boss room to a room with the least connections to prevent map splitting.
        rooms.sort(key=lambda room: len([x for x in room.adjacentRooms if x is not None]))
        min_connections = len([x for x in rooms[0].adjacentRooms if x is not None])
        leaf_rooms = [x for x in rooms if len([x for x in rooms[0].adjacentRooms if x is not None]) == min_connections]
        position = random.randint(0, len(leaf_rooms) - 1)
        leaf_rooms[position].encounter_type = EncounterTypes(100)
        boss_room = leaf_rooms.pop(position)
        other_rooms.append(boss_room)
        rooms.remove(boss_room)

        # Assign other required EncounterTypes to a random room.
        for i in range(101, max_single_rooms + 1):
            position = random.randint(0, len(rooms) - 1)
            rooms[position].encounter_type = EncounterTypes(i)
            other_rooms.append(rooms.pop(position))
    
        # Initiates the encounter object in every room.
        for room in rooms + other_rooms:
            room.initiate()

        return entrance
