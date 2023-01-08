from mapeditor.config import *
from assets.scripts.environment import MapElement

from abc import ABC

from pygame import sprite
from pygame import Vector2 as v2, Rect, Surface

class Element(sprite.DirtySprite, ABC):
    """Represents a tile, abstract
    """
    
    def __init__(self, id: int, coord: v2, image: Surface) -> None:

        super().__init__()
        self.id: int = id
        self.image: Surface = image
        self.rect: Rect = Rect(coord, image.get_size())

class StateElement(Element):

    def __init__(self, id: int, state: int, uuid: int, coord: v2, image: Surface) -> None:
        """Element that has different states

        Args:
            id (int): numeric id of the related asset
            state (int): current state of the tile
            uuid (int): unique identifier for the tile
            coord (v2): coordinate of the tile in the map
            image (Surface): texture of the tile
        """

        super().__init__(id, coord, image)
        self.state: int = state
        self.uuid: int = uuid

# Represents the air in-game
EmptyElement: StateElement = StateElement(-1, 0, 0x0000, v2(0, 0), Surface((1, 1)))

class IndexedElement(StateElement):

    def __init__(self, id: int, index: int, uuid: int, coord: v2, image: Surface):
        """StateElement that uses an index to choose texture

        Args:
            id (int): numeric id of the related asset
            index (int): index of the current texture
            uuid (int): unique identifier for the tile
            coord (v2): coordinate of the tile in the map
            image (Surface): texture of the tile
        """

        super().__init__(id, index, uuid, coord, image)

    # alias of state in StateElement
    @property
    def index(self) -> int:
        return self.state

    @index.setter
    def index(self, value: int) -> None:
        self.state = value

class FlagElement(StateElement):
 
    def __init__(self, id: int, flags: int, uuid: int, coord: v2, image: Surface) -> None:
        """StateElement that uses flags to choose texture

        Args:
            id (int): numeric id of the related asset
            flags (int): current flags of the tile 
            uuid (int): unique identifier for the tile
            coord (v2): coordinate of the tile in the map
            image (Surface): texture of the tile
        """

        super().__init__(id, flags, uuid, coord, image)
    
    # alias of state in StateElement
    @property
    def flag(self) -> int:
        return self.state

    @flag.setter
    def flag(self, value: int) -> None:
        self.state = value

class PaletteElement(IndexedElement):

    def __init__(self, id: int, index: int, script: type[MapElement], coord: v2, spritesheet: Surface):
        """IndexedElement that also stores its spritesheet

        Args:
            id (int): numeric id of the related asset
            index (int): index of the current texture
            coord (v2): coordinate of the tile in the map
            spritesheet (Surface): texture of the tile
        """

        self.spritesheet : list[Surface] = list()
        (spritesheet_columns, spritesheet_rows) = (spritesheet.get_width()//SPRITE_TILE_SIZE, spritesheet.get_height()//SPRITE_TILE_SIZE)
        for i in range(spritesheet_rows):
            for j in range(spritesheet_columns):
                self.spritesheet.append(spritesheet.subsurface(Rect(j*SPRITE_TILE_SIZE, i*SPRITE_TILE_SIZE, SPRITE_TILE_SIZE, SPRITE_TILE_SIZE)))

        super().__init__(id, index, 0x0000, coord, self.spritesheet[index])
        self.script = script
