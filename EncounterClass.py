import random
class Encounter:

    def __int__(self):

        #movement options
        self.Options = ['yes', 'no', 'forward', 'back', 'left', 'right']

        #possible monsters
        self.Monsters = ["Demon", "Dragon", "Minotaur", "Imp", "Goblin", "Ogre", "Dwarf"]

        #questions = keys
        #answers = values
        self.Riddles = {"What has to be broken before it can be used?": "an egg",
                   "I'm tall when I'm young, and I'm short when I'm old. What am I?": "a candle",
                   "What month of the year has 28 days?": "all of them",
                   "What is full of holes but still holds water?": "a sponge",
                   "What question can you never answer yes to?": "are you asleep?"}

        #lists for Q/A's
        self.questions = list(self.Riddles.keys())
        self.answers = list(self.Riddles.values())

    #encounterType rolls 1-3 inculsive
    def generate_encounter(self):
        encounterType = random.randint(1, 3)
        if encounterType == 1:
            return self.bossFight()
        if encounterType == 2:
            return self.puzzleRoom()
        else:
            return self.emptyRoom()

    #chooses random monster from Monsters list
    def boss_fight(self):
        boss = random.choice(self.Monsters)
        print(f'You encounter a {boss}')

    #chooses random question, checks for answers in the answers list. unlimited tries, or can give up.
    def puzzle_room(self):
        puzzle_question = random.choice(self.questions)
        puzzle_answers = self.answers
        user_input = ''
        print(f'You encounter a puzzle room: {puzzle_question}')
        while user_input not in puzzle_answers:
            user_input = input('answer: ')
            if user_input.lower().strip() in puzzle_answers:
                print('Well done!')
                #move on from here
            elif user_input.lower().strip() not in puzzle_answers:
                user_input = input('Hm, not quite. Would you like to try again? yes/no')
                if user_input.lower().strip() == 'no':
                    break

    def empty_room(self):
        print('You encounter an empty room')