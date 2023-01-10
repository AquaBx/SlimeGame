# standard
from threading import Thread

# libraries
import pygame as pg
from pygame.time import Clock
from text import Text
from menu_screen import MenuManager
from input import Input
from world import World
from config import GameConfig, GameState
from assets.spritesheet import SpritesheetManager

from eventlistener import EventManager
from buttons import ButtonManager
from gui import GUI
from sounds import Sounds

from world import World

from eventlistener import Listener
from customevents import CustomEvent, TitleScreenEvent, MenuEvent, QuitEvent, FlushPygameEvent

class Game(Listener):
    
    events: list[pg.event.Event] = []
    
    def __init__(self) -> None:
        pg.init()
        GameState.initialize()

        EventManager.initialize([
            "player_action",
            
            "change_stage",
            
            "title_screen",
            "menu",
            "quit",
            
            "flush_pygame"
        ])
        Listener.__init__(self, ["menu", "title_screen", "quit", "flush_pygame"], "game")

        Input.init()
        Sounds.init()
        Text.init(GameState.WINDOW, GameConfig.FONT_DATA, GameConfig.FONT_SIZE)
        ButtonManager.init(GameState.WINDOW)
        MenuManager.init(GameState.WINDOW)
        SpritesheetManager.initialize()

        Sounds.audios_preparation()

        self.physics: Thread = Thread(target=self.__update)
        self.clock: Clock = Clock()
        self.should_quit: bool = False

        self.world: World = None

    def __del__(self) -> None:
        pg.quit()

    def loop(self) -> None:
        MenuManager.open_menu("title_screen")
        Input.update()
        Sounds.play_audio("title")
        self.physics.start()
        while not self.should_quit and self.physics.is_alive():
            # on récupère les évènements de pygame dans la boucle principale
            # car on ne peut pas le faire dans un thread secondaire
            evs = pg.event.get()
            EventManager.push_event(FlushPygameEvent(evs.copy()))
            EventManager.flush()

            if not GameState.paused:
                # 1 / FPS_actuel ou si 0 FPS actuellement, 1/maxFPS
                GameState.graphicDT = 1 / (self.clock.get_fps() + (self.clock.get_fps() == 0)*GameConfig.gameGraphics.MaxFPS)
                GameState.GAME_SURFACE.fill('Black')
                self.__draw()

            MenuManager.draw_menus()
            ButtonManager.draw()
            pg.display.update()
            self.clock.tick(GameConfig.gameGraphics.MaxFPS)

    def notify(self, ce: CustomEvent) -> None:
        match ce.key:

            case "title_screen":
                tse: TitleScreenEvent = ce
                if tse.action == "menu.title.continue":
                    Sounds.from_title_to_theme()
                    self.world = World()
                    self.paused = False
                    MenuManager.close_menu("title_screen")
                elif tse.action == "menu.title.settings":
                    ...
                elif tse.action == "menu.title.quit":
                    self.should_quit = True

            case "menu":
                me: MenuEvent = ce
                if me.action == "menu.ingame.save_and_quit":
                    self.save_and_quit()
                elif me.action == "menu.ingame.resume":
                    Sounds.from_title_to_theme()
                    self.paused = False
                    MenuManager.close_menu("ingame_pause")
                elif me.action == "menu.ingame.settings":
                    if GameConfig.Graphics.EnableLights: 
                        GameConfig.Graphics.EnableLights = False
                        ButtonManager.rename_menu("menu.ingame.settings", "RTX off")
                    else: 
                        GameConfig.Graphics.EnableLights = True
                        ButtonManager.rename_menu("menu.ingame.settings", "RTX on")


            case "quit":
                self.should_quit = True

            case "flush_pygame":
                fpe: FlushPygameEvent = ce
                for ev in fpe.events:
                    if ev.type == pg.QUIT:
                        self.should_quit = True

    def save_and_quit(self) -> None:
        if not self.world is None:
            self.world.save()
        self.should_quit = True

    def __update(self) -> None:
        clock = Clock()
        while not self.should_quit:
            Input.update()
            ButtonManager.update()

            if not GameState.paused:
                self.world.update()

            if Input.is_pressed_once(pg.K_ESCAPE) and not MenuManager.is_open("title_screen"):
                Sounds.play_audio("button")
                if GameState.paused:
                    Sounds.from_title_to_theme()
                    MenuManager.close_menu("ingame_pause")
                else:
                    Sounds.from_theme_to_title()
                    MenuManager.open_menu("ingame_pause")

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