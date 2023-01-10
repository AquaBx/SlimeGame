from pygame import Vector2 as v2
from numpy import ndarray

from . import serializer, graphics, physics
import assets.saves
from assets.scripts.environment import MapElement
from assets.scripts.player import Player
from assets.scripts.enemy import Enemy
from assets.scripts.gameobject_attributes import LightSource
from utils import coords_to_v2
from config import GameConfig, GameState
from camera import Camera

from eventlistener import Listener
from customevents import CustomEvent, ChangeStageEvent

from time import time

class World(Listener):

    def __init__(self) -> None:
        Listener.__init__(self, ["change_stage"], "world")
        # on charge les données dans la savestate selectionnée
        GameState.save["data"]: dict = assets.saves.load(GameState.save["state"])

        # si jamais la partie n'avait pas débuté on charge les données du début du jeu
        if not GameState.save["data"]["occupied"]:
            GameState.save["data"] = {
                "occupied": True,
                "last_map": "stage2",
                "player": {
                    "position": (59, 5), # ici il faudra mettre la position qui convient dans la map par défaut soit ici stage2
                    "health": 300
                }
            }

        self.blocks: ndarray[(None, MapElement)] = None

        self.deserialize(GameState.save["data"]["last_map"])
        position: tuple[int, int] = GameState.save["data"]["player"]["position"]
        self.player = Player(coords_to_v2(position), v2(18), 5, GameState.save["data"]["player"]["health"])
        self.enemies: list[Enemy] = []
        GameState.camera = Camera(self.player)

        self.summon_enemies()

    def update(self) -> None:
        self.update_entity(self.player)
        for enemy in self.enemies:
            self.update_entity(enemy)
        
        GameState.camera.update()

    def save(self) -> None:
        GameState.save["data"]["player"]["position"] = tuple(int(n) for n in self.player.position_matrix_center.yx)
        GameState.save["data"]["player"]["health"] = self.player.health
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


    def notify(self, ce: CustomEvent) -> None:
        cse: ChangeStageEvent = ce
        
        GameState.paused = True
        GameState.save["data"]["last_map"] = cse.next_map
        
        LightSource.sources.clear()
        self.enemies.clear()
        self.summon_enemies()
        self.deserialize(cse.next_map)
        
        self.player: Player = Player(coords_to_v2(cse.next_position), self.player.size, self.player.mass, self.player.health)
        
        GameState.camera = Camera(self.player)
        GameState.paused = False
