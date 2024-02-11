from menuCode import startMenu

class Game:

    def __init__(self):
        self.player = None
        self.currentRoom = None

    def start(self):
        startMenu()

    def gameLoop(self):
        pass