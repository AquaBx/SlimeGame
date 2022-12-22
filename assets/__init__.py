import os

from .scripts.gameobject import Ground

class Asset:
    def __init__(self, global_id: int, path: str, script: type, name: str):
        self.id: int = global_id
        self.path: str = path
        self.script: type = script
        self.name: str = name

ASSET_DIR: str = os.path.dirname(__file__)
SCRIPT_DIR: str = f"{ASSET_DIR}/scripts"
SPRITE_DIR: str = f"{ASSET_DIR}/sprites"
MAP_DIR: str = f"{ASSET_DIR}/maps"
SAVE_DIR: str = f"{ASSET_DIR}/saves"

SPRITE_TILE_SIZE: int = 16

ASSETS: dict[int, Asset] = {
    id: Asset(id, f"{SPRITE_DIR}/{path}", script, name) for id, (name, path, script) in enumerate([
        # pas encore de scripts pour les background
        ("blue_background", "background/background.png", None),
        
        ("stone", "statics/ground.png", Ground),
        ("wood", "statics/wood_ground.png", Ground),
    ])
}
