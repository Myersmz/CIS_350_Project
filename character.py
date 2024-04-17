from item import *
from statistic import Statistic

# On load
file = open("monsters.json", "r")
monsters = json.load(file)
file.close()


class Character:
    """
    Represents a character entity in the game, which has stats such as health, attack, and defense
    Also contains methods such as add_to_inventory and print character info that allows for interaction
    With character aspects such as the inventory and stats
    """

    def __init__(self, name, health, attack, defense):
        if health <= 0 or attack < 0 or defense < 0:
            raise ValueError("Invalid argument")

        self.name = name
        self.is_player = False
        self.is_boss = False

        self.health = health
        self.base_attack = attack
        self.base_defense = defense
        self.score = 0

        self.next_defense = None
        self.next_attack = None

        self.multipliers = {
            "health": [],
            "attack": [],
            "defense": []
        }

        self.inventory = []
        self.gold = 0

        self.equipped_weapon: Item = Item("None", "", item_type=ItemTypes.MELEE, attribute_value=0)
        self.equipped_shield: Item = Item("None", "", item_type=ItemTypes.SHIELD, attribute_value=0)
        self.equipped_armour: Item = Item("None", "", item_type=ItemTypes.SHIELD, attribute_value=0)

    def assign_player(self):
        """
        Sets a flag to allow slightly different functionality of player vs monster.
        :return:
        """
        self.is_player = True
        self.equipped_weapon: Item = Item("Hands", "", item_type=ItemTypes.MELEE, attribute_value=3)

    def assign_boss(self):
        """
        Sets a flag to allow slightly different functionality of boss.
        :return:
        """
        self.is_boss = True

    def start_next_turn(self):
        """
        Resets the attack and defense values and decrements the duration of any Statistics.
        :return:
        """
        self.next_attack = None
        self.next_defense = None

        for key in self.multipliers.keys():
            for mult in self.multipliers.get(key):
                if mult.duration == 1:
                    self.multipliers[key].remove(mult)
                elif mult.duration == 0:
                    continue
                else:
                    mult.duration -= 1

    def add_to_inventory(self, item):
        """
        Adds item to the inventory, if it is gold it instead adds the value to an int var.
        :param item: Item to add [Items named "Gold" will not be added to the inventory]
        :return:
        """
        if item.name == "Gold":
            self.add_gold(item.get_attribute())
            return
        self.inventory.append(item)

    # Takes an item from inventory
    def remove_from_inventory(self, item):
        """
        Removes an item from the inventory.
        :param item: Item to remove.
        :return:
        """
        if item in self.inventory:
            self.inventory.remove(item)

    def equip_from_inventory(self, item: Item):
        """
        Equips and item from the inventory. The item must be in the inventory.
        :param item: An item from the inventory.
        :return:
        """
        if item not in self.inventory:
            raise ValueError("Item is not in my inventory")

        old_item = None
        if item.type in [ItemTypes.MELEE, ItemTypes.STAFF, ItemTypes.SPELLBOOK, ItemTypes.RANGED]:
            old_item = self.equipped_weapon
            self.equipped_weapon = item
            self.inventory.remove(item)
        elif item.type == ItemTypes.SHIELD:
            old_item = self.equipped_shield
            self.equipped_shield = item
            self.inventory.remove(item)
        elif item.type == ItemTypes.ARMOUR:
            old_item = self.equipped_armour
            self.equipped_armour = item
            self.inventory.remove(item)
        else:
            raise ValueError("Item is not equippable")

        if old_item.name not in ["None", "Hands"]:
            self.inventory.append(old_item)

    def get_character_info(self):
        return f"Character Name: {self.name}\n" \
               f"------~=====+=====~------\n" \
               f"Character Health: {self.health}\n" \
               f"Character Attack: {self.base_attack}\n" \
               f"Character Defense: {self.base_defense}\n" \
               f"Gold: {self.gold}\n" \
               f"Current Score: {self.score}\n" \
               f"Weapon: {self.equipped_weapon.name}\n" \
               f"Armour: {self.equipped_armour.name}\n" \
               f"Shield: {self.equipped_shield.name}"

    def get_attacked(self, attacker):
        """
        Takes damage from the attacker.
        :param attacker: Character
        :return:
        """
        damage = attacker.get_attack()
        defense = self.get_defense()
        attack = max(0, (damage - defense))
        self.health -= attack

        if self.health <= 0:
            if not self.is_player:
                raise CharacterDeathException(self.transfer_inventory(attacker), self)
            raise CharacterDeathException(f"", self)
        else:
            return f"Took {attack} damage"

    def transfer_inventory(self, target):
        """
        For monsters; transfers any inventory items to the target.
        :param target: Character
        :return:
        """
        item_str = "Obtained\n"

        if len(self.inventory) == 0:
            return "Obtained no items"

        while len(self.inventory) > 0:
            item = self.inventory.pop(0)
            item_str += f"{item.name}: {item.attributeValue}\n"
            target.add_to_inventory(item)
        return item_str

    def get_defense(self) -> int:
        """
        Calculates the defense value with the current conditions of the character.
        \nCalling this will calculate once per turn, and return the same value until the next turn.
        :return: Value of defense this character will apply this turn.
        """
        if self.next_defense:
            return self.next_defense

        multiplier = Statistic.get_multiplier(self.multipliers, "defense", is_monster=not self.is_player)

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

        multiplier = Statistic.get_multiplier(self.multipliers, "attack", is_monster=not self.is_player)

        strength = self.base_attack * multiplier
        strength += self.equipped_weapon.get_attribute() * multiplier

        self.next_attack = max(0, int(strength))
        return self.next_attack

    def get_gold(self) -> int:
        return self.gold

    def add_gold(self, amount: int):
        if amount <= 0:
            raise ValueError("Value \'amount\' must be a positive integer.")
        self.gold += amount

    def remove_gold(self, amount: int):
        if amount <= 0:
            raise ValueError("Value \'amount\' must be a positive integer.")
        if self.gold < amount:
            raise ValueError("Value \'amount\' cannot be greater than the value of get_gold()")

        self.gold -= amount

    def add_score(self, amount: int):
        self.score += amount

    def get_score(self) -> int:
        return self.score


class CharacterDeathException(BaseException):
    """
    Description: Exception for when a character dies handled in game.py raised in character.py
    """

    def __init__(self, st, character) -> None:
        super().__init__(st)
        self.character = character


def get_monster() -> Character:
    """
    Generates a monster from the monsters json file. Randomizes the attributes.
    :return: Character
    """
    monster_list = monsters.get("monster")

    monster = monster_list[random.randint(0, len(monster_list) - 1)]

    if type(health := monster.get("health")) == list:
        monster_health = random.randint(health[0], health[1])
    else:
        monster_health = health

    if type(attack := monster.get("attack")) == list:
        monster_attack = random.randint(attack[0], attack[1])
    else:
        monster_attack = attack

    if type(defense := monster.get("defense")) == list:
        monster_defense = random.randint(defense[0], defense[1])
    else:
        monster_defense = defense

    monster_health = int(monster_health * Statistic.get_multiplier(stat_type="health", is_monster=True))

    new_monster = Character(monster.get("name"), health=monster_health, attack=monster_attack, defense=monster_defense)

    gold_value = random.randint(0, 20)
    if gold_value != 0:
        new_monster.inventory.append(Item("Gold", description="Used to buy items at the shop",
                                          attribute_value=gold_value))
    return new_monster


def get_boss():
    """
    Generates a boss from the monsters json file. Randomizes the attributes.
    :return: Character
    """
    boss_list = monsters.get("boss")

    boss = boss_list[random.randint(0, len(boss_list) - 1)]

    if type(health := boss.get("health")) == list:
        boss_health = random.randint(health[0], health[1])
    else:
        boss_health = health

    if type(attack := boss.get("attack")) == list:
        boss_attack = random.randint(attack[0], attack[1])
    else:
        boss_attack = attack

    if type(defense := boss.get("defense")) == list:
        boss_defense = random.randint(defense[0], defense[1])
    else:
        boss_defense = defense

    boss_health = int(boss_health * Statistic.get_multiplier(stat_type="health", is_monster=True))

    new_boss = Character(boss.get("name"), health=boss_health, attack=boss_attack, defense=boss_defense)
    new_boss.assign_boss()

    gold_value = random.randint(40, 200)
    if gold_value != 0:
        new_boss.inventory.append(Item("Gold", description="Used to buy items at the shop",
                                       attribute_value=gold_value))
    return new_boss
