
# currently this is just a click through menu and does nothing really still need to add all the functionality and make look pretty

import tkinter as tk

class Gui():

    def __init__(self):
        self.start_menu_screen()

    def start_menu_screen(self):
        self.screen_menu = tk.Tk()
        self.screen_menu.geometry("500x500")
        self.screen_menu.title("Start Menu")

        label_intro = tk.Label(self.screen_menu, text = "Welcome to Run Escape! Select an Option Below")
        label_intro.grid(row = 0, padx = 2, pady = 2)
        button_play = tk.Button(self.screen_menu, text = "Play", command = self.play)
        button_play.grid(row = 1, padx = 2, pady = 2)
        button_load = tk.Button(self.screen_menu, text = "Load", command = self.load)
        button_load.grid(row = 2, padx = 2, pady = 2)
        button_quit = tk.Button(self.screen_menu, text = "Quit", command = self.quit)
        button_quit.grid(row = 3, padx = 2, pady = 2)
        self.screen_menu.mainloop()

    def play(self):
        self.character_creation_window = tk.Toplevel()
        self.character_creation_window.geometry("400x300")
        self.character_creation_window.title("Character Creation")

        label_name = tk.Label(self.character_creation_window, text = "Name: ")
        label_name.grid(row = 0, column = 0)

        entry_name = tk.Entry(self.character_creation_window)
        entry_name.grid(row = 0, column = 1)

        button_enter = tk.Button(self.character_creation_window, text = 'Enter', command = self.get_name)
        button_enter.grid(row = 1, columnspan = 2)

    def get_name(self):
        self.character_creation_window.destroy()
        self.screen_menu.destroy()
        self.game_screen()


    def load(self):
        pass

    def quit(self):
        self.quit_window = tk.Toplevel()
        self.quit_window.geometry("400x300")
        self.quit_window.title("Quit Menu")
        label_quit = tk.Label(self.quit_window, text = "Would you like to save before quitting?")

        label_quit.grid(row = 0, column = 0, columnspan= 2, padx = 2, pady = 2)

        button_yes = tk.Button(self.quit_window, text = "Yes", command = quit)
        button_yes.grid(row = 1, column = 0, padx = 2, pady = 2)

        button_no = tk.Button(self.quit_window, text = "No", command = quit)
        button_no.grid(row = 1, column = 1, padx = 2, pady = 2)
        
        
    def game_screen(self):
        self.screen_game = tk.Tk()
        self.screen_game.geometry("700x700")
        self.screen_game.title("Run Escape")

        self.label = tk.Label(self.screen_game, text = "Hello World")
        self.label.grid(row = 2, column = 0, columnspan= 8, padx = 2, pady = 2)

        button_west = tk.Button(self.screen_game, text = "West", command = self.west)
        button_west.grid(row = 4, column = 5, padx = 2, pady = 2)

        button_east = tk.Button(self.screen_game, text = "East", command = self.east)
        button_east.grid(row = 4, column = 7, padx = 2, pady = 2)
        
        button_north = tk.Button(self.screen_game, text = "North", command = self.north)
        button_north.grid(row = 3, column = 6, padx = 2, pady = 2)

        button_south = tk.Button(self.screen_game, text = "South", command = self.south)
        button_south.grid(row = 5, column = 6, padx = 2, pady = 2)

        button_guess = tk.Button(self.screen_game, text = "Guess", command = self.guess) 
        button_guess.grid(row = 4, column = 2, padx = 2, pady = 2)

        button_attack = tk.Button(self.screen_game, text = "Attack", command = self.attack) 
        button_attack.grid(row = 4, column = 0, padx = 2, pady = 2)

        button_pickup = tk.Button(self.screen_game, text = "Pickup", command = self.pickup) 
        button_pickup.grid(row = 5, column = 1, padx = 2, pady = 2)

        button_inventory = tk.Button(self.screen_game, text = "Inventory", command = self.inventory) 
        button_inventory.grid(row = 3, column = 1, padx = 2, pady = 2)

        button_stats = tk.Button(self.screen_game, text = "Stats", command = self.stats) 
        button_stats.grid(row = 3, column = 3, padx = 2, pady = 2)

        button_menu = tk.Button(self.screen_game, text = "Menu", command = self.menu) 
        button_menu.grid(row = 3, column = 4, padx = 2, pady = 2)

        self.screen_game.mainloop()

    def west(self):
        self.label.configure(text = "West")

    def north(self):
        self.label.configure(text = "North")

    def east(self):
        self.label.configure(text = "East")

    def south(self):
        self.label.configure(text = "South")

    def guess(self):
        self.guess_window = tk.Toplevel()
        self.guess_window.geometry("400x300")
        self.guess_window.title("Guess Menu")

        label_guess = tk.Label(self.guess_window, text = "Guess: ")
        label_guess.grid(row = 0, column = 0)

        entry_input = tk.Entry(self.guess_window)
        entry_input.grid(row = 0, column = 1)

        button_enter = tk.Button(self.guess_window, text = 'Enter Guess', command = self.get_guess)
        button_enter.grid(row = 1, columnspan = 2)

    def attack(self):
        self.label.configure(text = "Attack")

    def pickup(self):
        self.label.configure(text = "Pickup")

    def inventory(self):
        self.inventory_window = tk.Toplevel()
        self.inventory_window.geometry("400x300")
        self.inventory_window.title("Inventory Menu")

    def stats(self):
        self.stats_window = tk.Toplevel()
        self.stats_window.geometry("400x300")
        self.stats_window.title("Stats Menu")

    def menu(self):
        self.menu_window = tk.Toplevel()
        self.menu_window.geometry("400x300")
        self.menu_window.title("Menu")

        button_save = tk.Button(self.menu_window, text = 'Save', command = self.save)
        button_save.grid(row = 0)

        button_load = tk.Button(self.menu_window, text = 'Load', command = self.load)
        button_load.grid(row = 1)

        button_quit = tk.Button(self.menu_window, text = 'Quit', command = self.quit)
        button_quit.grid(row = 2)
        
        button_return = tk.Button(self.menu_window, text = 'Return to Game', command = self.return_to_game)
        button_return.grid(row = 3)


    def get_guess(self):
        self.guess_window.destroy()
        pass

    def save(self):
        pass

    def return_to_game(self):
        self.menu_window.destroy()


def main():
    # test gui
    g = Gui()


if __name__ == '__main__':
    main()


