import random
from characterClass import Character


class Encounter:
    def __init__(self):

        self.player = None
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

    # chooses random monster from Monsters list
    def boss_fight(self):
        self.is_empty = False

        # choose random boss from the list
        boss_name = random.choice(self.Monsters)
        print(f'You encounter a {boss_name}')

        # scale boss stats according to current player stats
        monster_health = int(self.player.health * 1.5)
        monster_attack = int(self.player.base_attack * 0.25)
        monster_defense = int(self.player.base_defense * 0.25)

        # create boss object
        boss = Character(boss_name, monster_health, monster_attack, monster_defense)

        # combat methods
        def attack(self, boss):
            damage = max(0, self.player.base_attack - boss.base_defense)
            boss.health -= damage
            print(f'You deal {damage} damage to the {boss_name}')
            if boss.health <= 0:
                print(f'The {boss_name} has been defeated!')
            else:
                print(f'The {boss_name} has {boss.health} health remaining.')

        def defend(self, player):
            damage = max(0, boss.base_defense - player.base_attack)
            player.health -= damage
            print(f'The {boss_name} dealt {damage} damage to you!')
            if self.player.health <= 0:
                print(f'You have been defeated!')
            else:
                print(f'You have {self.player.health} health left.')

        # combat loop
        while True:
            user_input = input('Attack or Defend? (a/d)\n')
            if user_input.lower().strip() == 'a':
                attack(self.player, boss)
                if boss.health <= 0:
                    # boss defeated, break out of the loop
                    self.is_empty = True
                    break
                defend(self.player, boss)
            elif user_input.lower().strip() == 'd':
                defend(self.player, boss)
                if self.player.health <= 0:
                    # player defeated, break out of the loop
                    break
                attack(self.player, boss)
            else:
                print('Invalid input.')


    # chooses random question, checks for answers in the answers list. unlimited tries, or can give up.
    def puzzle_room(self):
        puzzle_question = random.choice(self.questions)
        puzzle_answers = self.answers
        user_input = ''
        print(f'You encounter a puzzle room: {puzzle_question}')
        while user_input not in puzzle_answers:
            user_input = input('answer: ')
            if user_input.lower().strip() in puzzle_answers:
                print('Well done!')
                # TODO: possibly add reward item
                break
            elif user_input.lower().strip() not in puzzle_answers:
                user_input = input('Hm, not quite. Would you like to try again? yes/no')
                if user_input.lower().strip() == 'no':
                    break

    # TODO: possibly add random loot chance or trap?
    def empty_room(self):
        print('You encounter an empty room')

        # encounterType rolls 1-3 inculsive
        def generate_encounter(self):
            encounter_type = random.randint(1, 3)
            if encounter_type == 1:
                return self.bossFight()
            if encounter_type == 2:
                return self.puzzleRoom()
            else:
                return self.emptyRoom()
