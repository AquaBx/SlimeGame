# libraries
import pygame as pg
from pygame import Surface, Color, Rect, Vector2 as v2

# utils
from camera import Camera
from config import GameState, GameConfig
from assets.spritesheet import SpritesheetManager

# entity
from assets.scripts.animable import Animable
from assets.scripts.gameobject_attributes import LightSource, Dynamic, Damager

def load_frame(spritesheet: Surface, current_frame: int, animation_index: int, size: v2, flip: bool) -> Surface:
    TILE_SIZE = 18
    return pg.transform.flip(pg.transform.scale(spritesheet.subsurface(Rect(current_frame*TILE_SIZE,animation_index*TILE_SIZE,TILE_SIZE,TILE_SIZE)), size), flip, False)

class Enemy(Animable, LightSource, Dynamic, Damager):

    def __init__(self, position: v2, size: v2, mass: int, path: v2) -> None:
        Animable.__init__(self, position, SpritesheetManager.SlimeAnimations["ghost"], size)
        LightSource.__init__(self, radius = 2*GameConfig.BLOCK_SIZE, glow=Color(200,200,200))
        Dynamic.__init__(self, mass, pg.image.load("assets/sprites/dynamics/slime_hitbox.png"))
        Damager.__init__(self, 50, 2, 2)

        #x1, x2
        self.path: v2 = path

    @property
    def emit_position(self) -> v2:
        return v2(self.rect.center)

    def update(self) -> None:
        if self.position_matrix_center.x * GameConfig.BLOCK_SIZE <= self.path[0]:
            self.direction = "right"
        elif self.position_matrix_center.x * GameConfig.BLOCK_SIZE > self.path[1]:
            self.direction = "left"
        
        self.acceleration.x += (2*int(self.direction=="right")-1 )* 0.5 *  GameConfig.BLOCK_SIZE / GameState.physicDT * ( 1 - 0.75 * self.is_flying)

    def update_animation(self) -> None:
        if self.is_flying:
            self.current_animation = f"jump-{self.direction}"
        # elif Input.is_pressed(GameConfig.KeyBindings.right):
        else:
            self.current_animation = f"walk-{self.direction}"
            self.current_animation = f"idle-{self.direction}"

    def update_frame(self) -> None:
        self.status_frame = (self.status_frame+10*GameState.graphicDT) % 10

        if self.current_animation == f"jump-{self.direction}":
            h = 4
            # on est négatif si le joueur descend
            
            signe: int = (-1)**(self.velocity.y <= 0)
            ecc: float = self.velocity.y**2 / 2 * self.mass
            epp: float = GameConfig.Gravity * h * GameConfig.BLOCK_SIZE**2 * self.mass

            # frame = signe * (rapport ecc sur epp) et un peu de hard code
            frame = int((signe * int( ecc/epp ) + 5) /10*6)
            frame = max(min(7, frame), 1)
            self.current_frame = frame
        else:
            self.status_frame -= GameState.graphicDT
            self.current_frame = int(self.status_frame % len(self.animations[self.current_animation]))
