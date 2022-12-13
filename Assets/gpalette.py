import pygame
from pygame import Vector2 as v2, Surface, Rect

from assets import Asset, SPRITE_DIR, SPRITE_TILE_SIZE
from .scripts.gameobject import Ground

ASSETS: dict[int, Asset] = {
    id: Asset(id, f"{SPRITE_DIR}/{path}", script) for (id, path, script) in [
        (0, "statics/ground.png", Ground),
        (1, "statics/wood_ground.png", Ground),
        (2, "statics/wood_ground1.png", Ground),
        (3, "statics/wood_wall.png", Ground),
        (4, "statics/wood_wall1.png", Ground),
    ]
}

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

    def __init__(self, table: dict[int, Asset]):
        self.elements: dict[int, PaletteElement] = {}
        for (local_id, asset) in table.items():
            self.elements[local_id] = PaletteElement(local_id, asset.id, pygame.image.load(asset.path))

    def get_texture(self, id: int, state: int):
        return self.elements[id].spritesheet[state]
