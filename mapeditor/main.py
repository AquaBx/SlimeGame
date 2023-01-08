import sys
sys.path.insert(0, ".")

import pygame

from map_editor import MapEditor
from gamestates import GameStates

if __name__ == "__main__":
    """Application's launch function
    """
    
    pygame.init()

    GameStates.init()

    MapEditor().run()

    pygame.quit()

    exit(0)
