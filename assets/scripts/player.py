# libraries
import pygame as pg
from pygame import Color, Vector2 as v2
from math import sqrt

# utils
from camera import Camera
from config import GameState, GameConfig
from input import Input
from eventlistener import EventManager
from customevents import PlayerActionEvent
from gui import GUI, HealthBar
from assets.spritesheet import SpritesheetManager
from sounds import Sounds

# entity
from assets.scripts.animable import Animable
from assets.scripts.gameobject_attributes import LightSource, Damagable, Dynamic

class Player(Animable, LightSource, Dynamic, Damagable):

    JUMP_HEIGHT: int = 4

    # Damaged
    __life_to_color = ["ghost", "red", "orange", "green"]
    __life_to_glow = [(200, 200, 255, 128), (230,119,119), (255,140,16), (119,230,119)]

    def __init__(self, position: v2, size: v2, mass: int, health: int = 300) -> None:
        Damagable.__init__(self, 300, health)
        Dynamic.__init__(self, mass, pg.image.load("assets/sprites/dynamics/slime_hitbox.png"))

        life_state = 3*(self._health+(self.max_health//3-1))//self.max_health
        Animable.__init__(self, position, SpritesheetManager.SlimeAnimations[Player.__life_to_color[life_state]], size)
        LightSource.__init__(self, radius = 2*GameConfig.BLOCK_SIZE, glow=Color(Player.__life_to_glow[life_state]))

        GUI.add_component(HealthBar(self))

    def _set_health(self, v: int) -> None:
        self._health = max(0, v)
        # 0 -> dead; 1-100 -> red; 101-200 -> orange; 201-300 -> green
        life_state = 3*(self._health+(self.max_health//3-1))//self.max_health
        self.animations = SpritesheetManager.SlimeAnimations[Player.__life_to_color[life_state]]
        self.glow = Color(Player.__life_to_glow[life_state])      

    # LigthSource
    @property
    def emit_position(self) -> v2:
        return v2(self.rect.center)

    def update(self) -> None:
        self.hurt_time = max(0, self.hurt_time - GameState.physicDT)

        if Input.is_pressed_once(pg.K_SPACE):
            EventManager.push_event(PlayerActionEvent(self))
        
        if Input.is_pressed(GameConfig.KeyBindings.right):
            self.acceleration.x += GameConfig.BLOCK_SIZE / GameState.physicDT * ( 1 - 0.75 * self.is_flying)

        if Input.is_pressed(GameConfig.KeyBindings.left):
            self.acceleration.x -= GameConfig.BLOCK_SIZE / GameState.physicDT * ( 1 - 0.75 * self.is_flying)

        # if (Input.is_pressed_once(GameConfig.KeyBindings.right) or Input.is_pressed_once(GameConfig.KeyBindings.left)) and not self.is_flying:
        #     Sounds.play_audio("walk")

        # if (Input.is_just_released(GameConfig.KeyBindings.right) and not Input.is_pressed(GameConfig.KeyBindings.left)) or (Input.is_just_released(GameConfig.KeyBindings.left) and not Input.is_pressed(GameConfig.KeyBindings.right)) or self.is_flying:
        #     Sounds.stop_audio("walk")

        if Input.is_pressed(GameConfig.KeyBindings.up) and not self.is_flying:
            Sounds.play_audio("jump")
            # v² = 2*g*m*h 
            # sans la masse ça fait pas le bon saut
            # testé avec 2 valeurs de masse, de hauteur et de gravité, on saute bien à la hauteur souhaitée
            self.acceleration.y -= sqrt(2 * GameConfig.Gravity * Player.JUMP_HEIGHT * self.mass) / GameState.physicDT * GameConfig.BLOCK_SIZE 
            # on annule la sssgravité
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
