# libraries
import pygame as pg

# utils
from config import GameConfig

# entity
from assets.scripts.gameobject import GameObject

class Renderable(GameObject):
    """Définie une `texture` et une `size` pour une entité du jeu
    
    - Hérite de GameObject
    """

    def __init__(self, position: pg.Vector2, texture: pg.Surface, size: pg.Vector2 = pg.Vector2(GameConfig.BLOCK_SIZE)) -> None:
        GameObject.__init__(self, position)
        self.size: pg.Vector2 = size
        self.texture: pg.Surface = texture

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.position, self.size)

    @rect.setter
    def rect(self, value: pg.Rect) -> None:
        self.position = pg.Vector2(value.topleft)
        self.size = pg.Vector2(value.size)
