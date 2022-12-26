import pygame as pg
from pygame import Vector2 as v2, Surface
from pygame.font import Font

class GameConfig:
    WINDOW_SIZE: v2 = v2(16,9) * 120
    BLOCK_SIZE: float = 16
    FPS: float = 144.0

    WINDOW: Surface
    GAME_SURFACE: Surface

    FONT: Font
    back = pg.transform.scale(pg.image.load("main_background.jpg"), WINDOW_SIZE.xy)

    opacity_world = 150

    def initialise() -> None:
        pg.display.set_caption("Premier Jeu")
        GameConfig.WINDOW = pg.display.set_mode(GameConfig.WINDOW_SIZE.xy)
        GameConfig.GAME_SURFACE = pg.Surface((GameConfig.WINDOW_SIZE.x*9*GameConfig.BLOCK_SIZE/GameConfig.WINDOW_SIZE.y,9*GameConfig.BLOCK_SIZE))
        GameConfig.FONT = Font(None, 30)

class GameState:
    dt: float = 1/60
