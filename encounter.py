import random
import character
from character import Character
from enum import Enum
from shop import ShopEncounter
from item import *

# The largest value of the "safe to generate" EncounterTypes
max_generation_rooms = 3
# The largest value of the EncounterTypes that must have a single room
max_single_rooms = 101


class EncounterTypes(Enum):
    EMPTY = 1
    PUZZLE = 2
    TRAP = 3
    BOSS = 100
    SHOP = 101


class Encounter:
    """
    Represents an encounter in the game, which can be a boss fight, puzzle room, or an empty room. Has methods like
    `boss_fight`, `puzzle_room`, `empty_room`, and `generate_encounter` to create different types of encounters.
    """
    def __init__(self, encounter_type=None):
        self.is_empty = True

        # questions = keys
        # answers = values
        self.Riddles = {"What has to be broken before it can be used?": "egg",
                        "I'm tall when I'm young, and I'm short when I'm old. What am I?": "candle",
                        "What month of the year has 28 days?": "all of them",
                        "What is full of holes but still holds water?": "sponge",
                        "What question can you never answer yes to?": "are you asleep"}

        # problems = keys
        # solutions = values
        self.Problems = {"What is 2 + 96 + 7?": "105",
                         "What is 5 + 19 + 3?": "27",
                         "What is 3 + 9 + 45?": "57",
                         "What is 8 + 2 + 18?": "28",
                         "What is 5 + 6 + 23?": "34"}

        # lists for Q/A's
        self.questions = list(self.Riddles.keys())
        self.answers = list(self.Riddles.values())

        # lists for Trap Problems
        self.issues = list(self.Problems.keys())
        self.solutions = list(self.Problems.values())

        self.puzzle_question = None
        self.boss = None
        self.encounter_type = None
        self.door = None
        self.generate_encounter(encounter_type)

    # chooses random monster from Monsters list
    def boss_fight(self):
        self.is_empty = False

        # create boss object
        self.boss = character.get_boss()

    # chooses random question
    def puzzle_room(self):
        self.is_empty = False
        self.puzzle_question = random.choice(self.questions)

    # chooses random math problem
    def trap_room(self):
        self.is_empty = False
        self.trap_problem = random.choice(self.issues)

        # creates door object to be broken open
        self.door = Character('Door', 15, 0, 0)

    # TODO: possibly add random loot chance or trap?
    def empty_room(self):
        self.is_empty = True

    def generate_encounter(self, encounter_type=None):
        print('generating encounter...')
        if encounter_type is None:
            self.encounter_type = EncounterTypes(random.randint(1, max_generation_rooms))
        else:
            print('else')
            self.encounter_type = EncounterTypes(encounter_type)

        if self.encounter_type == EncounterTypes.BOSS:
            print('boss')
            self.boss_fight()
        elif self.encounter_type == EncounterTypes.PUZZLE:
            print('puzzle')
            self.puzzle_room()
        elif self.encounter_type == EncounterTypes.TRAP:
            print('trap')
            self.trap_room()
        elif self.encounter_type == EncounterTypes.SHOP:
            self.is_empty = False
            self.shop_encounter = ShopEncounter()
            print('You have encountered a shop!')
        else:
            print('else empty room')
            self.empty_room()
    
class ShopEncounter(Encounter):
    def __init__(self):
        super().__init__()  # Call the parent class's constructor

        # Load shop inventory from items.json
        with open("items.json", "r") as file:
            items = json.load(file)
            self.shop_inventory = [Item(name=item['NAME'], description=item['DESCRIPTION']) for item in items.get("CONSUMABLES", [])]

    def display_shop_inventory(self):
        for item in self.shop_inventory:
            print(f"{item.name} ({item.price} coins): {item.description}")

    def buy_item(self, player, item_name):
        for item in self.shop_inventory:
            if item.name == item_name:
                if player.currency >= item.price:
                    player.currency -= item.price
                    player.inventory.append(item)
                    print(f"You purchased {item.name}!")
                    return True
                else:
                    print("You don't have enough coins.")
                    return False
        print("Item not found in the shop.")
        return False
