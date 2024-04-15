import unittest
from room import *

class MyTestCase(unittest.TestCase):

    def test_default(self):
        room = Room("This room")

        self.assertEqual(room.name, "This room")
        self.assertIsInstance(room.items, list)
        self.assertEqual(room.position, [0,0])
        self.assertIsNone(room.adjacentRooms[0])
        self.assertIsNone(room.adjacentRooms[1])
        self.assertIsNone(room.adjacentRooms[2])
        self.assertIsNone(room.adjacentRooms[3])

    def test_default_args(self):
        item = Item()
        room = Room("This room", position=[10, 0], item_list=[item])

        self.assertEqual(room.name, "This room")
        self.assertEqual(room.items[0], item)
        self.assertEqual(room.position, [10, 0])
        self.assertIsNone(room.adjacentRooms[0])
        self.assertIsNone(room.adjacentRooms[1])
        self.assertIsNone(room.adjacentRooms[2])
        self.assertIsNone(room.adjacentRooms[3])

    def test_default_initiate(self):
        room = Room("This room")
        room.initiate()

        self.assertNotEqual(room.encounter, None)

    def test_generate_monster_invalid(self):
        room = Room("This room", encounter_type=EncounterTypes.SHOP)
        room.initiate()

        self.assertEqual(room.monsters, [])

    def test_generate_items(self):
        room = Room("This room")

        while room.items == []:
            room.generate_items()

        self.assertNotEqual(room.items, [])

    def test_remove_items(self):
        room = Room("This room")

        while room.items == []:
            room.generate_items()

        item = room.items[0]
        room.remove_item(item)
        self.assertFalse(item in room.items)

    def test_remove_items_invalid(self):
        room = Room("This room")

        while room.items == []:
            room.generate_items()

        item = Item()
        item.generateItem()
        self.assertRaises(ValueError, room.remove_item, item)

    def test_direction(self):
        room = Room("This room")
        room2 = Room("That room", left = room)
        self.assertEqual(room2.adjacentRooms[0], room)

    def test_assignRoom_invalidRoom(self):
        room = Room("This room")
        badRoom = "room"
        with self.assertRaises(TypeError):
            room.assignRoom(badRoom, 1)
   
    def test_assignRoom_invalidDirection(self):
        room = Room("This room")
        room2 = Room("That room")
        with self.assertRaises(TypeError):
            room.assignRoom(room2, "dog")
        with self.assertRaises(TypeError):
            room.assignRoom(room2, 1.5)
        with self.assertRaises(ValueError):
            room.assignRoom(room2, -1)
        with self.assertRaises(ValueError):
            room.assignRoom(room2, 4)
    
    def test_assignRoom_valid(self):
        room = Room("This room")
        room2 = Room("That room")
        room.assignRoom(room2, 1)

        self.assertEqual(room2.position, [0,-1])
        self.assertEqual(room2.adjacentRooms[3], room)
        self.assertEqual(room.adjacentRooms[1], room2)

    def test_assignRoom_valid2(self):
        room = Room("This room")
        room2 = Room("That room")
        room.assignRoom(room2, 3)

        self.assertEqual(room2.position, [0,1])
        self.assertEqual(room2.adjacentRooms[1], room)
        self.assertEqual(room.adjacentRooms[3], room2)

    def test_is_dead_end_invalidDirection(self):
        room = Room("This room")
        with self.assertRaises(TypeError):
            room.is_dead_end("dog")
        with self.assertRaises(TypeError):
            room.is_dead_end(1.5)
        with self.assertRaises(ValueError):
            room.is_dead_end(-1)
        with self.assertRaises(ValueError):
            room.is_dead_end(4)

    def test_is_dead_end_valid(self):
        room = Room("This room")
        room2 = Room("That room")
        room.assignRoom(room2, 1)
        self.assertTrue(room.is_dead_end(0))
        self.assertFalse(room.is_dead_end(1))

    def test_directions(self):
        room = Room("This room")
        room2 = Room("That room")
        room3 = Room("This room")
        room4 = Room("That room")
        room5 = Room("That room")
        self.assertEqual(room.directions(), '')
        room.assignRoom(room2, 0)
        self.assertEqual(room.directions(), 'West')
        room.assignRoom(room3, 1)
        self.assertEqual(room.directions(), 'West, North')
        room.assignRoom(room4, 2)
        self.assertEqual(room.directions(), 'West, North, East')
        room.assignRoom(room5, 3)
        self.assertEqual(room.directions(), 'West, North, East, South')
