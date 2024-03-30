import tkinter as tk
from tkinter import messagebox
from character import *
from encounter import *
from room import *
from item import *
import pickle
import random


class Gui():

    def __init__(self):
        self.player = None
        self.currentRoom = None
        self.game_started = False
        self.dungeonSize = 14
        self.start_menu_screen()

    def start_menu_screen(self):
        self.screen_menu = tk.Tk()
        self.screen_menu.geometry("500x500")
        self.screen_menu.title("Start Menu")
        label_intro = tk.Label(self.screen_menu, text="Welcome to Run Escape! Select an Option Below")
        label_intro.grid(row=0, padx=2, pady=2)
        button_play = tk.Button(self.screen_menu, text="Play", command=self.play)
        button_play.grid(row=1, padx=2, pady=2)
        button_load = tk.Button(self.screen_menu, text="Load", command=self.load)
        button_load.grid(row=2, padx=2, pady=2)
        button_quit = tk.Button(self.screen_menu, text="Quit", command=quit)
        button_quit.grid(row=3, padx=2, pady=2)
        self.screen_menu.mainloop()

    def play(self):
        self.character_creation_window = tk.Toplevel()
        self.character_creation_window.geometry("400x300")
        self.character_creation_window.title("Character Creation")

        label_name = tk.Label(self.character_creation_window, text="Name: ")
        label_name.grid(row=0, column=0)

        self.entry_name = tk.Entry(self.character_creation_window)
        self.entry_name.grid(row=0, column=1)

        button_enter = tk.Button(self.character_creation_window, text='Enter', command=self.get_name)
        button_enter.grid(row=1, columnspan=2)

    def get_name(self):
        self.player = Character(self.entry_name.get(), 25, 6, 4)
        self.character_creation_window.destroy()
        self.screen_menu.destroy()
        self.generateRooms()
        self.game_started = True
        self.game_screen()
        self.enterRoom()

    def load(self):
        # Loads the saveObject dictionary from a savefile-file in the working directory.
        try:
            Object = pickle.load(open("savefile", "rb"))

            # Restores the objects from the dictionary.
            self.currentRoom = Object.get("Rooms", None)
            self.player = Object.get("Player", None)
            self.game_started = True
            self.screen_menu.destroy()
            self.game_screen()
        except FileNotFoundError:
            messagebox.showerror("Error", message="Encountered an error while loading the savefile.")

    def quit(self):
        self.quit_window = tk.Toplevel()
        self.quit_window.geometry("400x300")
        self.quit_window.title("Quit Menu")
        label_quit = tk.Label(self.quit_window, text="Would you like to save before quitting?")

        label_quit.grid(row=0, column=0, columnspan=2, padx=2, pady=2)

        button_yes = tk.Button(self.quit_window, text="Yes", command=self.save_and_quit)
        button_yes.grid(row=1, column=0, padx=2, pady=2)

        button_no = tk.Button(self.quit_window, text="No", command=quit)
        button_no.grid(row=1, column=1, padx=2, pady=2)

    def save_and_quit(self):
        self.save()
        quit()

    def game_screen(self):
        self.screen_game = tk.Tk()
        self.screen_game.geometry("700x700")
        self.screen_game.title("Run Escape")

        self.label = tk.Label(self.screen_game, text="Hello World")
        self.label.grid(row=0, column=0, columnspan=8, padx=2, pady=2)

        self.label2 = tk.Label(self.screen_game, text="Hello World")
        self.label2.grid(row=1, column=0, columnspan=8, padx=2, pady=2)

        button_west = tk.Button(self.screen_game, text="West", command=self.west)
        button_west.grid(row=4, column=5, padx=2, pady=2)

        button_east = tk.Button(self.screen_game, text="East", command=self.east)
        button_east.grid(row=4, column=7, padx=2, pady=2)

        button_north = tk.Button(self.screen_game, text="North", command=self.north)
        button_north.grid(row=3, column=6, padx=2, pady=2)

        button_south = tk.Button(self.screen_game, text="South", command=self.south)
        button_south.grid(row=5, column=6, padx=2, pady=2)

        button_guess = tk.Button(self.screen_game, text="Guess", command=self.guess)
        button_guess.grid(row=4, column=2, padx=2, pady=2)

        button_attack = tk.Button(self.screen_game, text="Attack", command=self.attack)
        button_attack.grid(row=4, column=0, padx=2, pady=2)

        button_pickup = tk.Button(self.screen_game, text="Pickup", command=self.pickup)
        button_pickup.grid(row=5, column=1, padx=2, pady=2)

        button_inventory = tk.Button(self.screen_game, text="Inventory", command=self.inventory)
        button_inventory.grid(row=3, column=1, padx=2, pady=2)

        button_stats = tk.Button(self.screen_game, text="Stats", command=self.stats)
        button_stats.grid(row=3, column=3, padx=2, pady=2)

        button_menu = tk.Button(self.screen_game, text="Menu", command=self.menu)
        button_menu.grid(row=3, column=4, padx=2, pady=2)
        self.enterRoom()
        self.screen_game.mainloop()

    def west(self):
        if self.currentRoom.is_dead_end(0):
            messagebox.showerror("Error", message='There is no room west of this room.\n')
        elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP and not self.currentRoom.encounter.is_empty:
            messagebox.showerror("Error",
                                 message="You cannot go west because the doors to this room have shut, the doors look breakable with a sturdy hit or two")
        else:
            self.currentRoom = self.currentRoom.adjacentRooms[0]
            self.enterRoom()

    def north(self):
        if self.currentRoom.is_dead_end(1):
            messagebox.showerror("Error", message='There is no room north of this room.\n')
        elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP and not self.currentRoom.encounter.is_empty:
            messagebox.showerror("Error",
                                 message="You cannot go north because the doors to this room have shut, the doors look breakable with a sturdy hit or two")
        else:
            self.currentRoom = self.currentRoom.adjacentRooms[1]
            self.enterRoom()

    def east(self):
        if self.currentRoom.is_dead_end(2):
            messagebox.showerror("Error", message='There is no room east of this room.')
        elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP and not self.currentRoom.encounter.is_empty:
            messagebox.showerror("Error",
                                 message="You cannot go east because the doors to this room have shut, the doors look breakable with a sturdy hit or two")
        else:
            self.currentRoom = self.currentRoom.adjacentRooms[2]
            self.enterRoom()

    def south(self):
        if self.currentRoom.is_dead_end(3):
            messagebox.showerror("Error", message='There is no room south of this room.\n')
        elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP and not self.currentRoom.encounter.is_empty:
            messagebox.showerror("Error",
                                 message="You cannot go south because the doors to this room have shut, the doors look breakable with a sturdy hit or two")
        else:
            self.currentRoom = self.currentRoom.adjacentRooms[3]
            self.enterRoom()

    def guess_menu(self):
        self.guess_window = tk.Toplevel()
        self.guess_window.geometry("400x300")
        self.guess_window.title("Guess Menu")

        label_guess = tk.Label(self.guess_window, text="Guess: ")
        label_guess.grid(row=0, column=0)

        self.entry_input = tk.Entry(self.guess_window)
        self.entry_input.grid(row=0, column=1)
        if self.currentRoom.encounter.encounter_type == EncounterTypes.PUZZLE \
                and not self.currentRoom.encounter.is_empty:
            button_enter = tk.Button(self.guess_window, text='Enter Guess', command=self.puzzle_guess)
            button_enter.grid(row=1, columnspan=2)
        elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP \
                and not self.currentRoom.encounter.is_empty:
            button_enter = tk.Button(self.guess_window, text='Enter Guess', command=self.trap_guess)
            button_enter.grid(row=1, columnspan=2)

    def guess(self):
        if self.currentRoom.encounter.encounter_type == EncounterTypes.PUZZLE \
                and not self.currentRoom.encounter.is_empty:
            self.guess_menu()
        elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP \
                and not self.currentRoom.encounter.is_empty:
            self.guess_menu()
        else:
            messagebox.showerror("Error", message="There is no unsolved puzzle in this room\n")

    def puzzle_guess(self):
        user_input = self.entry_input.get()
        self.guess_window.destroy()
        if user_input.lower().strip() in self.currentRoom.encounter.answers:
            messagebox.showinfo('Success', message='Well done!\n')
            self.currentRoom.encounter.is_empty = True
            # TODO: possibly add reward item
        else:
            messagebox.showerror("Not Right", message='\nHm, not quite.\n')
        self.enterRoom()

    def trap_guess(self):
        user_input = self.entry_input.get()
        self.guess_window.destroy()
        if user_input.lower().strip() in self.currentRoom.encounter.solutions:
            messagebox.showinfo('Success', message='\nThe doors quickly swing open and you are free to leave!!!\n')
            self.currentRoom.encounter.is_empty = True
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

        shop_inventory_text = tk.Label(shop_window, text=self.currentRoom.encounter.shop_encounter.display_shop_inventory())
        shop_inventory_text.pack()

        # Create entry box for user input
        user_input_label = tk.Label(shop_window, text="What would you like to buy? (item, quantity)")
        user_input_label.pack()

        user_input_entry = tk.Entry(shop_window)
        user_input_entry.pack()

        # TODO: Implement 'gold' and define function to handle buying items
        def buy_item():
            pass

        # Create button to buy items
        buy_button = tk.Button(shop_window, text="Buy", command=buy_item)
        buy_button.pack()

        # Create button to exit the shop
        exit_button = tk.Button(shop_window, text="Exit", command=shop_window.destroy)
        exit_button.pack()

    def enterRoom(self):
        if self.currentRoom.encounter.is_empty:
            self.label.configure(text='You encounter an empty room')
        elif self.currentRoom.encounter.encounter_type == EncounterTypes.BOSS:
            self.label.configure(text=f'You encounter a {self.currentRoom.encounter.boss.name}')
            try:
                self.player.get_attacked(self.currentRoom.encounter.boss)
            except CharacterDeathException:
                self.game_started = False
                messagebox.showerror("Oh NO", message='\nYou have died!!!')
                self.screen_game.destroy()
                self.start_menu_screen()

        elif self.currentRoom.encounter.encounter_type == EncounterTypes.PUZZLE:
            self.label.configure(text=f'You encounter a puzzle room: {self.currentRoom.encounter.puzzle_question}')

        elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP:
            self.label.configure(text=f'The doors have quickly shut, trapping you in the room.\n' +
                                      f'You see a puzzle that seems to be connected to the doors\n' +
                                      f'The puzzle could probably open them, but the doors themselves\n' +
                                      f'Also look like they could be broken if you attacked them enough\n' +
                                      f'{self.currentRoom.encounter.trap_problem}')
            
        elif self.currentRoom.encounter.encounter_type == EncounterTypes.SHOP:
            self.label.configure(text="You have encountered a mysterious shop.")
            self.shop_window()

        self.label2.configure(text=f'\nThere are rooms to the {self.currentRoom.directions()} of this room\n')

    def attack(self):
        if self.currentRoom.encounter.encounter_type == EncounterTypes.BOSS \
                and not self.currentRoom.encounter.is_empty:
            try:
                self.currentRoom.encounter.boss.get_attacked(self.player)
            except CharacterDeathException:
                messagebox.showinfo('Success', message=f'The {self.currentRoom.encounter.boss.name} has been slain !!!')
                self.currentRoom.encounter.is_empty = True
        elif self.currentRoom.encounter.encounter_type == EncounterTypes.TRAP \
                and not self.currentRoom.encounter.is_empty:
            try:
                self.currentRoom.encounter.door.get_attacked(self.player)
            except CharacterDeathException:
                messagebox.showinfo('Success',
                                    message=f'The door splinters open and you are free to leave the room !!!')
                self.currentRoom.encounter.is_empty = True
        else:
            messagebox.showerror("Error", message="There is no monster to attack\n")
        self.enterRoom()

    def pickup(self):
        # TODO add functionality
        messagebox.showerror("Error", message='Not implemented yet')

    def inventory(self):
        self.inventory_window = tk.Toplevel()
        self.inventory_window.geometry("400x300")
        self.inventory_window.title("Inventory Menu")
        label_inventory = tk.Label(self.inventory_window, text=self.player.inventory)
        label_inventory.pack()
        # TODO add drop, equip and use buttons

    def stats(self):
        self.stats_window = tk.Toplevel()
        self.stats_window.geometry("400x300")
        self.stats_window.title("Stats Menu")
        label_stats = tk.Label(self.stats_window, text=self.player.get_character_info())
        label_stats.grid(row=0, column=0)

    def menu(self):
        self.menu_window = tk.Toplevel()
        self.menu_window.geometry("400x300")
        self.menu_window.title("Menu")

        button_save = tk.Button(self.menu_window, text='Save', command=self.save)
        button_save.grid(row=0)

        button_load = tk.Button(self.menu_window, text='Load', command=self.load)
        button_load.grid(row=1)

        button_quit = tk.Button(self.menu_window, text='Quit', command=self.quit)
        button_quit.grid(row=2)

        button_return = tk.Button(self.menu_window, text='Return to Game', command=self.menu_window.destroy)
        button_return.grid(row=3)

    def save(self):
        # Creates a dictionary to pickle all needed game objects. Any other needed objects are easily addable.
        saveObject = {
            "Rooms": self.currentRoom,
            "Player": self.player
        }

        # Dumps the saveObject to the working directory of the script.
        pickle.dump(saveObject, open("savefile", "wb"))
        messagebox.showinfo('Success', message='Save Successful')

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
                createdRooms += 1
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

        # Assign needed EncounterTypes.
        other_rooms = [rooms.pop(0)]
        for i in range(100, max_single_rooms+1):
            position = random.randint(0, len(rooms) - 1)
            rooms[position].encounter_type = EncounterTypes(i)
            other_rooms.append(rooms.pop(position))

        for room in rooms+other_rooms:
            room.initiate()


def main():
    # test gui
    g = Gui()


if __name__ == '__main__':
    main()
