# libraries
import pygame as pg
from pygame import Surface, Color, Rect, Vector2 as v2
from math import sqrt

# utils
from camera import Camera
from config import GameState, GameConfig
from input import Input
from eventlistener import EventManager
from customevents import PlayerActionEvent
from gui import GUI, HealthBar
from assets.spritesheet import SpritesheetManager

# entity
from assets.scripts.animable import Animable
from assets.scripts.gameobject_attributes import LightSource, Damaged

class Player(Animable, LightSource, Damaged):

    JUMP_HEIGHT: int = 4
               
    def __init__(self, position: v2, size: v2, mass: int) -> None:

        Animable.__init__(self, position, SpritesheetManager.SlimeAnimations["green"], size)
        LightSource.__init__(self, radius = 2*GameConfig.BLOCK_SIZE, glow=Color(119,230,119))
        self.mask: pg.mask.Mask = pg.mask.from_surface(self.animations["idle-right"][0])

        self.mass: int = mass
        self.__health: int = 300
        self.max_health: int = 300
        self.is_flying: bool = True
        self.size: v2 = size
        self.velocity: v2 = v2(0.0)
        self.acceleration: v2 = v2(0.0)
        self.status_frame: float = 0.0
        self.hurt_time: int = 0

        GUI.add_component(HealthBar(self))
    @property
    def emit_position(self) -> v2:
        return v2(self.rect.center)
        

    @property
    def health(self) -> int:
        return self.__health

    __life_to_color = ["ghost", "red", "orange", "green"]
    __life_to_glow = [(200, 200, 255, 128), (230,119,119), (255,140,16), (119,230,119)]
    @health.setter
    def health(self, v) -> None:
        self.__health = max(0, v)
        # 0 -> dead; 1-100 -> red; 101-200 -> orange; 201-300 -> green
        life_state = 3*(self.__health+(self.max_health//3-1))//self.max_health
        self.animations = SpritesheetManager.SlimeAnimations[Player.__life_to_color[life_state]]
        self.glow = Color(Player.__life_to_glow[life_state])
        
    def draw(self, camera: Camera) -> None:
        Animable.update(self)
        dest: v2 = camera.transform_coord(self.position)
        GameState.GAME_SURFACE.blit(self.texture, dest)

    # LigthSource
    @property
    def emit_position(self) -> v2:
        return v2(self.rect.center)

    def update(self) -> None:

        self.hurt_time = max(0, self.hurt_time - GameState.physicDT)

        if Input.is_pressed(pg.K_SPACE):
            EventManager.push_event(PlayerActionEvent(self))
        
        if Input.is_pressed(GameConfig.KeyBindings.right):
            self.acceleration.x += GameConfig.BLOCK_SIZE / GameState.physicDT * ( 1 - 0.75 * self.is_flying)

        if Input.is_pressed(GameConfig.KeyBindings.left):
            self.acceleration.x -= GameConfig.BLOCK_SIZE / GameState.physicDT * ( 1 - 0.75 * self.is_flying)

        if Input.is_pressed(GameConfig.KeyBindings.up) and not self.is_flying:
            # v² = 2*g*m*h 
            # sans la masse ça fait pas le bon saut
            # testé avec 2 valeurs de masse, de hauteur et de gravité, on saute bien à la hauteur souhaitée
            self.acceleration.y -= sqrt(2 * GameConfig.Gravity * Player.JUMP_HEIGHT * self.mass) / GameState.physicDT * GameConfig.BLOCK_SIZE 
            # on annule la gravité
            self.acceleration.y -= GameConfig.Gravity * self.mass * GameConfig.BLOCK_SIZE
            self.is_flying = True

    # Animables
    def update_animation(self) -> None:
        if self.hurt_time != 0:
            self.current_animation = f"hurt-{self.direction}"
        elif self.is_flying:
            self.current_animation = f"jump-{self.direction}"
        elif Input.is_pressed(GameConfig.KeyBindings.right):
            self.direction = "right"
            self.current_animation = f"walk-{self.direction}"
        elif Input.is_pressed(GameConfig.KeyBindings.left):
            self.direction = "left"
            self.current_animation = f"walk-{self.direction}"
        else:
            self.current_animation = f"idle-{self.direction}"

    def update_frame(self) -> None:
        self.status_frame = (self.status_frame+10*GameState.graphicDT) % 10

        if self.current_animation == f"jump-{self.direction}":
            # on est négatif si le joueur descend
            
            signe: int = (-1)**(self.velocity.y <= 0)
            ecc: float = self.velocity.y**2 / 2 * self.mass
            epp: float = GameConfig.Gravity * Player.JUMP_HEIGHT * GameConfig.BLOCK_SIZE**2 * self.mass

            # frame = signe * (rapport ecc sur epp) et un peu de hard code
            frame = int((signe * int( ecc/epp ) + 5) /10*6)
            frame = max(min(7, frame), 1)
            self.current_frame = frame
        else:
            self.status_frame -= GameState.graphicDT
            self.current_frame = int(self.status_frame % len(self.animations[self.current_animation]))
