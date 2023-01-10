from pygame import Surface, Rect, Vector2 as v2
from pygame import display, transform
from numpy import ndarray

from time import sleep

from . import serializer, graphics, physics
import assets.saves
from assets.scripts.environment import MapElement
from assets.scripts.player import Player
from assets.scripts.enemy import Enemy
from assets.scripts.gameobject_attributes import LightSource
from utils import coords_to_v2
from config import GameState, GameConfig
from camera import Camera
from sounds import Sounds
from eventlistener import Listener
from customevents import CustomEvent, ChangeStageEvent, PlayerDeathEvent
from menu_screen import MenuManager
from gui import GUI


class World(Listener):

    def __init__(self) -> None:
        Listener.__init__(self, ["player_death"], "world")
        # on charge les données dans la savestate selectionnée
        if GameState.save["data"] == {}:
            GameState.save["data"]: dict = assets.saves.load(GameState.save["state"])

        # si jamais la partie n'avait pas débuté on charge les données du début du jeu
        if not GameState.save["data"]["occupied"]:
            GameState.save["data"] = {
                "occupied": True,
                "last_map": "stage2",
                "last_warp_exit": (59,5),
                "player": {
                    "position": (59, 5), # ici il faudra mettre la position qui convient dans la map par défaut soit ici stage2
                    "health": 300
                }
            }

        self.blocks: ndarray[(None, MapElement)]
        self.background: Surface
        self.blocks, self.background = self.deserialize(GameState.save["data"]["last_map"])
        player_position: tuple[int, int] = GameState.save["data"]["player"]["position"]
        self.player = Player(coords_to_v2(player_position), v2(18), 5, GameState.save["data"]["player"]["health"])
        self.enemies: list[Enemy] = []
        GameState.camera = Camera(self.player)
        self.summon_enemies()

        if(GameState.has_rpc):
            stage = GameState.save["data"]["last_map"]
            GameState.rpc.update(state=f"Playing {stage}",details="github.com/aquabx/slimegame",large_image="image")
            
    def update(self) -> None:
        self.update_entity(self.player)
        for enemy in self.enemies:
            self.update_entity(enemy)
        
        GameState.camera.update()

    def leave(self) -> None:
        # self.player = None
        # GameState.camera = None
        LightSource.sources.clear()
        self.enemies.clear()

    def save(self) -> None:
        GameState.save["data"]["player"]["position"] = tuple(int(n) for n in self.player.position_matrix_center.yx)
        GameState.save["data"]["player"]["health"] = self.player.health
        assets.saves.save(GameState.save["data"], GameState.save["state"])

    def deserialize(self, file: str) -> tuple[ndarray[(None, MapElement)], Surface]:
        return serializer.deserialize(self, file)

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


    def play_death(self):
        GameState.paused = True

        Sounds.pause_audio("theme")
        Sounds.play_audio("failure")

        # update to death animation
        self.player.update_animation()
        
        # death black screen shading
        s = Surface(GameConfig.gameGraphics.WindowSize)  # the size of your rect
        for i in range(255):
            #game draw
            self.draw()
            GUI.draw(GameState.GAME_SURFACE)
        
            GameState.WINDOW.blit(transform.scale(GameState.GAME_SURFACE, GameState.WINDOW.get_size()),(0,0))

            #black screen draw
            s.set_alpha(i)
            GameState.WINDOW.blit(s,(0,0))
            display.update()

        # reset player and quit world
        GameState.save["data"]["player"]["health"] = 300
        GameState.save["data"]["player"]["position"] = GameState.save["data"]["last_warp_exit"]
        assets.saves.save(GameState.save["data"], GameState.save["state"])
        self.leave()

        MenuManager.open_menu("death_screen")

    def notify(self, ce: CustomEvent) -> None:
        if(ce.key == "player_death"):
            self.play_death()
