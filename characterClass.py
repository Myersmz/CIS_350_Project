class Character:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.base_attack = attack
        self.base_defense = defense
        self.inventory = []

#Currently the inventory is just a list of strings, we can change that if needed, and for now the only "functional" items are the shield and sword increasing defense and attack respectively

    #Adds an item to inventory
    def add_to_inventory(self, item):
        self.inventory.append(item)
        self.check_inventory()

    #Takes an item from inventory, prints are commented out because I was just using them to double check
    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.check_inventory()
            #print(f"{item} removed from inventory.")
        #else:
            #print(f"{item} not found in inventory.")

#Allows for the characters stats to be changed based on items in their inventory, it is called after each add, remove, and print inventory to keep things updated
    def check_inventory(self):
        if "Sword" in self.inventory:
            self.attack = self.base_attack + 5
        else:
            self.attack = self.base_attack

        if "Shield" in self.inventory:
            self.defense = self.base_defense + 10
        else:
            self.defense = self.base_defense

#Allows for the character information to be printed at any time
    def print_character_info(self):
        self.check_inventory()
        print("Character Name:", self.name)
        print("Character Health:", self.health)
        print("Character Attack:", self.attack)
        print("Character Defense:", self.defense)
        print("Character Inventory:", self.inventory)

# Allows for input to be taken from the user, for this instance I only added i to view character info and q to quit the program. It is also commented out because it was rendered obsolete from the startMenu code
#def handle_input():
    #user_input = input("Press 'i' to view character info, 'q' to quit: ")
    #if user_input.lower() == "i":
        #player.print_character_info()
    #elif user_input.lower() == "q":
        #print("Exiting program.")
        #quit()  # Exit the program
    #else:
        #print("Invalid input. Please try again.")

# Example character
#if __name__ == "__main__":
    # Create a character with initial attributes and a name
    #player = Character(name="TestCharacter", health=100, attack=5, defense=10)

    # Add items to the inventory, tests remove on Arrows
    #player.add_to_inventory("Potion")
    #player.add_to_inventory("Sword")
    #player.add_to_inventory("Shield")
    #player.add_to_inventory("Arrows")
    #player.remove_from_inventory("Arrows")

    #Continuously checks for user input
    #while True:
        #handle_input()