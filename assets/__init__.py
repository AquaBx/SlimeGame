import os

from .scripts.environment import MapElement, Platform, Background, Lamp, Spike

class Asset:
    def __init__(self, global_id: int, path: str, script: type[MapElement], name: str):
        self.id: int = global_id
        self.path: str = path
        self.script: type[MapElement] = script
        self.name: str = name

ASSET_DIR: str = os.path.dirname(__file__)
SCRIPT_DIR: str = f"{ASSET_DIR}/scripts"
SPRITE_DIR: str = f"{ASSET_DIR}/sprites"
MAP_DIR: str = f"{ASSET_DIR}/maps"
SAVE_DIR: str = f"{ASSET_DIR}/saves"
FONT_DIR: str = f"{ASSET_DIR}/fonts"
UI_DIR: str = f"{ASSET_DIR}/UI"

SPRITE_TILE_SIZE: int = 16

ASSETS: dict[int, Asset] = {
    id: Asset(id, f"{SPRITE_DIR}/{path}", script, name) for id,(name,path,script) in enumerate([
        ("brick_background", "background/brick_background.png", Background),
        
        ("stone", "statics/stone.png", Platform),
        ("wood", "statics/wood_ground.png", Platform),
        ("dark bricks", "statics/dark_bricks.png", Platform),
        ("copper", "statics/copper_full.png", Platform),
        ("light", "statics/light.png", Lamp),
        ("spikes", "statics/spike.png", Spike)
    ])
}
