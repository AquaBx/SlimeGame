from pygame import Rect, Vector2 as v2
from pygame import image, transform, draw

from mapeditor.config import * 
from window_component import WindowComponent
from elements import PaletteElement
from gamestates import GameStates
from assets import Asset, ASSETS

class Palette(WindowComponent):
    
    tile_size: int = PALETTE_TILE_SIZE

    def __init__(self, rect: Rect, table: list[Asset] = DEFAULT_PALETTE) -> None:
        """Holds the elements that can be used to draw the map

        Args:
            rect (Rect): Hitbox of the palette
            table (list[Asset], optional): Assets that will compose the palette. Defaults to DEFAULT_PALETTE.
        """
        
        super().__init__(rect)

        self.table: list[Asset] = table
        self.hitboxes: list[tuple[int, Rect]] = list()
        self.elements: dict[int, PaletteElement] = dict()
        self.selected: PaletteElement = None

        for local_id, asset in enumerate(table):

            rect: Rect = Rect(
                PALETTE_X+Palette.tile_size*(local_id%DEFAULT_PALETTE_COLUMNS),
                Palette.tile_size*(local_id//DEFAULT_GRID_COLUMNS),
                Palette.tile_size, Palette.tile_size
            )

            self.hitboxes.append((local_id, rect))
            self.elements[local_id] = PaletteElement(local_id, asset.script.default_state(), asset.script, rect.topleft, image.load(asset.path))
        
        # Manually add a new asset to the palette of a map
        # self.__manual_add(table, 7, "assets/sprites/statics/placeholder.png", Door)
    
    def draw(self) -> None:
        for el in self.elements.values():
            GameStates.window.blit(transform.scale(el.image, (Palette.tile_size, Palette.tile_size)), el.rect.topleft)
        if not self.selected is None:
            draw.rect(GameStates.window, "yellow", Rect(self.selected.rect.topleft, (Palette.tile_size, Palette.tile_size)), 2)

    def handle_click(self, mouse_coord: v2) -> None:
        """Selects an element using a click

        Args:
            mouse_coord (v2): coordinates of the mouse
        """
        for local_id, box in self.hitboxes:
            if box.collidepoint(mouse_coord.x, mouse_coord.y):
                self.select(local_id)

    def select(self, id: int) -> None:
        """Selects an element in the current palette

        Args:
            id (int): the index of the element in the palette
        """
        if id < len(self.elements.items()) : self.selected = self.elements[id]

    def __manual_add(self, table, global_id: int, path: str, asset_type: type, local_id: int = -1):
        l_id = local_id if local_id != -1 else len(table)
        rect: Rect = Rect(
            PALETTE_X+Palette.tile_size*(l_id%DEFAULT_PALETTE_COLUMNS),
            Palette.tile_size*(l_id//DEFAULT_GRID_COLUMNS),
            Palette.tile_size, Palette.tile_size
        )
        if(local_id == -1):
            self.hitboxes.append((l_id, rect))     
        self.elements[l_id] = PaletteElement(l_id, asset_type.default_state(), asset_type, rect.topleft, image.load(path))
        self.table.append(ASSETS[global_id])