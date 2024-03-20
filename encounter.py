import random
from characterClass import Character
from enum import Enum


class EncounterTypes(Enum):
    PUZZLE = 1
    BOSS = 2
    TRAP = 3
    EMPTY = 4


class Encounter:
    """
    Represents an encounter in the game, which can be a boss fight, puzzle room, or an empty room. Has methods like
    `boss_fight`, `puzzle_room`, `empty_room`, and `generate_encounter` to create different types of encounters.
    """
    def __init__(self, encounter_type=None):
        self.is_empty = True

        # movement options
        self.Options = ['yes', 'no', 'forward', 'back', 'left', 'right']

        # possible monsters
        self.Monsters = ["Demon", "Dragon", "Minotaur", "Imp", "Goblin", "Ogre", "Dwarf"]

        # questions = keys
        # answers = values
        self.Riddles = {"What has to be broken before it can be used?": "egg",
                        "I'm tall when I'm young, and I'm short when I'm old. What am I?": "candle",
                        "What month of the year has 28 days?": "all of them",
                        "What is full of holes but still holds water?": "sponge",
                        "What question can you never answer yes to?": "are you asleep"}

        # problems = keys
        # solutions = values
        self.Problems = {"What is 2+96+7?": "105",
                         "What is 5+19+3?": "27",
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

        # choose random boss from the list
        boss_name = random.choice(self.Monsters)

        # scale boss stats according to current player stats
        monster_health = random.randint(15, 25)
        monster_attack = random.randint(3, 6)
        monster_defense = random.randint(0, 4)

        # create boss object
        self.boss = Character(boss_name, monster_health, monster_attack, monster_defense)

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

    # encounterType rolls 1-4 inculsive
    def generate_encounter(self, encounter_type=None):
        if encounter_type is None:
            self.encounter_type = EncounterTypes(random.randint(1, 4))
        else:
            self.encounter_type = EncounterTypes(encounter_type)

        if self.encounter_type == EncounterTypes.BOSS:
            self.boss_fight()
        elif self.encounter_type == EncounterTypes.PUZZLE:
            self.puzzle_room()
        elif self.encounter_type == EncounterTypes.TRAP:
            self.trap_room()
        else:
            self.empty_room()
