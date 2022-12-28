import pygame as pg
from pygame import Vector2 as v2, Surface
from pygame.font import Font
import json
import inspect

class GameConfig:
    BLOCK_SIZE      : int = 16
    NB_BLOCK_HEIGHT : int = 9 # nombre de blocks affichés verticalement
    BLOCKS_HEIGHT   : int = NB_BLOCK_HEIGHT * BLOCK_SIZE

    # ambient_color_world = (170, 170, 170) # jour
    # ambient_color_world = (120, 120, 120) # aube
    ambient_color_world = ( 15,  15,  45) # nuit

    FONT_SIZE: int = 25
    FONT_DIR: str = "assets/fonts"
    FONTS: dict[str, Font] = {}
    __FONTS_DATA: dict[str, str] = {
        "BradBunR": f"{FONT_DIR}/BradBunR.ttf",
        "BLOBBYCHUG": f"{FONT_DIR}/BLOBBYCHUG.ttf",
        "PressStart2P": f"{FONT_DIR}/PressStart2P-Regular.ttf"
    }

    COLORS: dict[str, tuple[int, int, int]] = {
        "GREY":  (51, 51, 51),
        "RED":   (255, 0, 0),
        "BLUE":  (0, 0, 255),
        "GREEN": (0, 255, 0)
    }

    class KeyBindings:
        up   : int = pg.K_SPACE
        left : int = pg.K_LEFT
        right: int = pg.K_RIGHT

    class Graphics:
        EnableLights: bool= True
        WindowHeight: int = 1080
        WindowWidth : int = 1920
        MaxFPS      : int = 144

        @property
        def WindowSize(self) -> v2:
            return (self.WindowWidth,self.WindowHeight)
        @property
        def WindowRatio(self) -> v2:
            return self.WindowWidth/self.WindowHeight

    def initialise() -> None:

        def rec(classe, dict):
            """
            fonction qui attributs les settings du fichier settings.json à la classe GameConfig
            """
            for attr in dict.keys():
                if not(attr in classe.__dict__):
                    print(f"{attr} not a attribut of {classe.__name__}")
                elif inspect.isclass( classe.__dict__[attr] ):
                    rec(classe.__dict__[attr], dict[attr])
                elif hasattr(classe,attr):
                    setattr(classe,attr,dict[attr])

        with open("settings.json") as file:
            save: dict = json.load( file )
            rec(GameConfig,save["GameConfig"])
            
        pg.display.set_caption("Slime Game")
        pg.font.init()

        GameState.WINDOW = pg.display.set_mode(GameConfig.Graphics().WindowSize)
        GameState.GAME_SURFACE = pg.Surface((GameConfig.Graphics().WindowRatio*GameConfig.BLOCKS_HEIGHT,GameConfig.BLOCKS_HEIGHT))

        GameConfig.HealthBar = pg.image.load("assets/UI/healthbar.png").convert_alpha()
        
        for name, path in GameConfig.__FONTS_DATA.items():
            GameConfig.FONTS[name] = Font(path, GameConfig.FONT_SIZE)


class GameState:
    dt: float = 1/60
    WINDOW: Surface
    GAME_SURFACE: Surface
    
    save: dict = {
        "state": 1,
        "data": {}
    }
