from . import serializer, graphics, physics

from pygame import Rect, Vector2 as v2
from pygame.mask import Mask
import assets.saves
from assets.scripts.player import Player
from assets.scripts.enemy import Enemy
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
                "last_map": "test_damages",
                "player": {
                    "position": (20, 40) # ici il faudra mettre la position qui convient dans la map par défaut soit ici stage2
                }
            }

        self.deserialize(GameState.save["data"]["last_map"])
        position: tuple[int, int] = GameState.save["data"]["player"]["position"]
        self.player = Player(v2(position[0], position[1])*GameConfig.BLOCK_SIZE, 18*v2(1, 1),5)
        self.ennemies = []
        GameState.camera = Camera(self.player)



    def update(self) -> None:        
        self.update_entity(self.player)
        for ennemy in self.ennemies:
            offset: v2 = ennemy.position - self.player.position
            collide_mask: Mask = self.player.mask.overlap_mask(ennemy.mask, offset)
            collide_rect: list[Rect] = collide_mask.connected_component().get_bounding_rects()

            if collide_rect:
                self.player.health -= 1
            self.update_entity(ennemy)
        GameState.camera.update()

    def deserialize(self, file: str) -> None:
        serializer.deserialize(self, file)

    def draw(self) -> None:
        graphics.draw(self)
    
    def update_entity(self, obj) -> None:
        physics.update_entity(self, obj)
