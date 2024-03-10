import random
import unittest

from EncounterClass import *


class EncounterTester(unittest.TestCase):

    def setUp(self):
        # Use a fixed seed for consistent, repeatable testing of random behavior
        random.seed(1234)

    def test_init(self):
        """Ensures valid and invalid encounter types are handled correctly."""

        # Test valid types
        enc1 = Encounter(EncounterTypes.BOSS)
        self.assertEqual(enc1.encounter_type, EncounterTypes.BOSS)
        self.assertFalse(enc1.is_empty)  # Boss fight is not an empty room
        enc2 = Encounter(EncounterTypes.PUZZLE)
        self.assertEqual(enc2.encounter_type, EncounterTypes.PUZZLE)
        self.assertFalse(enc2.is_empty)  # Puzzle room is not an empty room
        enc3 = Encounter(EncounterTypes.EMPTY)
        self.assertEqual(enc3.encounter_type, EncounterTypes.EMPTY)
        self.assertTrue(enc3.is_empty)  # Empty room is empty

        # Test invalid types
        with self.assertRaises(ValueError):
            Encounter(0)
        with self.assertRaises(ValueError):
            Encounter(4)

    def test_random_encounter_type(self):
        """Verifies that random encounters generate expected types."""
        # Repeated tests increase coverage
        for _ in range(10):
            enc = Encounter()
            self.assertTrue(enc.encounter_type in EncounterTypes)
            if enc.encounter_type == EncounterTypes.BOSS:
                self.assertFalse(enc.is_empty)  # Boss fight is not an empty room
            elif enc.encounter_type == EncounterTypes.PUZZLE:
                self.assertFalse(enc.is_empty)  # Puzzle room is not an empty room
            else:
                self.assertTrue(enc.is_empty)  # Empty room is empty

    def test_boss_fight(self):
        """Asserts that boss fights generate appropriate monsters."""
        enc = Encounter(EncounterTypes.BOSS)
        enc.boss_fight()

        # Check monster scaling (might need adjustment based on your logic)
        self.assertGreater(enc.boss.health, 0)
        self.assertGreater(enc.boss.attack, 0)
        self.assertGreater(enc.boss.defense, 0)

        # Ensure the boss name is actually in the monster list
        self.assertIn(enc.boss.name, enc.Monsters)

    def test_puzzle_room(self):
        """Verifies that puzzle rooms generate valid questions and answers."""
        enc = Encounter(EncounterTypes.PUZZLE)
        enc.puzzle_room()

        # Check that the question and its answer are consistent
        index = enc.questions.index(enc.puzzle_question)
        self.assertEqual(enc.answers[index], enc.Riddles[enc.puzzle_question])

    def test_generate_encounter(self):
        """Asserts that generate_encounter() creates encounters of the expected type."""

        # Test boss fight
        enc = Encounter()
        enc.generate_encounter(EncounterTypes.BOSS)
        self.assertEqual(enc.encounter_type, EncounterTypes.BOSS)
        self.assertFalse(enc.is_empty)  # Boss fight is not an empty room

        # Test puzzle room
        enc = Encounter()
        enc.generate_encounter(EncounterTypes.PUZZLE)
        self.assertEqual(enc.encounter_type, EncounterTypes.PUZZLE)
        self.assertFalse(enc.is_empty)  # Puzzle room is not an empty room

        # Test empty room
        enc = Encounter()
        enc.generate_encounter(EncounterTypes.EMPTY)
        self.assertEqual(enc.encounter_type, EncounterTypes.EMPTY)
        self.assertTrue(enc.is_empty)  # Empty room is empty


if __name__ == '__main__':
    unittest.main()

