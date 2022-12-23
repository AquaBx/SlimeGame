from numpy import full
from numpy import ndarray

from pygame import Rect, Surface, Vector2 as v2
from pygame import transform, image

from config import *
from palette import Palette
from window_component import WindowComponent
from gamestates import GameStates

from assets import Asset
from elements import StateElement, IndexedElement, EmptyElement

class Grid(WindowComponent):

    tile_size: int = GRID_TILE_SIZE

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

        # Each neighboor is associated with a weight (base2 bit), each weight is associated with a state.
        # Note that diagonal neighboors might be irrelevant so we ignore them under specific conditions
        # scoring of X:
        # 128 1   2
        # 64  X   4
        # 32  16  8
        scoring_table = { # This table is only correct for Ground types
            28 : 0 , 124: 1 , 112: 2 , 16 : 3 , 247: 4 , 223: 5 ,
            31 : 6 , 255: 7 , 241: 8 , 17 : 9 , 253: 10, 127: 11,
            7  : 12, 199: 13, 193: 14, 1  : 15, 23 : 16, 209: 17,
            4  : 18, 68 : 19, 64 : 20, 0  : 21, 29 : 22, 113: 23,
            125: 24, 245: 25, 93 : 26, 117: 27, 20 : 28, 80 : 29,
            95 : 30, 215: 31, 87 : 32, 213: 33, 5  : 34, 65 : 35,
            116: 36, 92 : 37, 21 : 38, 84 : 39, 119: 40, 221: 41,
            197: 42, 71 : 43, 69 : 44, 81 : 45, 85 : 46
        }
        for i in range(self.rows):
            (top, bottom) = (i == 0, i == self.rows-1)
            for j in range(self.columns):
                (left, right) = (j == 0, j == self.columns-1)

                el: IndexedElement = self.map[i, j]
                if el is EmptyElement: continue

                # has neighboor
                (t,  r,  b,  l )  = (False, False, False, False)
                (tr, rb, bl, lt)  = (False, False, False, False)

                # 4 neighboors
                # side is calculated if there is no OOB risk
                t = (not top)    and (self.map[i-1, j].id == el.id)
                r = (not right)  and (self.map[i, j+1].id == el.id)
                b = (not bottom) and (self.map[i+1, j].id == el.id)
                l = (not left)   and (self.map[i, j-1].id == el.id)

                # 8 neighboors
                # corner is calculated if the 2 connected sides match with the current tile 
                tr = (t and r) and (self.map[i-1,j+1].id == el.id)
                rb = (r and b) and (self.map[i+1,j+1].id == el.id)
                bl = (b and l) and (self.map[i+1,j-1].id == el.id)
                lt = (l and t) and (self.map[i-1,j-1].id == el.id)

                # score calculation uses base2 to base10 system
                score = sum([((1<<i)*border) for i, border in enumerate([t, tr, r, rb, b, bl, l, lt])])

                el.index = scoring_table[score]
                el.image = palette.elements[el.id].spritesheet[el.index]

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
            self.map[i, j] = StateElement(palette.selected.id, palette.selected.state, palette.selected.uuid, v2(j*Grid.tile_size, i*Grid.tile_size), palette.selected.image)

    def remove_tile(self, mouse_coord: v2) -> None:
        """Removes a tile from the current map

        Args:
            mouse_coord (v2): Coordinates of the click
        """
        i, j = (int(mouse_coord.y)//Grid.tile_size, int(mouse_coord.x)//Grid.tile_size)
        self.map[i, j] = EmptyElement
    
    def clear(self) -> None:
        """Clears the current map from all its tiles
        """
        self.map.fill(EmptyElement)
