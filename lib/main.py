'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''
import header
from engine import Engine
from states import *

def main():
    app = Engine(SplashState(), fullscreen = True)
    app.run()
