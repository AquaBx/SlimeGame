from numpy import full
from numpy import ndarray

from pygame import Rect, Surface, Vector2 as v2
from pygame import transform, image

import json
from io import TextIOWrapper

from mapeditor.config import *
from palette import Palette
from window_component import WindowComponent
from gamestates import GameStates

from assets import Asset, SAVE_DIR
from elements import StateElement, EmptyElement

class Grid(WindowComponent):

    tile_size: int = GRID_TILE_SIZE
    metadata_file: TextIOWrapper
    metadata: dict[str, dict[str]]
    
    def initialize() -> None:
        with open(f"{SAVE_DIR}/metadata.json", "r") as f:
            Grid.metadata = json.load(f)

    def __init__(self, rect : Rect, background: Asset, grid: ndarray = None) -> None:
        """Holds the tiles of the map

        Args:
            rect (Rect): hitbox of the map
            background (Asset): Asset of the background
            grid (ndarray, optional): Tile matrix. Defaults to None.
        """
        super().__init__(rect)

        self.background: Asset = background
        self.__background: Surface = transform.scale(image.load(self.background.path), rect.size)

        if not grid is None:
            self.dim: tuple[int, int] = grid.shape
            self.map: ndarray = grid
        else:
            self.dim: tuple[int, int] = (DEFAULT_GRID_ROWS, DEFAULT_GRID_COLUMNS)
            self.map: ndarray = full(self.dim, EmptyElement, StateElement)

    @property
    def rows(self) -> int:
        return self.dim[0]

    @property
    def columns(self) -> int:
        return self.dim[1]

    def draw(self) -> None:
        GameStates.window.blit(self.__background,(0,0))
        for i in range(self.rows):
            for j in range(self.columns):
                if self.map[i, j] is EmptyElement: continue
                el : StateElement = self.map[i, j]
                GameStates.window.blit(transform.scale(el.image, (Grid.tile_size, Grid.tile_size)),(j*Grid.tile_size, i*Grid.tile_size))

    def compute_ct(self, palette: Palette): # ct stands for connected textures
        """Calculates the state the current tile should have. 
        
        Args:
            palette (Palette): Palette of the current map
        """
        
        for i in range(self.rows):
            (top, bottom) = (i == 0, i == self.rows-1)
            for j in range(self.columns):
                (left, right) = (j == 0, j == self.columns-1)

                el: StateElement = self.map[i, j]
                if el is EmptyElement: continue

                el.state = palette.elements[el.id].script.compute_state(self.map, palette, (top, right, bottom, left), el.id, (i,j))
                el.image = palette.elements[el.id].spritesheet[el.state]

    def put_tile(self, mouse_coord: v2, palette: Palette) -> None:
        """Adds a tile in the current map

        Args:
            mouse_coord (v2): Coordinates of the click
            palette (Palette): Palette of the current map
        """
        if palette.selected is None:
            return
        i, j = (int(mouse_coord.y)//Grid.tile_size, int(mouse_coord.x)//Grid.tile_size)
        if self.map[i, j].id != palette.selected.id:
            asset: Asset = palette.table[palette.selected.id]
            uuid: int = 0x0000
            if asset.script.require_uuid:
                uuid = Grid.metadata["last_uuid"]
                Grid.metadata["last_uuid"] += 1
            Grid.metadata[f"{uuid}"] = asset.script.default_metadata
            self.map[i, j] = StateElement(palette.selected.id, palette.selected.state, uuid, v2(j, i)*Grid.tile_size, palette.selected.image)

    def remove_tile(self, mouse_coord: v2) -> None:
        """Removes a tile from the current map

        Args:
            mouse_coord (v2): Coordinates of the click
        """
        i, j = (int(mouse_coord.y)//Grid.tile_size, int(mouse_coord.x)//Grid.tile_size)
        if self.map[i, j].uuid != 0x0000:
            # on retire 1 si l'élément qu'on retire est le dernier uuid
            Grid.metadata["last_uuid"] -= (self.map[i, j].uuid == Grid.metadata["last_uuid"]-1)
            del Grid.metadata[f"{self.map[i, j].uuid}"]
        self.map[i, j] = EmptyElement
    
    def clear(self) -> None:
        """Clears the current map from all its tiles
        """
        self.map.fill(EmptyElement)
