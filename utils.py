from pygame import Vector2 as v2
from config import GameConfig

def v2_to_coords(position: v2, grid_tile_size: int = GameConfig.BLOCK_SIZE) -> tuple[int, int]:
    return (int(position.y)//grid_tile_size, int(position.x)//grid_tile_size)

def coords_to_v2(coords: tuple[int, int], grid_tile_size: int = GameConfig.BLOCK_SIZE) -> v2:
    return v2(coords[1], coords[0]) * grid_tile_size