import random

from characterClass import Character
from Room import Room
import pickle


class Game:

    def __init__(self):
        self.player = None
        self.currentRoom = None
        self.game_started = False

    def start(self):
        self.generateRooms()
        print(self.currentRoom)
        self.startMenu()

    def gameLoop(self):
        pass

    def startMenu(self):

        # Loops constantly to display the menu options, if the game is supposed to be running, it will move to the second prompt
        while True:
            if not self.game_started:
                print("Welcome to the game!")
                print("Press p to play")
                print("Press l to load")
                print("Press Q to quit")
            else:
                print("Press 'i' to view character info, 'q' to quit")

            choice = input("Enter your choice: ").lower()

            if choice == 'p':
                if not self.game_started:
                    print("Starting new game...")
                    # Creates an example character
                    self.player = Character(name="TestCharacter", health=100, attack=5, defense=10)
                    self.player.add_to_inventory("Potion")
                    self.player.add_to_inventory("Sword")
                    self.player.add_to_inventory("Shield")
                    self.player.add_to_inventory("Arrows")
                    self.player.remove_from_inventory("Arrows")
                    game_started = True
            elif choice == 'l':
                print("Loading game...")
                # Add code to load the game here
            elif choice == 'q':
                print("Quitting...")
                break
            elif self.game_started and choice in ['i', 'q']:

                # If the game has started and the choice is either 'i' or 'q', handle input using character input handling
                if choice == 'i':
                    self.player.print_character_info()
                elif choice == 'q':
                    print("Exiting program.")
                    break  # Exit the program
            else:
                print("Invalid choice. Please try again.")

    def save(self):
        # Creates a dictionary to pickle all needed game objects. Any other needed objects are easily addable.
        saveObject = {
            "Rooms": self.currentRoom,
            "Player": self.player
        }

        # Dumps the saveObject to the working directory of the script.
        pickle.dump(saveObject, open("savefile", "wb"))

    def load(self):

        # Loads the saveObject dictionary from a savefile-file in the working directory.
        Object = pickle.load(open("savefile", "rb"))

        # Restores the objects from the dictionary.
        self.currentRoom = Object.get("Rooms", None)
        self.player = Object.get("Player", None)

        # Checks to see if any game objects are missing after loading from the save.
        if None in (self.currentRoom, self.player):
            print("Encountered an error while loading the savefile.")

            # Intake the player's choice to quit or start a new game.
            playerChoice = None
            while playerChoice not in ['y', 'n']:
                playerChoice = input("Do you want to start a new game? (y/n)\n").lower()

            if playerChoice == 'y':
                # Player decided to create a new game.
                # self.generateRooms()
                pass
            else:
                # Player choose to quit.
                print("Exiting..")
                exit()

    def generateRooms(self):
        self.currentRoom = Room("Entrance")

        dungeonSize = 40

        # gridSize = (dungeonSize + 1) % 2 + (dungeonSize * 2)
        rooms = [self.currentRoom]
        roomMap = {0: {0: self.currentRoom}}

        # Create rooms
        createdRooms = 1

        while createdRooms < dungeonSize:
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

        # print(len(rooms))
        # dups = 0
        # for i in range(len(rooms)):
        #     print("")
        #     for rm in rooms[i+1:]:
        #         print(rooms[i].position + rm.position)
        #         if rooms[i].position == rm.position:
        #             dups += 1
        #             print("Duplicate found")
        #
        # print("Duplicates: " + str(dups))

        #     catStr = ""
        #     for c in range(gridSize):
        #         if isinstance(grid[r][c], Room):
        #             if grid[r][c].name == "Entrance":
        #                 catStr += "E"
        #             else:
        #                 catStr += "■"
        #         else:
        #             catStr += "░"
        #     print(catStr)

    # TODO
    # Create this function to create a visible map of the rooms for debug and potentially in-game.
    # def generateMap(self):
    #     visitedRooms = []

    # def traverseMap(self, room, ):


game = Game()
game.start()
