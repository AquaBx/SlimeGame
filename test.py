import pygame as pg
import json
import inspect

class GameConfig:
    
    with open("settings.json") as file:
        save: dict = json.load( file )

    class KeyBindings:
        up   : int = pg.K_SPACE
        left : int = pg.K_LEFT
        right: int = pg.K_RIGHT

    class Graphics:
        EnableLights: bool= True
        WindowHeight: int = 1080
        WindowWidth : int = 1920
        MaxFPS      : int = 144
    
    def rec(classe, dict):
        for attr in dict.keys():
            if inspect.isclass( classe.__dict__[attr] ):
                GameConfig.rec(classe.__dict__[attr], dict[attr])
            else:
                setattr(classe,attr,dict[attr])


def main():
    pg.init()

    GameConfig.rec(GameConfig, GameConfig.save["GameConfig"])

    print(GameConfig.KeyBindings.up)
    pg.quit()

if __name__ == "__main__":
    main()