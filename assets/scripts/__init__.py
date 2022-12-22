from pygame import Surface, Vector2 as v2

from config import GameConfig

from assets.palette import Palette

class Empty:
    def __init__(self, coord: tuple[int, int]):
        self.texture: Surface = Surface((0, 0))
        self.position: v2 = v2(coord[1], coord[0]) * GameConfig.BLOCK_SIZE

class IGameObject:
    def create(coord: tuple[int, int], id: int, state: int, uuid: int):
        return Empty(coord)

class Ground(IGameObject):
    def __init__(self, position: v2, texture: Surface) -> None:
        self.position: v2 = position
        self.texture: Surface = texture

    def create(coord: tuple[int, int], id: int, state: int, uuid: int):
        return Ground(v2(coord[1], coord[0])*GameConfig.BLOCK_SIZE, Palette.get_texture(id, state))
