import pygame as pg
from pygame import Vector2 as v2, Surface
from pygame.font import Font

class GameConfig:
    WINDOW_SIZE: v2 = v2(16,9) * 60
    BLOCK_SIZE: float = 16
    FPS: float = 144.0

    WINDOW: Surface
    GAME_SURFACE: Surface


    opacity_world = 150

    FONTS = {
        "BradBunR":"BradBunR.ttf",
        "BLOBBYCHUG":"BLOBBYCHUG.ttf",
        "PressStart2P":"PressStart2P-Regular.ttf"
    }

    COLORS  = {
        "GREY": (51,51,51),
        "RED" : (255,0,0),
        "BLUE" : (0,0,255),
        "GREEN" : (0,255,0)
    }

    def initialise() -> None:
        pg.display.set_caption("Slime Game")
        pg.font.init()
        GameConfig.WINDOW = pg.display.set_mode(GameConfig.WINDOW_SIZE.xy)
        GameConfig.GAME_SURFACE = pg.Surface((GameConfig.WINDOW_SIZE.x*9*GameConfig.BLOCK_SIZE/GameConfig.WINDOW_SIZE.y,9*GameConfig.BLOCK_SIZE))

    def FONT(font,size): 
        return Font(GameConfig.FONTS[font], size)

class GameState:
    dt: float = 1/60
