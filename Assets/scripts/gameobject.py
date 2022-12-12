from abc import ABC, abstractclassmethod

import pygame as pg
from pygame import key, image, mask, transform
from pygame import Vector2 as v2, Rect, Surface
from pygame.mask import Mask

from camera import Camera
from config import GameConfig, GameState

class IGameObject(ABC):

    @abstractclassmethod
    def draw(self, camera: Camera) -> None: pass

    @abstractclassmethod
    def update(self) -> None: pass

class GameObject(IGameObject):

    def __init__(self, state: int, position: v2, taille: v2) -> None:
        self.state: int = state
        self.position: v2 = position
        self.taille: v2 = taille

    def update(self) -> None: pass
    def draw(self, camera: Camera) -> None: pass

    @property
    def rect(self) -> Rect:
        return Rect(self.position, self.taille)

class Static(GameObject):

    def __init__(self, state: int, position: v2, taille: v2, texture: Surface) -> None:
        super().__init__(state, position, taille)
        self.texture: Surface = texture
        self.mask: Mask = mask.from_surface(texture)

    def draw(self, camera: Camera) -> None:
        rect = camera.transform_coord(self.rect)
        GameConfig.WINDOW.blit(self.texture, rect)

class Dynamic(GameObject):

    def __init__(self, state: int, position: v2, taille: v2, animations: list[Surface]) -> None:
        super().__init__(state, position, taille)

        self.animations: list[Surface] = animations
        self.animation_frame: int = 0

        self.vitesse: v2 = v2(0.0, 0.0)
        self.acceleration: v2 = v2(0.0, 0.0)

    @property
    def texture(self) -> Surface:
        return self.animations[self.animation_frame]

    @property
    def mask(self) -> Mask:
        return mask.from_surface(self.texture) 
    
    def draw(self, camera: Camera) -> None:
        rect = camera.transform_coord(self.rect)
        GameConfig.WINDOW.blit(self.texture, rect)

class Empty(GameObject):
    def __init__(self, index: int, position: v2) -> None:
        taille = v2(GameConfig.BLOCK_SIZE,GameConfig.BLOCK_SIZE)
        super().__init__(index, position, taille)
    def update(self) -> None: pass

    @property
    def mask(self) -> Mask:
        return mask.Mask.clear()

class Ground(Static):

    def __init__(self, index: int, position: v2, src: str) -> None:
        texture = transform.scale(image.load(src), (GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE))
        taille = v2(GameConfig.BLOCK_SIZE,GameConfig.BLOCK_SIZE)

        super().__init__(index, position, taille, texture)

    def update(self) -> None: pass

class Player(Dynamic):

    def __init__(self, x: float, y: float, w: int, h: int, spritesheet: list[str]) -> None:
        state: int = 0
        position = v2(x, y)
        taille = v2(w, h)
        animations = [ transform.scale(image.load(src), (w, h)) for src in spritesheet ]

        super().__init__(state, position, taille, animations)

    def update_frame(self) -> None:
        self.animation_frame += 13*GameState.dt
        self.animation_frame = int(self.animation_frame % len(self.animations))

    def update(self) -> None:
        keys_pressed = key.get_pressed()

        self.acceleration.x = -self.vitesse.x * 1000 / GameConfig.BLOCK_SIZE
        self.acceleration.y = 0

        if keys_pressed[pg.K_d]:
            self.acceleration.x += 2 * GameConfig.BLOCK_SIZE / GameState.dt

        if keys_pressed[pg.K_q]:
            self.acceleration.x -= 2 * GameConfig.BLOCK_SIZE / GameState.dt

        # if keys_pressed[pygame.K_z]:
        #     self.acceleration.y -= 2/10 * Config.BLOCK_SIZE / Config.dt

        # if keys_pressed[pygame.K_s]:
        #     self.acceleration.y += 2/10 * Config.BLOCK_SIZE / Config.dt

        # self.vitesse.y += self.acceleration.y * Config.dt
        # self.position.y += self.vitesse.y * Config.dt

        self.vitesse.x += self.acceleration.x * GameState.dt
        self.position.x += self.vitesse.x * GameState.dt
