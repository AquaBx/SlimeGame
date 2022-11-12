import pygame
from config import *

class Entity:

    def __init__(self, x, y, w, h, src):
        self.position = pygame.Vector2(x, y)
        self.vitesse = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

        self.rect = pygame.Rect(self.position,(w, h))
        self.texture = pygame.transform.scale(pygame.image.load(src), (w, h))
        self.mask = pygame.mask.from_surface( self.texture ) 

    def move(self,dt):
        keys_pressed = pygame.key.get_pressed()

        self.acceleration.x = -self.vitesse.x * 1000 / Config.BLOCK_SIZE
        self.acceleration.y = 0

        if keys_pressed[pygame.K_d]:
            self.acceleration.x += 2 * Config.BLOCK_SIZE / dt

        if keys_pressed[pygame.K_q]:
            self.acceleration.x -= 2 * Config.BLOCK_SIZE / dt

        # if keys_pressed[pygame.K_z]:
        #     self.acceleration.y -= 2/10 * Config.BLOCK_SIZE / dt

        # if keys_pressed[pygame.K_s]:
        #     self.acceleration.y += 2/10 * Config.BLOCK_SIZE / dt

        # self.vitesse.y += self.acceleration.y * dt
        # self.position.y += self.vitesse.y * dt

        self.vitesse.x += self.acceleration.x * dt
        self.position.x += self.vitesse.x * dt

        self.rect.topleft = self.position

    def blit_player(self, window, camera):
        ncoord = camera.convert_coord(self.rect)
        window.blit(self.texture, ncoord)
