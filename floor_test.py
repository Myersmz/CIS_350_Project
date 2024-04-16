import unittest
from floor import *
from statistic import Statistic, multipliers


class FloorTest(unittest.TestCase):

    def test_initiate(self):
        floor = Floor()

        self.assertEqual(floor.dungeon_size, 8)
        self.assertEqual(floor.cleared_floors, 0)
        self.assertTrue(type(floor.current_room) == Room)

    def test_generate_new_floor(self):
        floor = Floor()
        old_room = floor.current_room

        floor.generate_new_floor()

        self.assertEqual(floor.dungeon_size, 12)
        self.assertEqual(floor.cleared_floors, 1)
        self.assertTrue(type(floor.current_room) == Room)
        self.assertNotEqual(old_room, floor.current_room)

    def test_room(self):
        floor = Floor()
        self.assertNotEqual(floor.room(), None)

    def test_increase_difficulty1(self):
        # Tests that nothing changes when cleared floors is not increased.
        floor = Floor()

        floor.increase_difficulty()
        self.assertEqual(floor.dungeon_size, 8)
        self.assertEqual(floor.cleared_floors, 0)
        self.assertTrue(type(floor.current_room) == Room)

    def test_increase_difficulty2(self):
        # Checks that the entire function runs.
        floor = Floor()

        floor.cleared_floors += 1
        floor.increase_difficulty()
        self.assertEqual(floor.dungeon_size, 12)
        self.assertEqual(floor.cleared_floors, 1)
        self.assertTrue(type(floor.current_room) == Room)

    def test_generate_floor(self):
        floor = Floor()
        new_room = floor.generate_floor()
        self.assertNotEqual(new_room, floor.current_room)

    def test_generate_floor1(self):
        floor = Floor()
        new_room = floor.generate_floor(20)
        self.assertNotEqual(new_room, floor.current_room)

    def test_generate_floor_invalid(self):
        floor = Floor()
        self.assertRaises(ValueError, floor.generate_floor, 2)

    def test_generate_floor_invalid1(self):
        floor = Floor()
        self.assertRaises(ValueError, floor.generate_floor, -2)



if __name__ == '__main__':
    unittest.main()
