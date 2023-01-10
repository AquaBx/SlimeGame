import assets
from assets import Asset

def compute_palette_tile_size(window_width: int, palette_columns: int, ratio: float = 0.25) -> int:
    return int(ratio * window_width / palette_columns)

def compute_palette_offset(window_width: int, palette_width: int) -> int:
    return window_width - palette_width

def compute_grid_tile_size(window_size: tuple[int, int], grid_dimensions: tuple[int, int], palette_width: int) -> int:
    return int(min((window_size[0]-palette_width)/grid_dimensions[1], window_size[1]/grid_dimensions[0]))

# CONFIG, SET YOUR OWN VALUES
WINDOW_W                : int = 750 # default 750
WINDOW_H                : int = 700 # default 700

DEFAULT_GRID_ROWS       : int = 18  # default 64
DEFAULT_GRID_COLUMNS    : int = 32  # default 64

DEFAULT_PALETTE_ROWS    : int = 30  # default 30
DEFAULT_PALETTE_COLUMNS : int = 13  # default 13

DEFAULT_BACKGROUND      : Asset = assets.ASSETS[0]

DEFAULT_PALETTE: list[Asset] = [
    assets.ASSETS[5],
    assets.ASSETS[2],
    assets.ASSETS[4],
    assets.ASSETS[1],
    assets.ASSETS[3],
    assets.ASSETS[6],
    assets.ASSETS[7]
]
# END OF CONFIG, DO NOT EDIT AFTER THIS LINE
SPRITE_TILE_SIZE         : int = 16

PALETTE_TILE_SIZE        : int = compute_palette_tile_size(WINDOW_W, DEFAULT_PALETTE_COLUMNS)
DEFAULT_PALETTE_WIDTH    : int = DEFAULT_PALETTE_COLUMNS*PALETTE_TILE_SIZE
DEFAULT_PALETTE_HEIGHT   : int = DEFAULT_PALETTE_ROWS*PALETTE_TILE_SIZE
PALETTE_X                : int = compute_palette_offset(WINDOW_W, DEFAULT_PALETTE_WIDTH)

GRID_TILE_SIZE           : int = compute_grid_tile_size((WINDOW_W, WINDOW_H), (DEFAULT_GRID_ROWS, DEFAULT_GRID_COLUMNS), DEFAULT_PALETTE_WIDTH)
DEFAULT_GRID_WIDTH       : int = DEFAULT_GRID_COLUMNS*GRID_TILE_SIZE
DEFAULT_GRID_HEIGHT      : int = DEFAULT_GRID_ROWS*GRID_TILE_SIZE
