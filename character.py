from item import *


class Character:
    """
    Represents a character entity in the game, which has stats such as health, attack, and defense
    Also contains methods such as add_to_inventory and print character info that allows for interaction
    With character aspects such as the inventory and stats
    """
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.is_player = False

        self.health = health
        self.base_attack = attack
        self.base_defense = defense

        self.next_defense = None
        self.next_attack = None

        self.multipliers = {
            "health": [],
            "attack": [],
            "defense": []
        }

        self.floor_multipliers = {
            "health": [],
            "attack": [],
            "defense": []
        }

        self.inventory = []
        self.equipped_weapon = Item("Hands", "", item_type=ItemTypes.MELEE, attribute_value=3)
        self.equipped_shield: Item = Item("Nothing", "", ItemTypes.ITEM, attribute_value=0)
        self.equipped_armour: Item = Item("Nothing", "", ItemTypes.ITEM, attribute_value=0)

    def assign_player(self):
        """
        Sets a flag to allow slightly different functionality of player vs monster.
        :return:
        """
        self.is_player = True

    def start_next_turn(self):
        self.next_attack = None
        self.next_defense = None

    # Adds an item to inventory
    def add_to_inventory(self, item):
        self.inventory.append(item)

    # Takes an item from inventory
    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    # Prints character information
    def print_character_info(self):
        print("Character Name:", self.name)
        print("Character Health:", self.health)
        print("Character Attack:", self.base_attack)
        print("Character Defense:", self.base_defense)
        print("Character Inventory:", self.inventory)

    def get_character_info(self):
        return f"Character Name: {self.name}\nCharacter Health: {self.health}\nCharacter Attack: {self.base_attack}\nCharacter Defense: {self.base_defense}\nCharacter Inventory: {self.inventory}"
    

    # Causes damage from one character to another, based on their attack and defense stats.
    def get_attacked(self, attacker):
        damage = attacker.get_attack()
        defense = self.get_defense()
        self.health -= max(0, (damage - defense))

        if self.health <= 0:
            raise CharacterDeathException(f"Died to {attacker.name}", self)

    def get_defense(self) -> int:
        """
        Calculates the defense value with the current conditions of the character.
        \nCalling this will calculate once per turn, and return the same value until the next turn.
        :return: Value of defense this character will apply this turn.
        """
        if self.next_defense:
            return self.next_defense

        multiplier = self.get_multiplier("defense")

        strength = self.base_defense * multiplier
        strength += self.equipped_shield.get_attribute() * multiplier
        strength += self.equipped_armour.get_attribute() * multiplier

        self.next_defense = max(0, int(strength))
        return self.next_defense

    def get_attack(self) -> int:
        """
        Calculates the attack value with the current conditions of the character.
        \nCalling this will calculate once per turn, and return the same value until the next turn.
        :return:
        """
        if self.next_attack:
            return self.next_attack

        multiplier = self.get_multiplier("attack")

        strength = self.base_attack * multiplier
        strength += self.equipped_weapon.get_attribute() * multiplier

        self.next_attack = max(0, int(strength))
        return self.next_attack

    def get_multiplier(self, stat_type: str = "health") -> float:
        """
        Calculates the total Stat multiplier for a specific type of stat.
        :param stat_type: "health", "attack", "defense"
        :return:
        """
        if stat_type not in self.multipliers.keys():
            raise ValueError("Invalid multiplier type given.")

        mult = 1.0
        if not self.is_player:
            for stat in self.floor_multipliers.get(stat_type):
                mult *= stat.multiplier

        for stat in self.multipliers.get(stat_type):
            mult *= stat.multiplier
        return mult


class CharacterDeathException(BaseException):

    """
    Description: Exception for when a character dies handled in game.py raised in character.py
    """
    def __init__(self, st, character) -> None:
        super().__init__(st)
        self.character = character


class Stat:
    def __init__(self, name: str = "Mysterious Aura", multiplier: float = 1, duration: int = 0):
        self.name = name
        self.multiplier = multiplier
        self.duration = duration


if __name__ == "__main__":
    # Test code
    test = Character("Lolz", 10, 10, 10)
    test.equipped_shield = Item("Iron Shield", "debug", attribute_value=[-4, 10], item_type=ItemTypes.SHIELD)
    # # test.equipped_shield = Item("Iron Shield", "debug", attribute_value=6, item_type=ItemTypes.SHIELD)
    # test.multipliers["defense"].append(Stat(multiplier=2))
    # test.multipliers["defense"].append(Stat("Slow", multiplier=0.7))

    mon = Character("Cursed Seal", 14, 6, 7)
    mon.equipped_weapon = Item("Flipper", "", attribute_value=[2, 8], item_type=ItemTypes.MELEE)
    mon.multipliers["attack"].append(Stat("Enraged", multiplier=5))

    test.print_character_info()
    test.get_attacked(mon)
    test.print_character_info()
    # print(test.calc_defense())

