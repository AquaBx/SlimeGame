from .deserialize import deserialize
from .draw import draw
from .update_pos import update_pos
from .collide import collide
from .update import update
from .update import update

from pygame import Vector2 as v2
import assets.saves
from assets import ASSETS
from assets.scripts.gameobject import Player
from config import GameConfig, GameState
from camera import Camera

class World:

    def __init__(self) -> None:
        # on charge les données dans la savestate selectionnée
        GameState.save["data"]: dict = assets.saves.load(GameState.save["state"])

        # si jamais la partie n'avait pas débuté on charge les données du début du jeu
        if not GameState.save["data"]["occupied"]:
            GameState.save["data"] = {
                "occupied": True,
                "last_map": "stage2",
                "player": {
                    "position": (5, 59) # ici il faudra mettre la position qui convient dans la map par défaut soit ici stage2
                }
            }

        self.deserialize(GameState.save["data"]["last_map"])
        position: tuple[int, int] = GameState.save["data"]["player"]["position"]
        self.player = Player(v2(position[0], position[1])*GameConfig.BLOCK_SIZE, 0.95*GameConfig.BLOCK_SIZE*v2(1, 1))
        self.camera: Camera = Camera(self.player)

    deserialize = deserialize
    draw = draw
    update_pos = update_pos
    collide = collide
    update = update