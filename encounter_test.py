import unittest
from unittest.mock import patch, MagicMock
from encounter import Encounter, EncounterTypes, ShopEncounter

class TestEncounter(unittest.TestCase):

    def test_init_with_encounter_type(self):
        # Test with provided encounter type
        encounter = Encounter(EncounterTypes.BOSS)
        self.assertEqual(encounter.encounter_type, EncounterTypes.BOSS)
        self.assertFalse(encounter.is_empty)

    def test_init_without_encounter_type(self):
        # Test without provided encounter type (random generation)
        with patch('random.randint', return_value=1):  # Simulate EMPTY room
            encounter = Encounter()
            self.assertEqual(encounter.encounter_type, EncounterTypes.EMPTY)
            self.assertTrue(encounter.is_empty)

    def test_boss_fight_monster_generation(self):
        encounter = Encounter(EncounterTypes.BOSS)
        encounter.boss_fight()
        self.assertIsNotNone(encounter.boss)
        self.assertGreater(encounter.boss.health, 0)
        self.assertIn(encounter.boss.name, encounter.Monsters)  # Assuming 'Monsters' exists in Encounter

    def test_puzzle_room_question_answer(self):
        encounter = Encounter(EncounterTypes.PUZZLE)
        encounter.puzzle_room()
        self.assertIn(encounter.puzzle_question, encounter.questions)
        self.assertEqual(encounter.Riddles[encounter.puzzle_question], encounter.answers[encounter.questions.index(encounter.puzzle_question)])

    def test_trap_room_problem_solution_door(self):
        encounter = Encounter(EncounterTypes.TRAP)
        encounter.trap_room()
        self.assertIn(encounter.trap_problem, encounter.issues)
        self.assertEqual(encounter.Problems[encounter.trap_problem], encounter.solutions[encounter.issues.index(encounter.trap_problem)])
        self.assertIsNotNone(encounter.door)

    def test_empty_room_sets_flag(self):
        encounter = Encounter(EncounterTypes.EMPTY)
        encounter.empty_room()
        self.assertTrue(encounter.is_empty)

    def test_generate_encounter_boss(self):
        encounter = Encounter()
        encounter.generate_encounter(EncounterTypes.BOSS)
        self.assertEqual(encounter.encounter_type, EncounterTypes.BOSS)
        self.assertFalse(encounter.is_empty)
        self.assertIsNotNone(encounter.boss)

    def test_generate_encounter_puzzle(self):
        encounter = Encounter()
        encounter.generate_encounter(EncounterTypes.PUZZLE)
        self.assertEqual(encounter.encounter_type, EncounterTypes.PUZZLE)
        self.assertFalse(encounter.is_empty)
        self.assertIsNotNone(encounter.puzzle_question)

    def test_generate_encounter_trap(self):
        encounter = Encounter()
        encounter.generate_encounter(EncounterTypes.TRAP)
        self.assertEqual(encounter.encounter_type, EncounterTypes.TRAP)
        self.assertFalse(encounter.is_empty)
        self.assertIsNotNone(encounter.trap_problem)
        self.assertIsNotNone(encounter.door)

    def test_generate_encounter_empty(self):
        encounter = Encounter()
        encounter.generate_encounter(EncounterTypes.EMPTY)
        self.assertEqual(encounter.encounter_type, EncounterTypes.EMPTY)
        self.assertTrue(encounter.is_empty)

    def test_generate_encounter_shop(self):
        encounter = Encounter()
        encounter.generate_encounter(EncounterTypes.SHOP)
        self.assertEqual(encounter.encounter_type, EncounterTypes.SHOP)
        self.assertFalse(encounter.is_empty)
        self.assertIsInstance(encounter.shop_encounter, ShopEncounter)

class TestShopEncounter(unittest.TestCase):
    def test_init_shop_inventory(self):
        shop_encounter = ShopEncounter()
        self.assertEqual(len(shop_encounter.shop_inventory), 3)  # Assuming 3 items in 'items.json' for SHOP
        for item in shop_encounter.shop_inventory: 
            self.assertEqual(item.type, ItemTypes.SHOP)

    def test_display_shop_inventory(self):
        shop_encounter = ShopEncounter()
        shop_inventory_string = shop_encounter.display_shop_inventory()
        # Verify the format and content of the string 
        # (adjust according to your item details)
        self.assertIn("sword (10 coins): A sharp weapon.", shop_inventory_string)
        self.assertIn("shield (5 coins): Protects you from attacks.", shop_inventory_string) 

    def test_get_item_price_found(self):
        shop_encounter = ShopEncounter()
        self.assertEqual(shop_encounter.get_item_price("sword"), 10) 

    def test_get_item_price_not_found(self):
        shop_encounter = ShopEncounter()
        self.assertIsNone(shop_encounter.get_item_price("nonexistent_item"))

if __name__ == '__main__':
    unittest.main()