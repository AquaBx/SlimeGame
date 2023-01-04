# libraries
from pygame import Surface, Vector2 as v2

# utils
from config import GameConfig

# entity
from assets.scripts.gameobject import GameObject

class Renderable(GameObject):
    """Définie une `texture` et une `size` pour une entité du jeu
    
    - Hérite de GameObject
    """

    def __init__(self, position: v2, texture: Surface, size: v2 = v2(GameConfig.BLOCK_SIZE)) -> None:
        GameObject.__init__(self, position, size)
        self.texture: Surface = texture
