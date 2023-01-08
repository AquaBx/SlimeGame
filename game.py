from menu_screen import Menu

import pygame as pg
from pygame.time import Clock

from config import GameConfig, GameState
from input import Input
from text import Text
from world import World
from assets.spritesheet import SpritesheetManager
import threading

from eventlistener import EventManager
from buttons import ButtonManager
from Gui import Gui

class Game:
    def __init__(self) -> None:
        pg.init()
        GameState.initialize()
        Input.init()
        Text.init(GameState.WINDOW, GameConfig.FONT_DATA, GameConfig.FONT_SIZE)
        ButtonManager.init(GameState.WINDOW)
        SpritesheetManager.initialize()
        EventManager.initialize(["player_action"])
        Menu.init(self)

        self.clock: Clock = Clock()
        self.should_quit: bool = False

        # il faudra donner un entier qui correspond au fichier de sauvegarde demandé (1, 2 ou 3 sans doute)
        self.world: World = World()
        self.paused = False

    def __del__(self) -> None:
        pg.quit()

    def loop(self) -> None:
        physique = threading.Thread ( target = self.__update )
        physique.start()
        while not self.should_quit:
            Input.update()

            self.__process_events()

            if not self.paused:
                GameState.graphicDT = 1 / self.clock.get_fps() if self.clock.get_fps() != 0 else 1 / GameConfig.Graphics.MaxFPS
                GameState.GAME_SURFACE.fill('Black')
                self.__draw()

            EventManager.flush()
            ButtonManager.update()
            pg.display.update()
            self.clock.tick(GameConfig.Graphics.MaxFPS)

    def __process_events(self) -> None:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                self.should_quit = True
        if Input.is_pressed_once(pg.K_ESCAPE):
            if self.paused:
                self.paused = False
                Menu.close_menu("ingame_pause")
            else:
                self.paused = True
                Menu.open_menu("ingame_pause")


    def __update(self) -> None:
        clock = Clock()
        while not self.should_quit:
            if not self.paused:
                self.world.update()
            GameState.physicDT = 1. / (clock.get_fps() + (clock.get_fps() == 0.) * GameConfig.PhysicTick)
            clock.tick(GameConfig.PhysicTick)
        

    def __draw(self) -> None:
        self.world.draw()
        Gui.draw(GameState().GAME_SURFACE)
        
        """ blit fenetre """
        # upscale sur la taille de la fenetre
        GameState.WINDOW.blit(pg.transform.scale(GameState.GAME_SURFACE, GameState.WINDOW.get_size()),(0,0))

# to avoid global variable instances in main function
def main() -> None:
    game = Game()
    game.loop()
    pg.quit()
    # del game


if __name__ == "__main__":
    main()
