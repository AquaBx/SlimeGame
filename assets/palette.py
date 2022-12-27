import pygame
from pygame import Surface, Rect

# from assets import SPRITE_TILE_SIZE
SPRITE_TILE_SIZE: int = 16

class PaletteElement:
    def __init__(self, id: int, global_id: int, spritesheet: Surface):
        self.spritesheet : list[Surface] = []
        spritesheet_dims = (spritesheet.get_width()//SPRITE_TILE_SIZE, spritesheet.get_height()//SPRITE_TILE_SIZE)
        for y in range(spritesheet_dims[1]):
            for x in range(spritesheet_dims[0]):
                self.spritesheet.append(spritesheet.subsurface(Rect(x*SPRITE_TILE_SIZE,y*SPRITE_TILE_SIZE,SPRITE_TILE_SIZE,SPRITE_TILE_SIZE)))
        self.global_id = global_id
        self.local_id = id

class Palette:

    def load(table: list) -> None:
        Palette.elements: dict[int, PaletteElement] = {}
        for index, asset in enumerate(table):
            Palette.elements[index] = PaletteElement(index, asset.id, pygame.image.load(asset.path))

    def get_texture(id: int, state: int):
        return Palette.elements[id].spritesheet[state]
