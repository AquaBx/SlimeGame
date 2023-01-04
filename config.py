import pygame as pg
from pygame import Vector2 as v2, Surface
from pygame.font import Font
import json
import inspect

class GameConfig:
    BLOCK_SIZE      : int   = 16
    Gravity         : float = 9.81
    NB_BLOCK_HEIGHT : int   = 12 # nombre de blocks affichés verticalement
    BLOCKS_HEIGHT   : int   = NB_BLOCK_HEIGHT * BLOCK_SIZE

    # ambient_color_world = (170, 170, 170) # jour
    ambient_color_world = (120, 120, 120) # aube
    # ambient_color_world = ( 15,  15,  45) # nuit

    PhysicTick = 120

    FONT_SIZE: int = 25
    FONT_DIR: str = "assets/fonts"
    FONT_DATA: dict[str, str] = {
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
        EnableLights: bool = True
        WindowAutoSize: bool  = True
        WindowHeight: int  = 360
        WindowWidth:  int  = 640
        MaxFPS:       int  = 144
        Fullscreen:  bool  = False

        @property
        def WindowSize(self) -> v2:
            return v2(self.WindowWidth, self.WindowHeight)

        @property
        def WindowRatio(self) -> v2:
            return v2(self.WindowWidth/self.WindowHeight, 1.0)

class GameState:
    
    def __initialize_game_configuration(T: type, attributes: dict[str, str]) -> None:
        """
        fonction qui attributs les settings du fichier settings.json à la classe GameConfig
        """
        for attr in attributes.keys():
            if not(attr in T.__dict__.keys()):
                print(f"{attr} not a attribut of {T.__name__}")
            elif inspect.isclass(T.__dict__[attr]):
                GameState.__initialize_game_configuration(T.__dict__[attr], attributes[attr])
            elif hasattr(T, attr):
                setattr(T, attr, attributes[attr])

    def initialize() -> None:
        with open("settings.json") as file:
            GameState.save = json.load(file)
            GameState.save["state"] = 1
            GameState.save["data"] = dict()

        GameState.__initialize_game_configuration(GameConfig, GameState.save["GameConfig"])

        flags = pg.FULLSCREEN if GameConfig.Graphics().Fullscreen else 0

        if GameConfig.Graphics().WindowAutoSize:
            setattr( GameConfig.Graphics, "WindowWidth", pg.display.Info().current_w )
            setattr( GameConfig.Graphics, "WindowHeight", pg.display.Info().current_h )
        
        GameState.DEFAULT_FONT = Font(GameConfig.FONT_DATA["PressStart2P"], GameConfig.FONT_SIZE)
        GameState.WINDOW = pg.display.set_mode(GameConfig.Graphics().WindowSize, flags=flags )
        GameState.GAME_SURFACE = pg.Surface(GameConfig.Graphics().WindowRatio*GameConfig.BLOCKS_HEIGHT)

        # il faudra mettre cette health bar dans le joueur ou une de ses classes parents

        GameConfig.HealthBar = pg.image.load("assets/UI/healthbar.png").convert_alpha()
        
        pg.display.set_caption("Slime Game")
        pg.display.set_icon(pg.image.load("assets/UI/icon.png"))
        pg.font.init()

    DEFAULT_FONT: Font = None
    
    WINDOW: Surface = None
    GAME_SURFACE: Surface = None
    
    PhysicDT = 1/GameConfig.PhysicTick
    dt: float = 1/60

    save: dict = {}
