# libraries
import pygame as pg
from pygame import Vector2 as v2

# utils
from camera import Camera
from config import GameState, GameConfig
from input import Input

# entity
from assets.scripts.animable import Animable
from assets.scripts.lightsource import LightSource

def load_frame(name: str, size: pg.Vector2) -> pg.Surface:
    return pg.transform.scale(pg.image.load(name).convert_alpha(), size)

class Player(Animable, LightSource):

    __default_animations: dict[str, tuple[str, int]] = {
        "idle":  ("assets/sprites/dynamics/slime/Grn_idle%d.png",      11),
        "right": ("assets/sprites/dynamics/slime/Grn_right%d.png",     6 ),
        "left":  ("assets/sprites/dynamics/slime/Grn_left%d.png",      6 ),
        "jump":  ("assets/sprites/dynamics/slime/Grn_jump%d.png", 11)
    }

    def __init__(self, position: pg.Vector2, size: pg.Vector2) -> None:
        Animable.__init__(self, position, { name: [ load_frame(fmt % i, size) for i in range(1, count) ] for name, (fmt, count) in Player.__default_animations.items() }, size)
        LightSource.__init__(self)
        self.mask: pg.Mask = pg.mask.from_surface(self.animations["idle"][0])

        self.sante: int = 300
        self.santemax: int = 300
        self.is_flying: bool = True
        self.taille: pg.Vector2 = size
        self.vitesse: pg.Vector2 = pg.Vector2(0.0)
        self.acceleration: pg.Vector2 = pg.Vector2(0.0)
        self.status_frame = 0

    @property
    def emit_position(self) -> pg.Vector2:
        return self.rect.center

    def draw(self, camera: Camera) -> None:
        Animable.update(self)
        dest: pg.Vector2 = camera.transform_coord(self.position)
        GameState.GAME_SURFACE.blit(self.texture, dest)

    def update(self) -> None:
        if Input.is_pressed(GameConfig.KeyBindings.right):
            self.acceleration.x += GameConfig.BLOCK_SIZE / GameState.PhysicDT * ( 1 - 0.75 * self.is_flying)

        if Input.is_pressed(GameConfig.KeyBindings.left):
            self.acceleration.x -= GameConfig.BLOCK_SIZE / GameState.PhysicDT * ( 1 - 0.75 * self.is_flying)

        if Input.is_pressed(GameConfig.KeyBindings.up) and not self.is_flying:
            self.acceleration.y -= 20 * GameConfig.BLOCK_SIZE / GameState.PhysicDT
            self.is_flying = True

    def update_animation(self) -> None:
        if Input.is_pressed(GameConfig.KeyBindings.right):
            self.current_animation = "right"
        elif Input.is_pressed(GameConfig.KeyBindings.left):
            self.current_animation = "left"
        else:
            self.current_animation = "idle"

    def update_frame(self) -> None:
        self.status_frame = (self.status_frame+10*GameState.dt) % 10
        is_flying = self.is_flying
        # jump_counter = 1

        # condition pour self.current_animation = "jump"
        # condition pour self.current_animation = "fall"

        # touches provisoires pour tester les frames
        # if Input.is_pressed(pg.K_p):
            # self.current_animation = "death"
        # elif Input.is_pressed(pg.K_o):
            # self.current_animation = "damage"
        # elif pressed[pg.K_i]:
        #     self.current_animation = "attack"
        # elif pressed[pg.K_u]:
        #     self.current_animation = "interaction"

        # propre
        if self.is_flying:
            self.current_animation = "jump"
        elif Input.is_pressed(GameConfig.KeyBindings.right):
            self.current_animation = "right"
        elif Input.is_pressed(GameConfig.KeyBindings.left):
            self.current_animation = "left"
        else:
            self.current_animation = "idle"

        pos_avant = v2(self.position.x,self.position.y)

        dir_y = self.position.y - pos_avant[1]

        # if self.current_animation == "jump":
        #     if is_flying: # si le slime vole -> frames 1, 2, 3, 4, 5, 6, 7
        #         if dir_y > 0 : # si le slime descend -> frames 6 7
        #             if jump_counter >= 7:
        #                 self.status_frame = 7
        #             elif 6 <= jump_counter <= 7:
        #                 self.status_frame = jump_counter
        #         elif dir_y < 0: # si le slime monte -> frames 1 2 3 4
        #             if 1 < jump_counter < 5:
        #                 self.status_frame = jump_counter
        #         else : # si le slime reste sur place -> frame 5
        #             if jump_counter == 5:
        #                 self.status_frame = 5
        #     else : # si le slime ne vole pas -> frames 0 8 9
        #         if jump_counter == 8 or jump_counter == 9:
        #             self.status_frame = jump_counter # je test
        #     jump_counter += 1

        if self.current_animation == "jump":
            frame = int(self.vitesse.y/300*5)
            frame = max(min(3,frame),-4)+5
            self.status_frame = frame
            self.current_frame = frame
        else:
            self.status_frame -= GameState.dt
            self.current_frame = int(self.status_frame % len(self.animations[self.current_animation]))
