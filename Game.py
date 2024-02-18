from characterClass import Character
import pickle
from Room import Room
import random

class Game:

    def __init__(self):
        self.player = None
        self.currentRoom = None
        self.game_started = False

    def start(self):
        self.generateRooms()
        self.createPlayer()
        self.game_started = True

    def play(self):
        while True:
            if not self.game_started:
                self.startMenu()
                self.currentRoom.enter_room()
            elif self.currentRoom.encounter.is_empty():
                print('You encounter an empty room')
                pass

            choice = input("What would you like to do?: (enter ? for options)").lower()

            if choice == 'west':
                if(self.currentRoom.is_dead_end(1)):
                    print('There is no room west of this room.')
                else:
                    self.currentRoom = self.currentRoom.adjacentRooms[1]
            elif choice == 'north':
                if(self.currentRoom.is_dead_end(2)):
                    print('There is no room north of this room.')
                else:
                    self.currentRoom = self.currentRoom.adjacentRooms[2]
            elif choice == 'east':
                if(self.currentRoom.is_dead_end(3)):
                    print('There is no room east of this room.')
                else:
                    self.currentRoom = self.currentRoom.adjacentRooms[3]
            elif choice == 'south':
                if(self.currentRoom.is_dead_end(4)):
                    print('There is no room south of this room.')
                else:
                    self.currentRoom = self.currentRoom.adjacentRooms[4]
            elif choice == '?':
                self.printChoices()
            elif choice == 'pickup':
                pass
            elif choice == 'attack':
                pass
            elif choice == 'stats':
                pass
            elif choice == 'save':
                pass
            elif choice == 'quit':
                pass
            elif choice == 'guess':
                pass
            elif choice == 'guess':
                pass


    def printChoices():
        print('west - to go to the room to the west')       
        print('north - to go to the room to the north')      
        print('east - to go to the room to the east')      
        print('south - to go to the room to the south')      
        print('? - to get command options')   
        print('pickup - to pickup an item in a room')

    def startMenu(self):
        print("Welcome to the Run Escape!")
        print("Press P to play")
        print("Press L to load")
        print("Press Q to quit")

        choice = input("Enter your choice: ").lower()

        if choice == 'p':
            print("Starting new game...")
            self.start()
        elif choice == 'l':
            print("Loading game...")
            self.load()
        elif choice == 'q':
            print("Quitting...")
            exit()
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
                self.start()
            else:
                # Player choose to quit.
                print("Exiting..")
                exit()

    def generateRooms(self):
        self.currentRoom = Room("Entrance")

        dungeonSize = 10

        # gridSize = (dungeonSize + 1) % 2 + dungeonSize * 2
        # grid = [[]*gridSize]*gridSize
        #
        # grid[dungeonSize][dungeonSize] = self.currentRoom
        rooms = [self.currentRoom]

        # Create rooms
        createdRooms = 1

        while createdRooms < dungeonSize:
            selectedRoom = rooms[random.randint(0, len(rooms) - 1)]
            direction = random.randint(0, 3)

            if selectedRoom.adjacentRooms[direction] is None:
                newRoom = Room("Room " + str(createdRooms))
                rooms.append(newRoom)
                selectedRoom.assignRoom(newRoom, direction)
                createdRooms += 1

    def createPlayer(self):
        pass

def main():
    # do the game
    g = Game()
    g.play()

if __name__ == '__main__':
    main()
