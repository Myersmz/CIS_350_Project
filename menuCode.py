from characterClass import Character
import pickle

def startMenu():
    # Simple variable to check if the game is supposed to be running, if so it will change the prompt
    game_started = False
    # Initializes the player variable
    player = None

    #Loops constantly to display the menu options, if the game is supposed to be running, it will move to the second prompt
    while True:
        if not game_started:
            print("Welcome to the game!")
            print("Press p to play")
            print("Press l to load")
            print("Press Q to quit")
        else:
            print("Press 'i' to view character info, 'q' to quit")

        choice = input("Enter your choice: ").lower()

        if choice == 'p':
            if not game_started:
                print("Starting new game...")
                #Creates an example character
                player = Character(name="TestCharacter", health=100, attack=5, defense=10)
                player.add_to_inventory("Potion")
                player.add_to_inventory("Sword")
                player.add_to_inventory("Shield")
                player.add_to_inventory("Arrows")
                player.remove_from_inventory("Arrows")
                game_started = True
        elif choice == 'l':
            print("Loading game...")
            # Add code to load the game here
        elif choice == 'q':
            print("Quitting...")
            break
        elif game_started and choice in ['i', 'q']:
            # If the game has started and the choice is either 'i' or 'q', handle input using character input handling
            if choice == 'i':
                player.print_character_info()
            elif choice == 'q':
                print("Exiting program.")
                break  # Exit the program
        else:
            print("Invalid choice. Please try again.")

# Call the function to start the menu
startMenu()


def save():
    # Creates a dictionary to pickle all needed game objects. Any other needed objects are easily addable.  
    saveObject = {
        "Rooms": self.currentRoom,
        "Player": self.player
    }
    
    # Dumps the saveObject to the working directory of the script.
    pickle.dump(saveObject, open("savefile", "wb"))


def load():
    
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
            self.generateRooms()
        else:
            # Player choose to quit.
            print("Exiting..")
            exit()