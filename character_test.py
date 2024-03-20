import unittest
from unittest.mock import patch
from io import StringIO
from character import Character, CharacterDeathException

class TestCharacter(unittest.TestCase):

    def setUp(self):
        self.character = Character("Player", 100, 10, 5)

    def test_init(self):
        self.assertEqual(self.character.name, "Player")
        self.assertEqual(self.character.health, 100)
        self.assertEqual(self.character.base_attack, 10)
        self.assertEqual(self.character.attack, 10)
        self.assertEqual(self.character.base_defense, 5)
        self.assertEqual(self.character.defense, 5)
        self.assertEqual(self.character.inventory, [])

    def test_add_to_inventory(self):
        self.character.add_to_inventory("Sword")
        self.assertIn("Sword", self.character.inventory)
        self.assertEqual(self.character.attack, 15)
        self.character.add_to_inventory("Shield")
        self.assertIn("Shield", self.character.inventory)
        self.assertEqual(self.character.defense, 15)

    def test_remove_from_inventory(self):
        self.character.add_to_inventory("Sword")
        self.character.add_to_inventory("Shield")
        self.character.remove_from_inventory("Sword")
        self.assertNotIn("Sword", self.character.inventory)
        self.assertEqual(self.character.attack, 10)
        self.character.remove_from_inventory("Shield")
        self.assertNotIn("Shield", self.character.inventory)
        self.assertEqual(self.character.defense, 5)

    def test_check_inventory(self):
        self.character.add_to_inventory("Sword")
        self.assertEqual(self.character.attack, 15)
        self.character.add_to_inventory("Shield")
        self.assertEqual(self.character.defense, 15)

    def test_print_character_info(self):
        expected_output = "Character Name: Player\nCharacter Health: 100\nCharacter Attack: 10\nCharacter Defense: 5\nCharacter Inventory: []\n"
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.character.print_character_info()
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_take_damage(self):
        def test_take_damage(self, mocked_print):
            attacker = Character("Enemy", 100, 20, 10)
            self.character.take_damage(attacker)
            mocked_print.assert_called_with("Enemy deals 10 damage to Player")
            self.assertEqual(self.character.health, 90)

    def test_take_damage_fatal(self):
        attacker = Character("Enemy", 100, 200, 10)
        with self.assertRaises(CharacterDeathException):
            self.character.take_damage(attacker)

if __name__ == '__main__':
    unittest.main()