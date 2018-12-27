"""
The primary application script for Alien Invaders
"""
from consts import *
from app import *

if __name__ == '__main__':
    Invaders(width=GAME_WIDTH,height=GAME_HEIGHT).run()
