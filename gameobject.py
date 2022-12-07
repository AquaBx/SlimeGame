import string
import pygame
from camera import Camera
from config import GameConfig,GameState
from abc import ABC, abstractclassmethod

class IGameObject(ABC):
    @abstractclassmethod
    def draw(self, camera:Camera) -> None: pass

    @abstractclassmethod
    def update(self) -> None: pass
    
class GameObject(IGameObject):
    def __init__(self, state:int, position:pygame.Vector2, taille:pygame.Vector2) -> None:
        self.state = state
        self.position = position
        self.taille = taille

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.position,self.taille) 

class Static(GameObject):
    def __init__(self, state:int, position:pygame.Vector2, taille:pygame.Vector2, texture:pygame.Surface) -> None:
        super().__init__(state, position,taille)
        self.texture = texture
        self.mask = pygame.mask.from_surface( texture )

    def draw(self,camera:Camera) -> None:
        rect = camera.transform_coord(self.rect)
        GameConfig.WINDOW.blit(self.texture,rect)

class Dynamic(GameObject):
    def __init__(self, state:int, position:pygame.Vector2, taille:pygame.Vector2, animations:list[pygame.Surface]) -> None:
        super().__init__(state, position,taille)

        self.animations = animations
        self.animation_frame = 0

        self.vitesse = pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)
    
    @property
    def texture(self) -> pygame.Surface:
        return self.animations[ int( self.animation_frame ) ]

    @property
    def mask(self) -> pygame.Mask:
        return pygame.mask.from_surface( self.texture ) 
    
    def draw(self,camera:Camera) -> None:
        rect = camera.transform_coord(self.rect)
        GameConfig.WINDOW.blit(self.texture,rect)

class Ground(Static):
    def __init__(self,index:int, position:pygame.Vector2, src:string) -> None:
        texture = pygame.transform.scale(pygame.image.load(src), (GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE))
        taille = pygame.Vector2(GameConfig.BLOCK_SIZE,GameConfig.BLOCK_SIZE)

        super().__init__(index, position,taille,texture)

    def update(self) -> None: pass

class Player(Dynamic):

    def __init__(self, x:float, y:float, w:int, h:int, idle_srcs:list[string]) -> None:
        position = pygame.Vector2(x, y)
        taille = pygame.Vector2(w, h)
        animations = [ pygame.transform.scale(pygame.image.load(src), (w, h)) for src in idle_srcs ]

        super().__init__(True,position,taille,animations)

    def update_frame(self) -> None:
        self.animation_frame += 13*GameState.dt
        self.animation_frame = self.animation_frame % len(self.animations)

    def update(self) -> None:
        keys_pressed = pygame.key.get_pressed()

        self.acceleration.x = -self.vitesse.x * 1000 / GameConfig.BLOCK_SIZE
        self.acceleration.y = 0

        if keys_pressed[pygame.K_d]:
            self.acceleration.x += 2 * GameConfig.BLOCK_SIZE / GameState.dt

        if keys_pressed[pygame.K_q]:
            self.acceleration.x -= 2 * GameConfig.BLOCK_SIZE / GameState.dt

        # if keys_pressed[pygame.K_z]:
        #     self.acceleration.y -= 2/10 * Config.BLOCK_SIZE / Config.dt

        # if keys_pressed[pygame.K_s]:
        #     self.acceleration.y += 2/10 * Config.BLOCK_SIZE / Config.dt

        # self.vitesse.y += self.acceleration.y * Config.dt
        # self.position.y += self.vitesse.y * Config.dt

        self.vitesse.x += self.acceleration.x * GameState.dt
        self.position.x += self.vitesse.x * GameState.dt
    