import sys
sys.path.insert(0, ".")

import pygame as pg
from pygame.time import Clock

from config import GameConfig, GameState
from input import Input
from world import World

class Game:
    def __init__(self) -> None:
        pg.init();
        GameConfig.initialise()
        Input.init()
        self.clock: Clock = Clock()
        self.should_quit: bool = False
        # il faudra donner un entier qui correspond au fichier de sauvegarde demandé (1, 2 ou 3 sans doute)
        self.world: World = World(1)

    def __del__(self) -> None:
        pg.quit()

    def loop(self) -> None:
        while not self.should_quit:
            
            GameState.dt = 1 / self.clock.get_fps() if self.clock.get_fps() != 0 else 1 / GameConfig.FPS
            GameConfig.WINDOW.fill('Black')

            self.__process_events()
            self.__update()
            self.__draw()
            self.clock.tick_busy_loop(GameConfig.FPS)

    def __process_events(self) -> None:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                self.should_quit = True

    def __update(self) -> None:
        self.world.update()

    def __draw(self) -> None:
        self.world.draw()
        pg.display.update()

# to avoid global variable instances in main function
def main() -> None:
    Game().loop()

if __name__ == "__main__":
    main()
