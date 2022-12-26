from abc import ABC, abstractclassmethod
from xmlrpc.client import Boolean, boolean

import pygame as pg
from pygame import key, image, mask, transform,Color
from pygame import Vector2 as v2, Rect, Surface
from pygame.mask import Mask

from camera import Camera
from config import GameConfig, GameState
from input import Input
from assets.palette import Palette

import shader

class IGameObject(ABC):
    
    def create(coord: tuple[int, int], id: int, state: int, uuid: int, shinning):
        print(f"Create Default Game Object at coord {coord} (id: int - {id} ; state: int {state} ; uuid: int {uuid})")
        return GameObject(state, v2(coord[1], coord[0]) * GameConfig.BLOCK_SIZE, v2(1, 1) * GameConfig.BLOCK_SIZE, shinning)

    @abstractclassmethod
    def draw(self, camera: Camera) -> None: pass

    @abstractclassmethod
    def update(self) -> None: pass

class Background(IGameObject):
    pass

class GameObject(IGameObject):

    def __init__(self, state: int, position: v2, taille: v2, shinning:Boolean=False) -> None:
        self.state: int = state
        self.position: v2 = position 
        self.shinning:Boolean = shinning
        self.taille: v2 = taille
        self._mask = mask.Mask(self.taille, True)

    def update(self) -> None: pass
    
    def draw(self, camera: Camera) -> None:
        pass

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

    def __init__(self, state: int, position: v2, taille: v2, texture: Surface,shinning:Boolean) -> None:
        super().__init__(state, position, taille,shinning=shinning)
        self.texture: Surface = transform.scale(texture, self.taille)

    def draw(self,camera) -> None:
        rect = camera.transform_coord(self.rect)

        if self.shinning:
            shader.draw_a_ligth(rect.center,(230, 199, 119,255),int(2*GameConfig.BLOCK_SIZE))

        GameConfig.GAME_SURFACE.blit(self.texture, rect)

    @property
    def mask(self) -> Mask:
        return mask.from_surface(self.texture) 

class Dynamic(GameObject):

    def __init__(self, state: int, position: v2, taille:v2, animations: list[Surface],shinning=False) -> None:
        super().__init__(state, position,taille,shinning)

        self.animations: list[Surface] = animations
        self.animation_frame: int = 0
        self.sante : int = 20
        self.santemax : int = 20
        self.is_flying : bool = True

        self.vitesse: v2 = v2(0.0, 0.0)
        self.acceleration: v2 = v2(0.0, 0.0)

    def draw(self,camera) -> None:
        rect = camera.transform_coord(self.rect)

        if self.shinning:
            shader.draw_a_ligth(rect.center,(178, 230, 119,255),int(2*GameConfig.BLOCK_SIZE))

        GameConfig.GAME_SURFACE.blit(self.texture, rect)

    @property
    def texture(self) -> Surface:
        return self.animations[self.animation_frame]

class Empty(GameObject):
    def __init__(self, index: int, position: v2, taille:v2, shine=False) -> None:
        super().__init__(index, position, taille,shine)
    def update(self) -> None: pass

    @property
    def mask(self) -> Mask:
        mask = pg.mask.from_surface(pg.Surface((0,0)))
        return mask.scale((GameConfig.BLOCK_SIZE,GameConfig.BLOCK_SIZE))

EmptyElement: GameObject = GameObject(0, v2(0, 0), v2(0, 0))

class Ground(Static):
    
    def create(coord: tuple[int, int], id: int, index: int, uuid: int,shine:boolean):
        return Ground(index, v2(coord[1], coord[0]) * GameConfig.BLOCK_SIZE, v2(1, 1)*GameConfig.BLOCK_SIZE, Palette.get_texture(id, index),shine)

    def __init__(self, index: int, position: v2, taille: v2, texture: Surface,shine:Boolean) -> None:
        super().__init__(index, position, taille, texture,shine)

    def update(self) -> None: pass

class Player(Dynamic):

    def __init__(self, position: v2, taille: v2, spritesheet: list[str]) -> None:
        state: int = 0
        animations = [ transform.scale(image.load(src), (taille.x, taille.y)) for src in spritesheet ]

        super().__init__(state, position, taille, animations,True)

        self._mask = mask.from_surface(animations[0])

    def update_frame(self) -> None:
        self.animation_frame += 13*GameState.dt
        self.animation_frame = int(self.animation_frame % len(self.animations))

    def update(self) -> None:


        if Input.is_pressed(pg.K_d):
            self.acceleration.x += GameConfig.BLOCK_SIZE / GameState.dt

        if Input.is_pressed(pg.K_q):
            self.acceleration.x -= GameConfig.BLOCK_SIZE / GameState.dt

        if Input.is_pressed(pg.K_s) and self.is_flying:
            self.acceleration.y += 35 * GameConfig.BLOCK_SIZE / GameState.dt

        if Input.is_pressed(pg.K_z) and not self.is_flying:
            self.acceleration.y -= 35 * GameConfig.BLOCK_SIZE / GameState.dt
            self.is_flying = True
