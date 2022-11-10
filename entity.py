from cmath import rect
import pygame
from config import *
from camera import Camera

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
        self.acceleration.y = -self.vitesse.y * 1000 / Config.BLOCK_SIZE

        if keys_pressed[pygame.K_d]:
            self.acceleration.x += 2 * Config.BLOCK_SIZE / dt

        if keys_pressed[pygame.K_q]:
            self.acceleration.x -= 2 * Config.BLOCK_SIZE / dt

        if keys_pressed[pygame.K_z]:
            self.acceleration.y -= 2 * Config.BLOCK_SIZE / dt

        if keys_pressed[pygame.K_s]:
            self.acceleration.y += 2 * Config.BLOCK_SIZE / dt

        self.vitesse.y += self.acceleration.y * dt
        self.position.y += self.vitesse.y * dt

        self.vitesse.x += self.acceleration.x * dt
        self.position.x += self.vitesse.x * dt

        self.rect.topleft = self.position

    def blit_player(self, window, x_cam, y_cam):
        ncoord = (self.rect.left/2 + self.rect.right / 2 - x_cam + Config.WINDOW_W / 2,
                  self.rect.top + - y_cam + Config.WINDOW_H / 2)
        window.blit(self.texture, ncoord)
