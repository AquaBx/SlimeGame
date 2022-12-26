import pygame as pg
from pygame import Vector2 as v2, Surface
from pygame.font import Font

class GameConfig:
    WINDOW_SIZE: v2 = v2(1280,720)
    BLOCK_SIZE: float = WINDOW_SIZE.y / 12
    FPS: float = 144.0

    WINDOW: Surface
    FONT: Font
    back = pg.transform.scale(pg.image.load("main_background.jpg"), (WINDOW_SIZE.x, WINDOW_SIZE.y))

    def initialise() -> None:
        pg.display.set_caption("Premier Jeu")
        GameConfig.WINDOW = pg.display.set_mode((GameConfig.WINDOW_SIZE.x, GameConfig.WINDOW_SIZE.y))
        GameConfig.FONT = Font(None, 30)

class GameState:
    dt: float = 1/60
