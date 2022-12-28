import pygame as pg
from pygame import Vector2 as v2, Surface
from pygame.font import Font


class GameConfig:

    """
    resolution   | facteur 
    1080p        | 120
    720p         | 80
    540p         | 60
    360p         | 40
    144p (natif) | 16
    """

    BLOCK_SIZE: int = 16

    WINDOW_SIZE: v2 = v2(16,9) * 16
    FPS: float = 60.0

    WINDOW: Surface
    GAME_SURFACE: Surface

    class KeyBindings:
        left = -1
        right = -1
        up = -1

    opacity_world = 150

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

    def initialise() -> None:

        with open("settings.txt") as config:
            for option in config.read().split("\n"):
                if option == "":
                    continue
                
                attr,val = option.split("=")

                if "KeyBindings" in attr:
                    exec(f"{attr}=pg.key.key_code('{val}')")
                else:
                    exec(f"{attr}={val}")

        pg.display.set_caption("Slime Game")
        pg.font.init()
        GameConfig.WINDOW = pg.display.set_mode(GameConfig.WINDOW_SIZE.xy)
        GameConfig.GAME_SURFACE = pg.Surface((GameConfig.WINDOW_SIZE.x*9*GameConfig.BLOCK_SIZE/GameConfig.WINDOW_SIZE.y,9*GameConfig.BLOCK_SIZE))
        for name, path in GameConfig.__FONTS_DATA.items():
            GameConfig.FONTS[name] = Font(path, GameConfig.FONT_SIZE)


class GameState:
    dt: float = 1/60
    
    save: dict = {
        "state": 1,
        "data": {}
    }
