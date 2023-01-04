# libraries
import pygame as pg
from pygame import Surface, Color, Vector2 as v2
from math import sqrt

# utils
from camera import Camera
from config import GameState, GameConfig
from input import Input

# entity
from assets.scripts.animable import Animable
from assets.scripts.lightsource import LightSource

def load_frame(name: str, size: v2, flip: bool) -> Surface:
    return pg.transform.flip(pg.transform.scale(pg.image.load(name).convert_alpha(), size), flip, False)

class Player(Animable, LightSource):

    __default_animations: dict[str, tuple[str, int]] = {
        "idle":  ("assets/sprites/dynamics/slime/Grn_Idle%d.png", 11),
        "walk": ("assets/sprites/dynamics/slime/Grn_Walk%d.png", 6 ),
        "jump":  ("assets/sprites/dynamics/slime/Grn_Jump%d.png", 11)
    }

    def __create_animations(size: v2) -> dict[str, list[Surface]]:
        return {
            f"{name}-{direction}": [ load_frame(fmt % i, size, direction == "left") for i in range(1, count) ]
                                   for name, (fmt, count) in Player.__default_animations.items()
                                   for direction in ["right","left"]
        }

    def __init__(self, position: v2, size: v2, mass: int) -> None:
        Animable.__init__(self, position, Player.__create_animations(size), size)
        LightSource.__init__(self, radius = 2*GameConfig.BLOCK_SIZE, glow=Color(119,230,119))
        self.mask: pg.Mask = pg.mask.from_surface(self.animations["idle-right"][0])

        self.mass: int = mass
        self.health: int = 300
        self.max_health: int = 300
        self.is_flying: bool = True
        self.size: v2 = size
        self.velocity: v2 = v2(0.0)
        self.acceleration: v2 = v2(0.0)
        self.status_frame: float = 0.0

    @property
    def emit_position(self) -> v2:
        return v2(self.rect.center)

    def draw(self, camera: Camera) -> None:
        Animable.update(self)
        dest: v2 = camera.transform_coord(self.position)
        GameState.GAME_SURFACE.blit(self.texture, dest)

    def update(self) -> None:
        if Input.is_pressed(GameConfig.KeyBindings.right):
            self.acceleration.x += GameConfig.BLOCK_SIZE / GameState.PhysicDT * ( 1 - 0.75 * self.is_flying)

        if Input.is_pressed(GameConfig.KeyBindings.left):
            self.acceleration.x -= GameConfig.BLOCK_SIZE / GameState.PhysicDT * ( 1 - 0.75 * self.is_flying)

        if Input.is_pressed(GameConfig.KeyBindings.up) and not self.is_flying:
            hauteur = 4 # hauteur en blocks

            # v² = 2*g*m*h 
            # sans la masse ça fait pas le bon saut
            # testé avec 2 valeurs de masse, de hauteur et de gravité, on saute bien à la hauteur souhaitée
            self.acceleration.y -= sqrt(2 * GameConfig.Gravity * hauteur * self.mass) / GameState.PhysicDT * GameConfig.BLOCK_SIZE 
            self.acceleration.y -= GameConfig.Gravity * self.mass * GameConfig.BLOCK_SIZE
            self.is_flying = True

    def update_animation(self) -> None:
        if self.is_flying:
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
        self.status_frame = (self.status_frame+10*GameState.dt) % 10

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
            self.status_frame -= GameState.dt
            self.current_frame = int(self.status_frame % len(self.animations[self.current_animation]))
