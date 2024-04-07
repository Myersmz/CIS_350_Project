import tkinter as tk
from tkinter import messagebox

from character import *
from floor import *
import pickle


class Gui:

    def __init__(self):
        '''
        Starts the game
        '''
        # setting variables
        self.player = None
        self.floor = None
        self.game_started = False
        self.dungeonSize = 14

        # starting the start menu screen
        self.start_menu_screen()

    def start_menu_screen(self):
        '''
        This creates and starts the start menu
        '''
        # creating the screen
        self.screen_menu = tk.Tk()
        self.screen_menu.geometry("400x300")
        self.screen_menu.title("Start Menu")
        self.screen_menu.grid_rowconfigure(0, weight=3) # label weight is higher to be bigger than the buttons
        self.screen_menu.grid_rowconfigure([1,2,3], weight=1) # buttons weight
        self.screen_menu.grid_columnconfigure(0, weight=1) # only one column
        
        # creating labels
        label_intro = tk.Label(self.screen_menu, text="Welcome to Run Escape! Select an Option Below")
        label_intro.grid(row=0, sticky="NESW")

        # creating buttons
        button_play = tk.Button(self.screen_menu, text="Play", command=self.play)
        button_play.grid(row=1, sticky="NESW")
        button_load = tk.Button(self.screen_menu, text="Load", command=self.load)
        button_load.grid(row=2, sticky="NESW")
        button_quit = tk.Button(self.screen_menu, text="Quit", command=quit)
        button_quit.grid(row=3, sticky="NESW")

        # starting the window
        self.screen_menu.mainloop()

    def play(self):
        '''
        This creates a top level menu for creating the character
        '''
        # creating the screen - Toplevel pops up without the mainloop() call
        self.character_menu = tk.Toplevel()
        self.character_menu.geometry("300x100")
        self.character_menu.title("Character Creation")
        self.character_menu.grid_rowconfigure([0,1], weight=1)
        self.character_menu.grid_columnconfigure([0,1], weight=1)

        # creating labels
        label_name = tk.Label(self.character_menu, text="Name: ")
        label_name.grid(row=0, column=0,sticky="NESW")

        # creating entries
        self.entry_name = tk.Entry(self.character_menu)
        self.entry_name.grid(row=0, column=1,sticky="NESW")

        # creating buttons
        button_enter = tk.Button(self.character_menu, text='Enter', command=self.get_name)
        button_enter.grid(row=1, columnspan=2,sticky="NESW")

        # TODO: add class or other features???

    def get_name(self):
        '''
        Creates the player character based on info from the character_menu
        '''
        # creating  player
        self.player = Character(self.entry_name.get(), 25, 6, 4)
        self.player.add_gold(25)

        # destroying the previous screens and menus
        self.character_menu.destroy()
        self.screen_menu.destroy()

        # creating the floor and starting the game menu
        self.floor = Floor()
        self.game_started = True
        self.game_screen()

    def save(self):
        '''
        Creates a dictionary to pickle all needed game objects. Any other needed objects are easily addable.
        '''
        saveObject = {
            "Floor": self.floor,
            "Player": self.player
        }

        # Dumps the saveObject to the working directory of the script.
        pickle.dump(saveObject, open("savefile", "wb"))
        messagebox.showinfo('Success', message='Save Successful')

    def load(self):
        '''
        Loads the saveObject dictionary from a savefile-file in the working directory.
        '''
        try:
            Object = pickle.load(open("savefile", "rb"))

            # Restores the objects from the dictionary.
            self.floor = Object.get("Floor", None)
            self.player = Object.get("Player", None)
            self.game_started = True

            # destroy the screen menu if it is created
            self.screen_menu.destroy()

            # start the game screen
            self.game_screen()
        except FileNotFoundError:
            messagebox.showerror("Error", message="Encountered an error while loading the savefile.")
        except tk.TclError: # loading from the game menu
            self.menu_window.destroy()
            self.enterRoom()

    def quit(self):
        '''
        This creates a top level menu for quiting and asking the user if they want to save before quiting
        '''
        # creating the screen - Toplevel pops up without the mainloop() call
        self.quit_window = tk.Toplevel()
        self.quit_window.geometry("300x100")
        self.quit_window.title("Quit Menu")
        self.quit_window.grid_rowconfigure([0,1], weight=1)
        self.quit_window.grid_columnconfigure([0,1], weight=1)

        # creating labels
        label_quit = tk.Label(self.quit_window, text="Would you like to save before quitting?")
        label_quit.grid(row=0, column=0, columnspan=2, sticky="NESW")

        # creating buttons
        button_yes = tk.Button(self.quit_window, text="Yes", command=self.save_and_quit)
        button_yes.grid(row=1, column=0, sticky="NESW")
        button_no = tk.Button(self.quit_window, text="No", command=quit)
        button_no.grid(row=1, column=1, sticky="NESW")

    def save_and_quit(self):
        '''
        Runs the save function then quits the program
        '''
        self.save()
        quit()

    def game_screen(self):
        '''
        This creates a screen for playing the game
        '''
        
        # creating the screen
        self.screen_game = tk.Tk()
        self.screen_game.geometry("700x400")
        self.screen_game.title("Run Escape")
        self.screen_game.grid_rowconfigure([2,3,4], weight=3) # buttons weight
        self.screen_game.grid_rowconfigure([0,1], weight=1) # labels weight
        self.screen_game.grid_columnconfigure([0,1,2,3,4,5,6,7], weight=1)

        # creating the labels
        self.label = tk.Label(self.screen_game, text="...")
        self.label.grid(row=0, column=0, columnspan=8, sticky="NESW")
        self.label2 = tk.Label(self.screen_game, text="...")
        self.label2.grid(row=1, column=0, columnspan=8, sticky="NESW")

        # creating the buttons
        button_west = tk.Button(self.screen_game, text="West", command=self.west)
        button_west.grid(row=3, column=5, sticky="NESW")
        button_east = tk.Button(self.screen_game, text="East", command=self.east)
        button_east.grid(row=3, column=7, sticky="NESW")
        button_north = tk.Button(self.screen_game, text="North", command=self.north)
        button_north.grid(row=2, column=6, sticky="NESW")
        button_south = tk.Button(self.screen_game, text="South", command=self.south)
        button_south.grid(row=4, column=6, sticky="NESW")
        button_guess = tk.Button(self.screen_game, text="Guess", command=self.guess)
        button_guess.grid(row=3, column=2, sticky="NESW")
        button_attack = tk.Button(self.screen_game, text="Attack", command=self.attack)
        button_attack.grid(row=3, column=0, sticky="NESW")
        button_pickup = tk.Button(self.screen_game, text="Pickup", command=self.pickup)
        button_pickup.grid(row=4, column=1, sticky="NESW")
        button_inventory = tk.Button(self.screen_game, text="Inventory", command=self.inventory)
        button_inventory.grid(row=2, column=1, sticky="NESW")
        button_stats = tk.Button(self.screen_game, text="Stats", command=self.stats)
        button_stats.grid(row=2, column=3, sticky="NESW")
        button_menu = tk.Button(self.screen_game, text="Menu", command=self.menu)
        button_menu.grid(row=2, column=4, sticky="NESW")

        # enter the room to update the labels
        self.enterRoom()

        #start the screen
        self.screen_game.mainloop()

    def boss_confirmation(self, direction: int):
        '''
        This creates a top level menu for confirming if the player wants to enter a boss room
        '''
        # creating the screen - Toplevel pops up without the mainloop() call
        boss_notice = tk.Toplevel()
        boss_notice.geometry("300x200")
        boss_notice.title("Warning")
        boss_notice.grid_rowconfigure([0,1], weight=1) 
        boss_notice.grid_columnconfigure([0,1], weight=1)

        # function for continuing entering the room
        def yes():
            boss_notice.destroy()
            self.floor.current_room = self.floor.room().adjacentRooms[direction]
            self.enterRoom()
            return

        # function for cancelling entering the room
        def no():
            boss_notice.destroy()
            return

        # creating labels
        label_name = tk.Label(boss_notice, text="The next room contains a Boss\nDo you want to continue?")
        label_name.grid(row=0, column=0, columnspan=2, sticky="NESW")

        # creating buttons
        confirm = tk.Button(boss_notice, text='Enter', command=yes)
        confirm.grid(row=1, column=0, sticky="NESW")
        turn_back = tk.Button(boss_notice, text='Turn back..', command=no)
        turn_back.grid(row=1, column=1, sticky="NESW")

    def west(self):
        '''
        This function is used for attempting to go west
        '''

        # checking for errors
        if self.floor.room().is_dead_end(0):
            messagebox.showerror("Error", message='There is no room west of this room.\n')
            return
        elif self.floor.room().encounter.encounter_type == EncounterTypes.TRAP and not self.floor.room().encounter.is_empty:
            messagebox.showerror("Error",
                                 message="You cannot go west because the doors to this room have shut, the doors look breakable with a sturdy hit or two")
            return

        next_room: Room = self.floor.room().adjacentRooms[0]
        if next_room.encounter_type == EncounterTypes.BOSS:
            if not self.boss_confirmation(0):
                return

        self.floor.current_room = next_room
        self.enterRoom()

    def north(self):
        '''
        This function is used for attempting to go north
        '''

        # checking for errors
        if self.floor.room().is_dead_end(1):
            messagebox.showerror("Error", message='There is no room north of this room.\n')
            return
        elif self.floor.room().encounter.encounter_type == EncounterTypes.TRAP and not self.floor.room().encounter.is_empty:
            messagebox.showerror("Error",
                                 message="You cannot go north because the doors to this room have shut, the doors look breakable with a sturdy hit or two")
            return

        next_room: Room = self.floor.room().adjacentRooms[1]
        if next_room.encounter_type == EncounterTypes.BOSS:
            if not self.boss_confirmation(1):
                return

        self.floor.current_room = next_room
        self.enterRoom()

    def east(self):
        '''
        This function is used for attempting to go east
        '''

        # checking for errors
        if self.floor.room().is_dead_end(2):
            messagebox.showerror("Error", message='There is no room east of this room.')
            return
        elif self.floor.room().encounter.encounter_type == EncounterTypes.TRAP and not self.floor.room().encounter.is_empty:
            messagebox.showerror("Error",
                                 message="You cannot go east because the doors to this room have shut, the doors look breakable with a sturdy hit or two")
            return

        next_room: Room = self.floor.room().adjacentRooms[2]
        if next_room.encounter_type == EncounterTypes.BOSS:
            if not self.boss_confirmation(2):
                return

        self.floor.current_room = next_room
        self.enterRoom()

    def south(self):
        '''
        This function is used for attempting to go south
        '''

        # checking for errors
        if self.floor.room().is_dead_end(3):
            messagebox.showerror("Error", message='There is no room south of this room.\n')
            return
        elif self.floor.room().encounter.encounter_type == EncounterTypes.TRAP and not self.floor.room().encounter.is_empty:
            messagebox.showerror("Error",
                                 message="You cannot go south because the doors to this room have shut, the doors look breakable with a sturdy hit or two")
            return

        next_room: Room = self.floor.room().adjacentRooms[3]
        if next_room.encounter_type == EncounterTypes.BOSS:
            if not self.boss_confirmation(3):
                return

        self.floor.current_room = next_room
        self.enterRoom()

    def guess_menu(self):
        '''
        This creates a top level menu for attempting to guess a riddle or puzzle
        '''

        # creating the screen - Toplevel pops up without the mainloop() call
        self.guess_window = tk.Toplevel()
        self.guess_window.geometry("300x100")
        self.guess_window.title("Guess Menu")
        self.guess_window.grid_rowconfigure([0,1], weight=1) 
        self.guess_window.grid_columnconfigure([0,1], weight=1)

        # creating labels
        label_guess = tk.Label(self.guess_window, text="Guess: ")
        label_guess.grid(row=0, column=0, sticky="NESW")

        # creating entries
        self.entry_input = tk.Entry(self.guess_window)
        self.entry_input.grid(row=0, column=1, sticky="NESW")

        # creating button with command base don what type of room we are in 
        if self.floor.room().encounter.encounter_type == EncounterTypes.PUZZLE \
                and not self.floor.room().encounter.is_empty:
            button_enter = tk.Button(self.guess_window, text='Enter Guess', command=self.puzzle_guess)
            button_enter.grid(row=1, column=0, columnspan=2, sticky="NESW")
        elif self.floor.room().encounter.encounter_type == EncounterTypes.TRAP \
                and not self.floor.room().encounter.is_empty:
            button_enter = tk.Button(self.guess_window, text='Enter Guess', command=self.trap_guess)
            button_enter.grid(row=1, column=0, columnspan=2, sticky="NESW")

    def guess(self):
        '''
        This either opens the guess menu or shows an error based on the type of room the player is in at the time
        '''
        if self.floor.room().encounter.encounter_type == EncounterTypes.PUZZLE \
                and not self.floor.room().encounter.is_empty:
            self.guess_menu()
        elif self.floor.room().encounter.encounter_type == EncounterTypes.TRAP \
                and not self.floor.room().encounter.is_empty:
            self.guess_menu()
        else:
            messagebox.showerror("Error", message="There is no unsolved puzzle in this room\n")

    def puzzle_guess(self):
        '''
        This function is for guessing if the player is in a puzzle room
        '''
        user_input = self.entry_input.get()
        self.guess_window.destroy()
        if user_input.lower().strip() in self.floor.room().encounter.answers:
            messagebox.showinfo('Success', message='Well done!\n')
            self.floor.room().encounter.is_empty = True
            # TODO: possibly add reward item
        else:
            messagebox.showerror("Not Right", message='\nHm, not quite.\n')
        self.enterRoom()

    def trap_guess(self):
        '''
        This function is for guessing if the player is in a trap room
        '''
        user_input = self.entry_input.get()
        self.guess_window.destroy()
        if user_input.lower().strip() in self.floor.room().encounter.solutions:
            messagebox.showinfo('Success', message='\nThe doors quickly swing open and you are free to leave!!!\n')
            self.floor.room().encounter.is_empty = True
        else:
            messagebox.showerror("Not Right",
                                 message='\nThe doors remain firmly in place, it seems that was not quite the answer.\n')
        self.enterRoom()

    def shop_window(self):
        # Create a new window for the shop
        shop_window = tk.Toplevel(self.screen_game)
        shop_window.title("Shop")

        # Display shop message
        shop_label = tk.Label(shop_window, text="Welcome to the shop.")
        shop_label.pack()

        # Display shop inventory
        shop_inventory_text = tk.Label(shop_window, text=self.floor.room().encounter.shop_encounter.display_shop_inventory())
        shop_inventory_text.pack()

        # Dropdown for item selection
        item_options = self.floor.room().encounter.shop_encounter.display_items()
        selected_item = tk.StringVar(shop_window)
        selected_item.set(item_options[0])

        item_dropdown = tk.OptionMenu(shop_window, selected_item, *item_options)
        item_dropdown.pack()

        # Dropdown for quantity selection
        quantity_options = [str(i) for i in range(1, 11)]
        selected_quantity = tk.StringVar(shop_window)
        selected_quantity.set(quantity_options[0])

        quantity_dropdown = tk.OptionMenu(shop_window, selected_quantity, *quantity_options)
        quantity_dropdown.pack()
        
        def buy_items():
            selected_item_name = selected_item.get()  # Retrieve selected item name
            quantity = int(selected_quantity.get())  # Retrieve selected quantity
            total_cost = quantity * 10

            # Check if the player has enough gold
            total_cost = quantity * 10
            if self.player.get_gold() < total_cost:
                messagebox.showerror("Error", "You don't have enough gold to purchase these items.")
                return

            # Remove gold from the player
            self.player.remove_gold(total_cost)

            # Add items to the player's inventory
            for _ in range(quantity):
                for item in self.floor.room().encounter.shop_encounter.shop_inventory:
                    if item.name == selected_item_name:
                        self.player.add_to_inventory(item)
                        break  # Exit the inner loop once the item is found

            # Inform the player about the purchase
            messagebox.showinfo("Success", f"You purchased {quantity} {selected_item_name}(s).")
                # Create button to buy items
            
        buy_button = tk.Button(shop_window, text="Buy", command=buy_items)
        buy_button.pack()

        # Create button to exit the shop
        exit_button = tk.Button(shop_window, text="Exit", command=shop_window.destroy)
        exit_button.pack()

    def enterRoom(self):
        '''
        This function is for entering the room and updates the labels of the game screen
        '''
        if self.floor.room().encounter.is_empty:
            self.label.configure(text='You encounter an empty room')
        elif self.floor.room().encounter.encounter_type == EncounterTypes.BOSS:
            self.label.configure(text=f'You encounter a {self.floor.room().encounter.boss.name}')
            try:
                self.player.get_attacked(self.floor.room().encounter.boss)
            except CharacterDeathException:
                self.game_started = False
                messagebox.showerror("Oh NO", message='\nYou have died!!!')
                self.screen_game.destroy()
                self.start_menu_screen()

        elif self.floor.room().encounter.encounter_type == EncounterTypes.PUZZLE:
            self.label.configure(text=f'You encounter a puzzle room: {self.floor.room().encounter.puzzle_question}')

        elif self.floor.room().encounter.encounter_type == EncounterTypes.TRAP:
            self.label.configure(text=f'The doors have quickly shut, trapping you in the room.\n' +
                                      f'You see a puzzle that seems to be connected to the doors\n' +
                                      f'The puzzle could probably open them, but the doors themselves\n' +
                                      f'Also look like they could be broken if you attacked them enough\n' +
                                      f'{self.floor.room().encounter.trap_problem}')
            
        elif self.floor.room().encounter.encounter_type == EncounterTypes.SHOP:
            self.label.configure(text="You have encountered a mysterious shop.")
            self.shop_window()

        self.label2.configure(text=f'\nThere are rooms to the {self.floor.room().directions()} of this room\n')

    def attack(self):
        if self.floor.room().encounter.encounter_type == EncounterTypes.BOSS \
                and not self.floor.room().encounter.is_empty:
            try:
                self.floor.room().encounter.boss.get_attacked(self.player)
            except CharacterDeathException:
                messagebox.showinfo('Success', message=f'The {self.floor.room().encounter.boss.name} has been slain !!!')
                self.floor.room().encounter.is_empty = True
        elif self.floor.room().encounter.encounter_type == EncounterTypes.TRAP \
                and not self.floor.room().encounter.is_empty:
            try:
                self.floor.room().encounter.door.get_attacked(self.player)
            except CharacterDeathException:
                messagebox.showinfo('Success',
                                    message=f'The door splinters open and you are free to leave the room !!!')
                self.floor.room().encounter.is_empty = True
        else:
            messagebox.showerror("Error", message="There is no monster to attack\n")
        self.enterRoom()

    def pickup(self):
        item_list = self.floor.room().items

        # In progress
        #
        # if len(item_list) == 0:
        #     messagebox.showerror("Pickup", message="The room is empty...")
        #     return
        #
        # item_pickup_menu = tk.Toplevel()
        # item_pickup_menu.geometry("200x400")
        # item_pickup_menu.title("Pickup")
        #
        # label = tk.Label(item_pickup_menu, text="Pickup what?")
        # label.pack()
        #
        # self.pickup_item_buttons = []
        #
        # i = 0
        # pack = []
        # for item in item_list:
        #     attribute_name = ""
        #     match item.type:
        #         case ItemTypes.MELEE, ItemTypes.RANGED, ItemTypes.SPELLBOOK, ItemTypes.STAFF:
        #             attribute_name = " attack"
        #         case ItemTypes.SHIELD, ItemTypes.ARMOUR:
        #             attribute_name = " defense"
        #         case default:
        #             pass
        #
        #     pack.append({"index": i, "item": item})
        #     button = tk.Button(item_pickup_menu, text=f"{item.name}: {item.attributeValue}{attribute_name}",
        #                        command=lambda: self.pickup_item(pack[i]))
        #     self.pickup_item_buttons.append(button)
        #     button.pack()
        #     i += 1
        # i+=20

    def inventory(self):
        '''
        This creates a top level menu for showing the stats of the player
        '''

        # creating the screen - Toplevel pops up without the mainloop() call
        self.inventory_window = tk.Toplevel()
        self.inventory_window.geometry("400x300")
        self.inventory_window.title("Inventory Menu")
        #self.inventory_window.grid_rowconfigure([0,1], weight=1) # labels weight
        #self.inventory_window.grid_columnconfigure([0,1,2,3,4,5,6,7], weight=1)

        label_inventory = tk.Label(self.inventory_window, text=self.player.inventory)
        label_inventory.grid(row=0, column=0, sticky="NESW")
        # TODO add each item as a radio button option to use the other buttons

        # TODO add drop, equip and use buttons

    def stats(self):
        '''
        This creates a top level menu for showing the stats of the player
        '''

        # creating the screen - Toplevel pops up without the mainloop() call
        self.stats_window = tk.Toplevel()
        self.stats_window.geometry("250x250")
        self.stats_window.title("Stats Menu")
        self.stats_window.grid_rowconfigure(0, weight=1) 
        self.stats_window.grid_columnconfigure(0, weight=1)

        # creating labels
        label_stats = tk.Label(self.stats_window, text=self.player.get_character_info())
        label_stats.grid(row=0, column=0, sticky="NESW")

    def menu(self):
        '''
        This creates a top level menu for showing the game menu
        '''

        # creating the screen - Toplevel pops up without the mainloop() call
        self.menu_window = tk.Toplevel()
        self.menu_window.geometry("250x250")
        self.menu_window.title("Menu")
        self.menu_window.grid_rowconfigure([0,1,2,3], weight=1) 
        self.menu_window.grid_columnconfigure(0, weight=1)

        # creating the buttons
        button_save = tk.Button(self.menu_window, text='Save', command=self.save)
        button_save.grid(row=0, sticky="NESW")
        button_load = tk.Button(self.menu_window, text='Load', command=self.load)
        button_load.grid(row=1, sticky="NESW")
        button_quit = tk.Button(self.menu_window, text='Quit', command=self.quit)
        button_quit.grid(row=2, sticky="NESW")
        button_return = tk.Button(self.menu_window, text='Return to Game', command=self.menu_window.destroy)
        button_return.grid(row=3, sticky="NESW")


def main():
    # test gui
    g = Gui()


if __name__ == '__main__':
    main()
