'''

Represents a character entity in the game, which has stats such as health, attack, and defense
Also contains methods such as add_to_inventory and print character info that allows for interaction
With character aspects such as the inventory and stats

'''

class Character:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.base_attack = attack
        self.attack = attack
        self.base_defense = defense
        self.defense = defense
        self.inventory = []

    # Adds an item to inventory
    def add_to_inventory(self, item):
        self.inventory.append(item)
        self.check_inventory()

    # Takes an item from inventory
    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.check_inventory()

    # Allows for the characters stats to be changed based on items in their inventory
    def check_inventory(self):
        if "Sword" in self.inventory:
            self.attack = self.base_attack + 5
        else:
            self.attack = self.base_attack

        if "Shield" in self.inventory:
            self.defense = self.base_defense + 10
        else:
            self.defense = self.base_defense

    # Prints character information
    def print_character_info(self):
        self.check_inventory()
        print("Character Name:", self.name)
        print("Character Health:", self.health)
        print("Character Attack:", self.attack)
        print("Character Defense:", self.defense)
        print("Character Inventory:", self.inventory)

    # Causes damage from one character to another, based on their attack and defense stats.
    def take_damage(self, attacker):
        damage = max(0, attacker.attack - self.defense)
        self.health -= damage
        print(f'{attacker.name} deals {damage} damage to {self.name}')
        if self.health <= 0:
            raise(CharacterDeathException(f'{self.name} has died', self))
        else:
            print(f'{self.name} has {self.health} health left.')



class CharacterDeathException(BaseException):

    """
    Description: Exception for when a character dies handled in game.py raised in character.py
    """
    def __init__(self, st, character) -> None:
        super().__init__(st)
        self.character = character
