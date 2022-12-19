import os

class Asset:
    def __init__(self, global_id: int, path: str, script: type):
        self.id: int = global_id
        self.path: str = path
        self.script: type = script

ASSET_DIR: str = os.path.dirname(__file__)
SCRIPT_DIR: str = f"{ASSET_DIR}/scripts"
SPRITE_DIR: str = f"{ASSET_DIR}/sprites"
MAP_DIR: str = f"{ASSET_DIR}/maps"

SPRITE_TILE_SIZE: int = 16
