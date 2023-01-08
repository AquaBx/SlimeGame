from pygame import display
from pygame import Surface
from pygame.time import Clock
from pygame_gui import UIManager

from mapeditor import config

class GameStates:
    """Application wide variables

    Members:
        should_quit (bool): Closes the game if True
        menu_open (bool): True if a pygame_gui window is open
        window (Surface): Window on which application is drawn
        ui_manager (UIManager): Manages pygame_gui stuff
        clock (Clock): Manages timings
    """

    should_quit: bool
    menu_open:   bool
    window:      Surface
    ui_manager:  UIManager
    clock:       Clock

    def init():
        GameStates.should_quit: bool = False
        GameStates.menu_open : bool = False
        GameStates.window: Surface = display.set_mode((config.WINDOW_W, config.WINDOW_H))
        GameStates.ui_manager : UIManager = UIManager((config.WINDOW_W, config.WINDOW_H))
        GameStates.clock : Clock = Clock()
