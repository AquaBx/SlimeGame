# libraries
import pygame as pg

# utils
from config import GameConfig

# entity
from assets.scripts.gameobject import GameObject

class Animable(GameObject):

    # pour init je vois plutôt passer la spritesheet en paramètre
    # donner une liste de nom d'animations
    # une animation par ligne

    def __init__(self, position: pg.Vector2, animations: dict[str, list[pg.Surface]], size: pg.Vector2 = pg.Vector2(GameConfig.BLOCK_SIZE)) -> None:
        GameObject.__init__(self, position)
        self.size: pg.Vector2 = size
        self.direction:str = "right"
        self.current_animation: str = f"idle-{self.direction}"
        self.current_frame: int = 0
        self.animations: dict[str, list[pg.Surface]] = animations

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.position, self.size)

    @rect.setter
    def rect(self, value: pg.Rect) -> None:
        self.position = pg.Vector2(value.topleft)
        self.size = pg.Vector2(value.size)

    @property
    def texture(self):
        return self.animations[self.current_animation][self.current_frame]

    def update(self) -> None:
        self.update_animation()
        self.update_frame()

    def update_animation(self) -> None: ...
    def update_frame(self) -> None: ...

    