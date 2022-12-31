# libraries
import pygame as pg

# utils
from config import GameConfig

class GameObject:
    """Définie une `position` pour une entité du jeu
    """
    
    def __init__(self, position: pg.Vector2) -> None:
        self.position: pg.Vector2 = position

    @property
    def coordinates(self) -> tuple[int, int]:
        return (int(self.y/GameConfig.BLOCK_SIZE), int(self.x/GameConfig.BLOCK_SIZE))

    @property
    def position_matrix_top_left(self) -> pg.Vector2:
        return self.position/GameConfig.BLOCK_SIZE

    @property
    def position_matrix_center(self) -> pg.Vector2:
        return (self.position + self.size/2)/GameConfig.BLOCK_SIZE

    @property
    def position_matrix_top_right(self) -> pg.Vector2:
        return (self.position+pg.Vector2(self.size.x,0))/GameConfig.BLOCK_SIZE

    @property
    def position_matrix_bottom_left(self) -> pg.Vector2:
        return (self.position+pg.Vector2(0,self.size.y))/GameConfig.BLOCK_SIZE
    
    @property
    def position_matrix_bottom_right(self) -> pg.Vector2:
        return (self.position + self.size)/GameConfig.BLOCK_SIZE
