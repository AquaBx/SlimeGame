# libraries
from pygame import Surface, Vector2 as v2
from abc import ABC, abstractclassmethod

# utils
from config import GameConfig, GameState
from camera import Camera

# entity
from assets.scripts.gameobject import GameObject

class Animable(GameObject, ABC):

    # pour init je vois plutôt passer la spritesheet en paramètre
    # donner une liste de nom d'animations
    # une animation par ligne

    def __init__(self, position: v2, animations: dict[str, list[Surface]], size: v2 = v2(GameConfig.BLOCK_SIZE)) -> None:
        GameObject.__init__(self, position, size)
        self.direction:str = "right"
        self.current_animation: str = f"idle-{self.direction}"
        self.current_frame: int = 0
        self.animations: dict[str, list[Surface]] = animations
        self.status_frame: float = 0.0

    @property
    def texture(self):
        return self.animations[self.current_animation][self.current_frame]

    def draw(self, camera : Camera):
        self.update_animation()
        self.update_frame()
        dest: v2 = camera.transform_coord(self.position)
        GameState.GAME_SURFACE.blit(self.texture, dest)

    @abstractclassmethod
    def update_animation(self) -> None: ...
    
    @abstractclassmethod
    def update_frame(self) -> None: ...

    