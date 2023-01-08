# standard
from threading import Thread

# libraries
import pygame as pg
from pygame.time import Clock

from text import Text
from menu_screen import Menu
from input import Input
from world import World
from config import GameConfig, GameState
from assets.spritesheet import SpritesheetManager

from eventlistener import EventManager
from buttons import ButtonManager
from gui import GUI

from world import World

from eventlistener import Listener
from customevents import CustomEvent, TitleScreenEvent, MenuEvent, QuitEvent

class Game(Listener):
    def __init__(self) -> None:
        pg.init()
        GameState.initialize()

        EventManager.initialize([
            "player_action",
            
            "title_screen",
            "menu",
            "quit"
        ])
        Listener.__init__(self, ["menu", "title_screen", "quit"])

        Input.init()
        Text.init(GameState.WINDOW, GameConfig.FONT_DATA, GameConfig.FONT_SIZE)
        ButtonManager.init(GameState.WINDOW)
        Menu.init()
        SpritesheetManager.initialize()

        self.physics: Thread = Thread(target=self.__update)
        self.clock: Clock = Clock()
        self.should_quit: bool = False

        self.world: World = None
        self.paused: bool = True

    def __del__(self) -> None:
        pg.quit()

    def loop(self) -> None:
        Menu.open_menu("title_screen")
        self.physics.start()
        while not self.should_quit:
            Input.update()

            self.__process_events()

            if not Menu.is_open():
                GameState.graphicDT = 1 / self.clock.get_fps() if self.clock.get_fps() != 0 else 1 / GameConfig.Graphics.MaxFPS
                GameState.GAME_SURFACE.fill('Black')
                self.__draw()

            EventManager.flush()
            ButtonManager.update()
            pg.display.update()
            self.clock.tick(GameConfig.Graphics.MaxFPS)

    def notify(self, ce: CustomEvent) -> None:
        match ce.key:

            case "title_screen":
                tse: TitleScreenEvent = ce
                if tse.action == "menu.title.continue":
                    self.world = World()
                    self.paused = False
                    Menu.close_menu("title_screen")
                elif tse.action == "menu.title.settings":
                    ...
                elif tse.action == "menu.title.quit":
                    self.should_quit = True

            case "menu":
                me: MenuEvent = ce
                if me.action == "menu.ingame.save_and_quit":
                    self.save_and_quit()
                elif me.action == "menu.ingame.resume":
                    self.paused = False
                    Menu.close_menu("ingame_pause")
                elif me.action == "menu.ingame.settings":
                    ...

            case "quit":
                self.should_quit = True

    def save_and_quit(self) -> None:
        if not self.world is None:
            self.world.save()
        self.should_quit = True

    def __process_events(self) -> None:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                self.should_quit = True
        if Input.is_pressed_once(pg.K_ESCAPE) and not Menu.is_open("title_screen"):
            if self.paused:
                self.paused = False
                Menu.close_menu("ingame_pause")
            else:
                self.paused = True
                Menu.open_menu("ingame_pause")

    def __update(self) -> None:
        clock = Clock()
        while not self.should_quit:
            if not Menu.is_open():
                self.world.update()
            GameState.physicDT = 1. / (clock.get_fps() + (clock.get_fps() == 0.) * GameConfig.PhysicTick)
            clock.tick(GameConfig.PhysicTick)

    def __draw(self) -> None:
        self.world.draw()
        GUI.draw(GameState().GAME_SURFACE)
        
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
