import random
from characterClass import Character


class Encounter:
    def __init__(self, encounter_type: int = None):
        self.is_empty = True

        # movement options
        self.Options = ['yes', 'no', 'forward', 'back', 'left', 'right']

        # possible monsters
        self.Monsters = ["Demon", "Dragon", "Minotaur", "Imp", "Goblin", "Ogre", "Dwarf"]

        # questions = keys
        # answers = values
        self.Riddles = {"What has to be broken before it can be used?": "an egg",
                        "I'm tall when I'm young, and I'm short when I'm old. What am I?": "a candle",
                        "What month of the year has 28 days?": "all of them",
                        "What is full of holes but still holds water?": "a sponge",
                        "What question can you never answer yes to?": "are you asleep?"}

        # lists for Q/A's
        self.questions = list(self.Riddles.keys())
        self.answers = list(self.Riddles.values())

        self.encounter_type = encounter_type

        if encounter_type == None:
            self.generate_encounter()
        else:
            self.generate_encounter(encounter_type)

    # chooses random monster from Monsters list
    def boss_fight(self, player):
        self.is_empty = False

        # choose random boss from the list
        boss_name = random.choice(self.Monsters)

        # scale boss stats according to current player stats
        monster_health = int(player.health * 1.5)
        monster_attack = int(player.base_attack * 0.25)
        monster_defense = int(player.base_defense * 0.25)

        # create boss object
        self.boss = Character(boss_name, monster_health, monster_attack, monster_defense)

    # chooses random question
    def puzzle_room(self):
        self.puzzle_question = random.choice(self.questions)

    # TODO: possibly add random loot chance or trap?
    def empty_room(self):
        pass

    # encounterType rolls 1-3 inculsive
    def generate_encounter(self, encounter_type = random.randint(1, 3)):
        if encounter_type == 1:
            self.bossFight()
        if self.encounter_type == 2:
            self.puzzleRoom()
        else:
            self.emptyRoom()
