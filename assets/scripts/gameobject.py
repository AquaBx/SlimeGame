# libraries
from pygame import Rect, Vector2 as v2

# utils
from config import GameConfig

class GameObject:
    """Définie une `position` pour une entité du jeu
    """
    
    def __init__(self, position: v2, size: v2) -> None:
        self.position: v2 = position
        self.size: v2 = size

    @property
    def coordinates(self) -> tuple[int, int]:
        return (int(self.y/GameConfig.BLOCK_SIZE), int(self.x/GameConfig.BLOCK_SIZE))

    @property
    def position_matrix_top_left(self) -> v2:
        return self.position/GameConfig.BLOCK_SIZE

    @property
    def position_matrix_center(self) -> v2:
        return (self.position + self.size/2)/GameConfig.BLOCK_SIZE

    @property
    def position_matrix_top_right(self) -> v2:
        return (self.position+v2(self.size.x,0))/GameConfig.BLOCK_SIZE

    @property
    def position_matrix_bottom_left(self) -> v2:
        return (self.position+v2(0,self.size.y))/GameConfig.BLOCK_SIZE
    
    @property
    def position_matrix_bottom_right(self) -> v2:
        return (self.position + self.size)/GameConfig.BLOCK_SIZE

    @property
    def rect(self) -> Rect:
        return Rect(self.position, self.size)

    @rect.setter
    def rect(self, value: Rect) -> None:
        self.position = v2(value.topleft)
        self.size = v2(value.size)
