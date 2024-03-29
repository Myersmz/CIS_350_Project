import os

from character import *
from encounter import *
from room import *
from item import *
import pickle
import random
import time
from shop import *

class Game:

    def __init__(self):
        self.player = None
        self.currentRoom = None
        self.game_started = False
        self.dungeonSize = 14

    def start(self):
        self.generateRooms()
        self.createPlayer()
        self.game_started = True

    def play(self):
        while True:
            time.sleep(1)
            if not self.game_started:
                self.startMenu()
            else:
                self.enterRoom()

                choice = input("What would you like to do? (? for help): ").lower().split(" ")
                os.system('cls')

                command = choice.pop(0)
                if command == 'move':
                    match choice[0] if len(choice) > 0 else "":
                        case "west":
                            if self.currentRoom.is_dead_end(0):
                                print('There is no room west of this room.\n')
                            elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP and not self.currentRoom.encounter.is_empty:
                                print("You cannot go west because the doors to this room have shut, the doors look breakable with a sturdy hit or two")
                            else:
                                self.currentRoom = self.currentRoom.adjacentRooms[0]
                        case "north":
                            if self.currentRoom.is_dead_end(1):
                                print('There is no room north of this room.\n')
                            elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP and not self.currentRoom.encounter.is_empty:
                                print("You cannot go north because the doors to this room have shut, the doors look breakable with a sturdy hit or two")
                            else:
                                self.currentRoom = self.currentRoom.adjacentRooms[1]
                        case "east":
                            if self.currentRoom.is_dead_end(2):
                                print('There is no room east of this room.\n')
                            elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP and not self.currentRoom.encounter.is_empty:
                                print("You cannot go east because the doors to this room have shut, the doors look breakable with a sturdy hit or two")
                            else:
                                self.currentRoom = self.currentRoom.adjacentRooms[2]
                        case "south":
                            if self.currentRoom.is_dead_end(3):
                                print('There is no room south of this room.\n')
                            elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP and not self.currentRoom.encounter.is_empty:
                                print("You cannot go south because the doors to this room have shut, the doors look breakable with a sturdy hit or two")
                            else:
                                self.currentRoom = self.currentRoom.adjacentRooms[3]
                        case _:
                            print("Please enter a direction with the command.")
                elif command == '?':
                    self.printChoices()
                elif command == 'pickup':
                    pass
                elif command == 'attack':
                    if self.currentRoom.encounter.encounter_type == EncounterTypes.BOSS \
                            and not self.currentRoom.encounter.is_empty:
                        try:
                            self.currentRoom.encounter.boss.get_attacked(self.player)
                        except CharacterDeathException:
                            print(f'The {self.currentRoom.encounter.boss.name} has been slain !!!')
                            self.currentRoom.encounter.is_empty = True
                    elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP \
                              and not self.currentRoom.encounter.is_empty:
                        try:
                            self.currentRoom.encounter.door.get_attacked(self.player)
                        except CharacterDeathException:
                            print(f'The door splinters open and you are free to leave the room !!!')
                            self.currentRoom.encounter.is_empty = True
                    else:
                        print("There is no monster to attack\n")
                elif command == 'stats':
                    self.player.print_character_info()
                elif command == 'save':
                    self.save()
                elif command == 'quit':
                    user_input = input("Would you like to save before quitting?: (y for yes, n for no)").lower()
                    if user_input == 'y':
                        self.save()
                    quit()
                elif command == 'guess':
                    if self.currentRoom.encounter.encounter_type == EncounterTypes.PUZZLE \
                            and not self.currentRoom.encounter.is_empty:
                        self.puzzle_guess()
                    elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP \
                            and not self.currentRoom.encounter.is_empty:
                        self.trap_guess()
                    else:
                        print("There is no unsolved puzzle in this room\n")
                else:
                    print("\nThat is not a valid command\n")

    def puzzle_guess(self):
        user_input = input('Answer: ')
        if user_input.lower().strip() == self.currentRoom.encounter.answers[
            self.currentRoom.encounter.questions.index(self.currentRoom.encounter.puzzle_question)]:
            print('\nWell done!\n')
            self.currentRoom.encounter.is_empty = True
            # TODO: possibly add reward item
        else:
            print('\nHm, not quite.\n')

    def trap_guess(self):
        user_input = input('Solution: ')
        if user_input.lower().strip() == self.currentRoom.encounter.solutions[
            self.currentRoom.encounter.issues.index(self.currentRoom.encounter.trap_problem)]:
            print('\nThe doors quickly swing open and you are free to leave!!!\n')
            self.currentRoom.encounter.is_empty = True
        else:
            print('\nThe doors remain firmly in place, it seems that was not quite the answer.\n')

    def enterRoom(self):
        if self.currentRoom.encounter.is_empty:
            print('You encounter an empty room')
        elif self.currentRoom.encounter.encounter_type == EncounterTypes.BOSS:
            print(f'You encounter a {self.currentRoom.encounter.boss.name}')
            try:
                self.player.get_attacked(self.currentRoom.encounter.boss)
            except CharacterDeathException:
                print('\nYou have died!!!')
                self.game_started = False
                self.startMenu()

        elif self.currentRoom.encounter.encounter_type == EncounterTypes.PUZZLE:
            print(f'You encounter a puzzle room: {self.currentRoom.encounter.puzzle_question}')

        elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP:
            print(f'The doors have quickly shut, trapping you in the room.\n'
                  f'You see a puzzle that seems to be connected to the doors\n'
                  f'The puzzle could probably open them, but the doors themselves\n'
                  f'Also look like they could be broken if you attacked them enough')
            print(f'{self.currentRoom.encounter.trap_problem}')

        elif self.currentRoom.encounter.encounter_type == EncounterTypes.SHOP:
            print(f'You have encountered a mysterious shop\n')
            self.currentRoom.encounter.shop_encounter.display_shop_inventory()
            print('\nBuy - Buy items\n')

            choice = input('Enter your choice: ').lower
            os.system('cls')

            # TODO: implement buy method
            if choice == 'buy':
                print('TODO: implement shop menu/buy method')

        print(f'There are rooms to the {self.currentRoom.directions()} of this room\n')

    def printChoices(self):
        print("\nMove - move to another room")
        print('Pickup - pickup an item in a room')
        print('Attack - attack any monster in the room')
        print('Stats - print out character stats')
        print('Save - save the game')
        print('Quit - quit the game')

        if self.currentRoom.encounter.encounter_type == EncounterTypes.PUZZLE:
            print('Guess - guess in a puzzle room\n')

    def startMenu(self):
        print("\nWelcome to the Run Escape!")
        print("Press P to play")
        print("Press L to load")
        print("Press Q to quit\n")

        choice = input("Enter your choice: ").lower()
        os.system('cls')

        if choice == 'p':
            print("Starting new game...\n")
            self.start()
        elif choice == 'l':
            print("Loading game...\n")
            self.load()
        elif choice == 'q':
            print("Quitting...")
            exit()
        else:
            print("Invalid choice. Please try again.\n")

    def save(self):
        # Creates a dictionary to pickle all needed game objects. Any other needed objects are easily addable.
        print('Saving...')
        saveObject = {
            "Rooms": self.currentRoom,
            "Player": self.player
        }

        # Dumps the saveObject to the working directory of the script.
        pickle.dump(saveObject, open("savefile", "wb"))

    def load(self):
        # Loads the saveObject dictionary from a savefile-file in the working directory.
        try:
            Object = pickle.load(open("savefile", "rb"))

            # Restores the objects from the dictionary.
            self.currentRoom = Object.get("Rooms", None)
            self.player = Object.get("Player", None)
            self.game_started = True
        except FileNotFoundError:
            print("Encountered an error while loading the savefile.\n")

    def createPlayer(self):
        name = ""
        while name == "":
            name = input("Enter your name, hero: ")
        os.system('cls')

        self.player = Character(name, 25, 6, 4)

    def generateRooms(self):
        self.currentRoom = Room("Entrance")

        # gridSize = (dungeonSize + 1) % 2 + (dungeonSize * 2)
        rooms = [self.currentRoom]
        roomMap = {0: {0: self.currentRoom}}

        # Create rooms
        createdRooms = 1

        while createdRooms < self.dungeonSize:
            selectedRoom = rooms[random.randint(0, len(rooms) - 1)]
            direction = random.randint(0, 3)

            if selectedRoom.adjacentRooms[direction] is None:
                newRoom = Room("Room " + str(createdRooms))
                selectedRoom.assignRoom(newRoom, direction)
                rooms.append(newRoom)

                if roomMap.get(newRoom.position[0], None) is None:
                    roomMap[newRoom.position[0]] = {newRoom.position[1]: newRoom}
                else:
                    roomMap[newRoom.position[0]][newRoom.position[1]] = newRoom

                newRoom_position = newRoom.position

                rm = roomMap.get(newRoom_position[0] - 1, {}).get(newRoom_position[1], None)
                if rm is not None and rm != selectedRoom:
                    rm.assignRoom(newRoom, 2)
                rm = roomMap.get(newRoom_position[0], {}).get(newRoom_position[1] - 1, None)
                if rm is not None and rm != selectedRoom:
                    rm.assignRoom(newRoom, 3)
                rm = roomMap.get(newRoom_position[0] + 1, {}).get(newRoom_position[1], None)
                if rm is not None and rm != selectedRoom:
                    rm.assignRoom(newRoom, 0)
                rm = roomMap.get(newRoom_position[0], {}).get(newRoom_position[1] + 1, None)
                if rm is not None and rm != selectedRoom:
                    rm.assignRoom(newRoom, 1)
                createdRooms += 1

def main():
    # do the game
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
