import unittest
from unittest.mock import patch
from io import StringIO

import character
from character import Character, CharacterDeathException
from item import Item, ItemTypes
from statistic import Statistic


class CharacterTest(unittest.TestCase):

    def setUp(self):
        self.character = Character("Player", 25, 10, 5)
        self.character.assign_player()

    def test_init(self):
        self.assertEqual(self.character.name, "Player")
        self.assertEqual(self.character.health, 25)
        self.assertEqual(self.character.base_attack, 10)
        self.assertEqual(self.character.base_defense, 5)
        self.assertEqual(self.character.inventory, [])
        self.assertTrue(self.character.is_player)
        self.assertEqual(self.character.score, 0)
        self.assertEqual(self.character.equipped_weapon.name, "Hands")
        self.assertEqual(self.character.equipped_armour.name, "None")
        self.assertEqual(self.character.equipped_shield.name, "None")
        self.assertEqual(self.character.gold, 0)
        self.assertEqual(self.character.multipliers, {"attack": [], "defense": [], "health": []})

    def test_init_invalid_health(self):
        self.assertRaises(ValueError, Character, "test", 0, 10, 10)

    def test_init_invalid_attack(self):
        self.assertRaises(ValueError, Character, "test", 10, -1, 10)

    def test_init_invalid_defense(self):
        self.assertRaises(ValueError, Character, "test", 10, 10, -1)

    def test_start_next_turn(self):
        buff = Statistic("Aura", multiplier=2, duration=2)
        self.character.multipliers["attack"].append(buff)
        self.assertEqual(self.character.get_attack(), 26)

        self.character.start_next_turn()

        self.assertEqual(self.character.next_defense, None)
        self.assertEqual(self.character.next_attack, None)
        self.assertEqual(self.character.multipliers.get("attack")[0].duration, 1)

    def test_start_next_turn_remove_stat(self):
        buff = Statistic("Aura", multiplier=2, duration=1)
        self.character.multipliers["attack"].append(buff)
        self.assertEqual(self.character.get_attack(), 26)

        self.character.start_next_turn()

        self.assertEqual(self.character.next_defense, None)
        self.assertEqual(self.character.next_attack, None)
        self.assertEqual(len(self.character.multipliers.get("attack")), 0)

    def test_start_next_turn_indefinite_stat(self):
        buff = Statistic("Aura", multiplier=2, duration=0)
        self.character.multipliers["attack"].append(buff)
        self.assertEqual(self.character.get_attack(), 26)

        self.character.start_next_turn()

        self.assertEqual(self.character.next_defense, None)
        self.assertEqual(self.character.next_attack, None)
        self.assertEqual(self.character.multipliers.get("attack")[0].duration, 0)

    def test_add_to_inventory(self):
        item = Item()
        item.generateItem()
        self.character.add_to_inventory(item)

        self.assertTrue(item in self.character.inventory)

    def test_add_to_inventory_gold(self):
        item = Item("Gold", attribute_value=100)
        self.character.add_to_inventory(item)
        self.assertEqual(self.character.gold, 100)

    def test_remove_from_inventory(self):
        item = Item()
        item.generateItem()
        self.character.add_to_inventory(item)

        self.assertEqual(len(self.character.inventory), 1)
        self.character.remove_from_inventory(item)
        self.assertEqual(len(self.character.inventory), 0)

    def test_equip_from_inventory_weapon(self):
        item = Item()
        item.generateItem(item_type=ItemTypes.MELEE)
        self.character.add_to_inventory(item)
        self.character.equip_from_inventory(item)

        self.assertEqual(len(self.character.inventory), 0)
        self.assertEqual(self.character.equipped_weapon, item)

    def test_equip_from_inventory_armour(self):
        item = Item()
        item.generateItem(item_type=ItemTypes.ARMOUR)
        self.character.add_to_inventory(item)
        self.character.equip_from_inventory(item)

        self.assertEqual(len(self.character.inventory), 0)
        self.assertEqual(self.character.equipped_armour, item)

    def test_equip_from_inventory_shield(self):
        item = Item()
        item.generateItem(item_type=ItemTypes.SHIELD)
        self.character.add_to_inventory(item)
        self.character.equip_from_inventory(item)

        self.assertEqual(len(self.character.inventory), 0)
        self.assertEqual(self.character.equipped_shield, item)

    def test_equip_from_inventory_swap(self):
        item = Item()
        item.generateItem(ItemTypes.MELEE)
        self.character.add_to_inventory(item)
        self.character.equip_from_inventory(item)

        item2 = Item()
        item2.generateItem(ItemTypes.MELEE)
        self.character.add_to_inventory(item2)
        self.character.equip_from_inventory(item2)

        self.assertEqual(self.character.equipped_weapon, item2)
        self.assertEqual(self.character.inventory[0], item)

    def test_equip_from_inventory_not_equippable(self):
        item = Item()
        item.generateItem(item_type=ItemTypes.POTION)
        self.character.add_to_inventory(item)
        self.assertRaises(ValueError, self.character.equip_from_inventory, item)

    def test_equip_from_inventory_invalid(self):
        item = Item()
        item.generateItem(item_type=ItemTypes.MELEE)
        self.character.add_to_inventory(item)

        item_2 = Item()
        item_2.generateItem()
        self.assertRaises(ValueError, self.character.equip_from_inventory, item_2)

    def test_get_character_info(self):
        # Needs to be changed still...
        
        Stringvalue = f"Character Name: {self.character.name}\n" \
               f"------~=====+=====~------\n" \
               f"Character Health: {self.character.health}\n" \
               f"Character Attack: {self.character.base_attack}\n" \
               f"Character Defense: {self.character.base_defense}\n" \
               f"Gold: {self.character.gold}\n" \
               f"Current Score: {self.character.score}\n" \
               f"Weapon: {self.character.equipped_weapon.name}\n" \
               f"Armour: {self.character.equipped_armour.name}\n" \
               f"Shield: {self.character.equipped_shield.name}"
        
        self.assertEqual(self.character.get_character_info(), Stringvalue)

    def test_get_attacked(self):
        attacker = Character("Enemy", 10, 10, 0)
        attack = self.character.get_attacked(attacker)

        self.assertEqual(attack, "Took 5 damage")
        self.assertEqual(self.character.health, 20)

    def test_get_attacked_enemy(self):
        enemy = Character("Enemy", 5, 0, 0)
        item = Item(item_type=ItemTypes.POTION)
        enemy.add_to_inventory(item)
        self.assertRaises(CharacterDeathException, enemy.get_attacked, self.character)
        self.assertEqual(self.character.inventory[0], item)

    def test_transfer_inventory(self):
        enemy = Character("Enemy", 5, 0, 0)
        item = Item(item_type=ItemTypes.POTION)
        enemy.add_to_inventory(item)
        enemy.transfer_inventory(self.character)
        self.assertEqual(self.character.inventory[0], item)

    def test_transfer_inventory_zero(self):
        enemy = Character("Enemy", 5, 0, 0)
        result = enemy.transfer_inventory(self.character)
        self.assertEqual(result, "Obtained no items")

    def test_get_defense(self):
        self.assertEqual(self.character.get_defense(), 5)

    def test_get_defense1(self):
        self.character.get_defense()
        self.assertEqual(self.character.get_defense(), 5)

    def test_get_defense_multiplier(self):
        buff = Statistic("Aura", multiplier=2)
        self.character.multipliers["defense"].append(buff)
        self.assertEqual(self.character.get_defense(), 10)

    def test_get_attack(self):
        self.assertEqual(self.character.get_attack(), 13)

    def test_get_attack1(self):
        self.character.get_attack()
        self.assertEqual(self.character.get_attack(), 13)

    def test_get_attack_multiplier(self):
        buff = Statistic("Aura", multiplier=2)
        self.character.multipliers["attack"].append(buff)
        self.assertEqual(self.character.get_attack(), 26)

    def test_get_gold(self):
        item = Item("Gold", attribute_value=50)
        self.character.add_to_inventory(item)
        self.assertEqual(self.character.get_gold(), 50)

    def test_add_gold(self):
        self.character.add_gold(100)
        self.assertEqual(self.character.get_gold(), 100)

    def test_add_gold_invalid(self):
        self.assertRaises(ValueError, self.character.add_gold, -10)

    def test_remove_gold(self):
        self.character.add_gold(50)
        self.character.remove_gold(20)
        self.assertEqual(self.character.get_gold(), 30)

    def test_remove_gold_invalid_negative(self):
        self.character.add_gold(50)
        self.assertRaises(ValueError, self.character.remove_gold, -10)

    def test_remove_gold_invalid_not_enough(self):
        self.character.add_gold(50)
        self.assertRaises(ValueError, self.character.remove_gold, 80)

    def test_add_score(self):
        self.character.add_score(50)
        self.assertEqual(self.character.score, 50)

    def test_get_score(self):
        self.character.add_score(60)
        self.assertEqual(self.character.get_score(), 60)

    # def test_print_character_info(self):
    #     expected_output = "Character Name: Player\n" \
    #                       "Character Health: 100\n" \
    #                       "Character Attack: 10\nCharacter Defense: 5\nCharacter Inventory: []\n"
    #     with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
    #         self.character.print_character_info()
    #         self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_take_damage(self):
        def test_take_damage(self, mocked_print):
            attacker = Character("Enemy", 100, 20, 10)
            self.character.take_damage(attacker)
            mocked_print.assert_called_with("Enemy deals 10 damage to Player")
            self.assertEqual(self.character.health, 90)

    def test_take_damage_fatal(self):
        attacker = Character("Enemy", 100, 200, 10)
        with self.assertRaises(CharacterDeathException):
            self.character.get_attacked(attacker)

    def test_get_monster(self):
        monster = character.get_monster()

        self.assertNotEqual(monster.health, None)
        self.assertNotEqual(monster.base_attack, None)
        self.assertNotEqual(monster.base_defense, None)
        self.assertNotEqual(monster.inventory, None)
        self.assertFalse(monster.is_player)
        self.assertEqual(monster.score, 0)
        self.assertEqual(monster.equipped_weapon.name, "None")
        self.assertEqual(monster.equipped_armour.name, "None")
        self.assertEqual(monster.equipped_shield.name, "None")
        self.assertNotEqual(monster.gold, None)
        self.assertEqual(monster.multipliers, {"attack": [], "defense": [], "health": []})

    def test_get_boss(self):
        monster = character.get_boss()

        self.assertNotEqual(monster.health, None)
        self.assertNotEqual(monster.base_attack, None)
        self.assertNotEqual(monster.base_defense, None)
        self.assertNotEqual(monster.inventory, None)
        self.assertFalse(monster.is_player)
        self.assertEqual(monster.score, 0)
        self.assertEqual(monster.equipped_weapon.name, "None")
        self.assertEqual(monster.equipped_armour.name, "None")
        self.assertEqual(monster.equipped_shield.name, "None")
        self.assertNotEqual(monster.gold, None)
        self.assertEqual(monster.multipliers, {"attack": [], "defense": [], "health": []})


if __name__ == '__main__':
    unittest.main()