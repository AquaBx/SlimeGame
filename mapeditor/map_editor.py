import pygame as pg
from pygame import Rect, Vector2 as v2
from pygame import display, event
import pygame_gui

from mapeditor.config import *
from grid import Grid
from input import Input
from palette import Palette
from gui import GUI

from gamestates import GameStates

class MapEditor:

    def __init__(self) -> None:
        Input.init()

        self.palette = Palette(Rect(PALETTE_X, 0, DEFAULT_PALETTE_WIDTH, DEFAULT_PALETTE_HEIGHT))
        self.grid = Grid(Rect(0, 0, DEFAULT_GRID_WIDTH, DEFAULT_GRID_HEIGHT), DEFAULT_BACKGROUND)
        self.gui: GUI = GUI(self)

    def run(self) -> None:
        """Runs application's main loop
        """
        while not GameStates.should_quit:
            dt: float = GameStates.clock.tick(60) / 1000.0
            Input.update()

            self.__handle_events()
            self.__draw()

            GameStates.ui_manager.update(dt)

    def __handle_events(self) -> None:
        """Listens to and handles all keyboard, mouse, and button events
        """
        # Keyboard inputs
        if Input.is_pressed_once(pg.K_ESCAPE):
            if not GameStates.menu_open:
                GameStates.should_quit = True
            else:
                GameStates.menu_open = False
                [sel.kill() for sel in self.gui.file_selections.values() if not sel is None]
                [sel.kill() for sel in [self.gui.palette_tile_selection] if not sel is None]

        # ctrl shortcuts
        if Input.is_pressed(pg.K_LCTRL):
            if Input.is_pressed_once(pg.K_s):
                self.gui.save_map()
            elif Input.is_pressed_once(pg.K_l):
                self.gui.load_map()
            elif Input.is_pressed_once(pg.K_r):
                self.grid.compute_ct(self.palette)

        # handy shortcut
        if Input.is_pressed_once(pg.K_DELETE):
            self.grid.clear()
        
        # palette shortcut
        for key in range(49,58): # 1 (&) to 0 (à) keyboard buttons
            if Input.is_pressed_once(key):
                self.palette.select(key-49)

        # Mouse inputs (not gui buttons)
        if not(GameStates.menu_open):
            mouse: v2 = Input.get_mouse()

            if self.grid.is_clicked(mouse):
                if Input.is_clicked(Input.MOUSE_LEFT):
                    self.grid.put_tile(mouse, self.palette)
                elif Input.is_clicked(Input.MOUSE_RIGHT):
                    self.grid.remove_tile(mouse)

            elif self.palette.is_clicked(mouse) and Input.is_clicked_once(Input.MOUSE_LEFT):
                self.palette.handle_click(mouse)

        # Pygame events
        for e in event.get():
            if e.type == pg.QUIT:
                GameStates.should_quit = True
                
            # évènements ajoutés par nous ou pygame_gui
            elif e.type == pg.USEREVENT:
                if e.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    self.gui.detect_pressed_button(e.ui_element)
                # TODO
                # if e.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                #     if e.ui_object_id == "asset_selection.#item_list_item":
                #         pass
            GameStates.ui_manager.process_events(e)

    def __draw(self) -> None:
        """Draws application's components
        """
        GameStates.window.fill("black")

        self.grid.draw()
        self.palette.draw()
        GameStates.ui_manager.draw_ui(GameStates.window)

        display.update()
