from abc import ABC, abstractclassmethod

import pygame as pg
from pygame import key, image, mask, transform
from pygame import Vector2 as v2, Rect, Surface
from pygame.mask import Mask

from camera import Camera
from config import GameConfig, GameState
from input import Input

from assets.palette import Palette

import shader

class IGameObject(ABC):
    
    def create(coord: tuple[int, int], id: int, state: int, uuid: int):
        print(f"Create Default Game Object at coord {coord} (id: int - {id} ; state: int {state} ; uuid: int {uuid})")
        return GameObject(state, v2(coord[1], coord[0]) * GameConfig.BLOCK_SIZE, v2(1, 1) * GameConfig.BLOCK_SIZE)

    @abstractclassmethod
    def draw(self, camera: Camera) -> None: pass

    @abstractclassmethod
    def update(self) -> None: pass

class Background(IGameObject):
    pass

class GameObject(IGameObject):

    def __init__(self, state: int, position: v2, taille: v2) -> None:
        self.state: int = state
        self.position: v2 = position 
        self.taille: v2 = taille
        self._mask = mask.Mask(self.taille, True)

    def update(self) -> None: ...
    
    def draw(self, camera: Camera) -> None: ...

    @property
    def position_matrix_top_left(self) -> v2:
        return self.position/GameConfig.BLOCK_SIZE

    @property
    def position_matrix_center(self) -> v2:
        return (self.position + self.taille/2)/GameConfig.BLOCK_SIZE

    @property
    def position_matrix_top_right(self) -> v2:
        return (self.position+v2(self.taille.x,0))/GameConfig.BLOCK_SIZE

    @property
    def position_matrix_bottom_left(self) -> v2:
        return (self.position+v2(0,self.taille.y))/GameConfig.BLOCK_SIZE
    
    @property
    def position_matrix_bottom_right(self) -> v2:
        return (self.position + self.taille)/GameConfig.BLOCK_SIZE

    @property
    def mask(self) -> Mask:
        return self._mask

    @mask.setter
    def mask(self, value: Mask) -> Mask:
        self._mask = value
        return self._mask

    @property
    def rect(self) -> Rect:
        return Rect(self.position, self.taille)

class Static(GameObject):
    
    def create(coord: tuple[int, int], id: int, state: int, uuid: int):
        return Static(state, v2(coord[1], coord[0]) * GameConfig.BLOCK_SIZE, v2(1, 1)*GameConfig.BLOCK_SIZE, Palette.get_texture(id, state))

    def __init__(self, state: int, position: v2, taille: v2, texture: Surface) -> None:
        GameObject.__init__(self, state, position, taille)
        self.texture: Surface = transform.scale(texture, self.taille)

    def draw(self,camera) -> None:
        rect = camera.transform_coord(self.rect)
        GameConfig.GAME_SURFACE.blit(self.texture, rect)

    @property
    def mask(self) -> Mask:
        return mask.from_surface(self.texture) 

class Dynamic(GameObject):

    def __init__(self, state: int, position: v2, taille:v2, animations: dict[str, list[Surface]]) -> None:
        GameObject.__init__(self, state, position,taille)

        self.animations: dict[str, list[Surface]] = animations
        self.animation_frame: int = 0
        self.current_animation: str = "idle"
        self.sante : int = 20
        self.santemax : int = 20
        self.is_flying : bool = True

        self.vitesse: v2 = v2(0.0, 0.0)
        self.acceleration: v2 = v2(0.0, 0.0)

    def draw(self,camera) -> None:
        rect = camera.transform_coord(self.rect)
        GameConfig.GAME_SURFACE.blit(self.texture, rect)

    @property
    def texture(self) -> Surface:
        return self.animations[self.current_animation][self.animation_frame]

EmptyElement: GameObject = GameObject(0, v2(0, 0), v2(0, 0))

class Ground(Static):
    
    def create(coord: tuple[int, int], id: int, index: int, uuid: int):
        return Ground(index, v2(coord[1], coord[0]) * GameConfig.BLOCK_SIZE, v2(1, 1)*GameConfig.BLOCK_SIZE, Palette.get_texture(id, index))

    def __init__(self, index: int, position: v2, taille: v2, texture: Surface) -> None:
        Static.__init__(self, index, position, taille, texture)

class LigthSource():
    def create(coord: tuple[int, int], id: int, state: int, uuid: int):
        return LigthSource(state, v2(coord[1] + 0.5, coord[0] + 0.5)*GameConfig.BLOCK_SIZE)

    def __init__(self) -> None:
        self.radius: int = 2*GameConfig.BLOCK_SIZE
        self.glow: tuple[int, int, int, int] = (230, 199, 119, 255)

    def draw(self, camera: Camera):
        rect = camera.transform_coord(self.rect)
        shader.draw_a_light(rect.center, self.glow, self.radius)

class Lamp(Static, LigthSource):

    def create(coord: tuple[int, int], id: int, state: int, uuid: int):
        return Lamp(id, state, v2(coord[1], coord[0])*GameConfig.BLOCK_SIZE, v2(1, 1)*GameConfig.BLOCK_SIZE)

    def __init__(self, id: int, state: int, position: v2, taille: v2) -> None:
        Static.__init__(self, state, position, taille, Palette.get_texture(id, state))
        LigthSource.__init__(self)

    def draw(self, camera: Camera) -> None:
        LigthSource.draw(self, camera)
        rect = camera.transform_coord(self.rect)
        GameConfig.GAME_SURFACE.blit(self.texture, rect)

class Player(Dynamic, LigthSource):
    
    __animation_sprites: list[list[str]] = [
        [f"assets/sprites/dynamics/GreenSlime/Grn_Idle{i}.png" for i in range(1,11)],
        [f"assets/sprites/dynamics/GreenSlime/Grn_HighJump{i}.png" for i in range(1,11)],
        [f"assets/sprites/dynamics/GreenSlime/Grn_Death{i}.png" for i in range(1,6)],
        [f"assets/sprites/dynamics/GreenSlime/Grn_Right{i}.png" for i in range(1,6)],
        [f"assets/sprites/dynamics/GreenSlime/Grn_Left{i}.png" for i in range(1,6)],
        [f"assets/sprites/dynamics/GreenSlime/Grn_Dmg{i}.png" for i in range(1,6)]
    ]

    def __init__(self, position: v2, taille: v2) -> None:
        state: int = 0
        self.status_frame: float = 0
        animations: dict[str, list[Surface]] = {
            "idle": [ transform.scale(image.load(src), (taille.x, taille.y)) for src in Player.__animation_sprites[0]],
            "jump": [ transform.scale(image.load(src), (taille.x, 3*taille.y)) for src in Player.__animation_sprites[1]],
            "death": [ transform.scale(image.load(src), (taille.x, taille.y)) for src in Player.__animation_sprites[2]],
            "right": [ transform.scale(image.load(src), (taille.x, taille.y)) for src in Player.__animation_sprites[3]],
            "left": [ transform.scale(image.load(src), (taille.x, taille.y)) for src in Player.__animation_sprites[4]],
            "damage": [ transform.scale(image.load(src), (taille.x, taille.y)) for src in Player.__animation_sprites[5]]
            # "attack": [ transform.scale(image.load(src), (taille.x, taille.y)) for src in Player.__animation_sprites[6]]
            # "fall": [ transform.scale(image.load(src), (taille.x, taille.y)) for src in Player.__animation_sprites[7]]
            # "interaction": [ transform.scale(image.load(src), (taille.x, taille.y)) for src in Player.__animation_sprites[8]]
        }
        super().__init__(state, position, taille, animations)
        Dynamic.__init__(self, state, position, taille, animations)
        LigthSource.__init__(self)
        self.glow = (178, 230, 119, 255)
        self._mask = mask.from_surface(animations["idle"][0])

    def update_frame(self, is_flying) -> None:
        self.status_frame = (self.status_frame+15*GameState.dt) % 10
        # jump_counter = 1

        # condition pour self.current_animation = "jump"
        # condition pour self.current_animation = "fall"

        # touches provisoires pour tester les frames
        if Input.is_pressed(pg.K_p):
            self.current_animation = "death"
        elif Input.is_pressed(pg.K_o):
            self.current_animation = "damage"
        # elif pressed[pg.K_i]:
        #     self.current_animation = "attack"
        # elif pressed[pg.K_u]:
        #     self.current_animation = "interaction"

        # propre
        elif Input.is_pressed(pg.K_d):
            self.current_animation = "right"
        elif Input.is_pressed(pg.K_q):
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

        self.status_frame -= GameState.dt
        self.animation_frame = int(self.status_frame)
        self.animation_frame = int(self.animation_frame % len(self.animations[self.current_animation]))

    def update(self) -> None:
        if Input.is_pressed(pg.K_d):
            self.acceleration.x += GameConfig.BLOCK_SIZE / GameState.dt * ( 1 - 0.75 * self.is_flying)

        if Input.is_pressed(pg.K_q):
            self.acceleration.x -= GameConfig.BLOCK_SIZE / GameState.dt * ( 1 - 0.75 * self.is_flying)

        if Input.is_pressed(pg.K_s) and self.is_flying:
            self.acceleration.y += GameConfig.BLOCK_SIZE / GameState.dt

        if Input.is_pressed(pg.K_z) and not self.is_flying:
            self.acceleration.y -= 20 * GameConfig.BLOCK_SIZE / GameState.dt
            self.is_flying = True

    def draw(self, camera: Camera) -> None:
        rect = camera.transform_coord(self.rect)
        LigthSource.draw(self, camera)
        GameConfig.GAME_SURFACE.blit(self.texture, rect)
