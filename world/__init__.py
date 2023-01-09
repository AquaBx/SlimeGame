from pygame import Rect, Vector2 as v2
from pygame.mask import Mask
from numpy import ndarray

from . import serializer, graphics, physics
import assets.saves
from assets.scripts.environment import MapElement
from assets.scripts.player import Player
from assets.scripts.enemy import Enemy
from utils import v2_to_coords, coords_to_v2
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
                    "position": (56, 11) # ici il faudra mettre la position qui convient dans la map par défaut soit ici stage2
                }
            }

        self.blocks: ndarray[(None, MapElement)] = None

        self.deserialize(GameState.save["data"]["last_map"])
        position: tuple[int, int] = GameState.save["data"]["player"]["position"]
        self.player: Player = Player(coords_to_v2(position), 18*v2(1, 1),5)
        self.enemies: list[Enemy] = []
        GameState.camera = Camera(self.player)

        self.summon_enemies()

    def update(self) -> None:
        self.update_entity(self.player)
        for enemy in self.enemies:
            self.update_entity(enemy)
        
        GameState.camera.update()

    def save(self) -> None:
        GameState.save["data"]["player"]["position"] = v2_to_coords(self.player.position_matrix_center * GameConfig.BLOCK_SIZE)
        assets.saves.save(GameState.save["data"], GameState.save["state"])

    def deserialize(self, file: str) -> None:
        serializer.deserialize(self, file)

    def draw(self) -> None:
        graphics.draw(self)

    def update_entity(self, obj) -> None:
        physics.update_entity(self, obj)

    # solution temp
    def summon_enemies(self):
        match GameState.save["data"]["last_map"]:
            case "stage2":
                self.enemies.append(Enemy(coords_to_v2((59, 9)), v2(18), 5, coords_to_v2((14,9))))
                self.enemies.append(Enemy(coords_to_v2((59,23)), v2(18), 5, coords_to_v2((40,24))))

