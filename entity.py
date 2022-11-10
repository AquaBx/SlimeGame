from cmath import rect
import pygame
from config import *
from camera import Camera


class Entity:

    def __init__(self, x, y, w, h, src):
        self.position = pygame.Vector2(x, y)
        self.vitesse = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

        self.taille = pygame.Vector2(w, h)
        self.texture = pygame.transform.scale(pygame.image.load(src), (w, h))

    def implement_player():
        return Entity(10 * Config.BLOCK_SIZE,
                      Config.WINDOW_H - 2 * Config.BLOCK_SIZE,
                      Config.BLOCK_SIZE, Config.BLOCK_SIZE,
                      "Assets/GreenSlime/Grn_Idle1.png")

    def move(self):
        keys_pressed = pygame.key.get_pressed()

        self.acceleration.x = -self.vitesse.x * 1000 / Config.BLOCK_SIZE
        self.acceleration.y = -self.vitesse.y * 1000 / Config.BLOCK_SIZE

        if keys_pressed[pygame.K_d]:
            self.acceleration.x += 2 * Config.BLOCK_SIZE / Config.dt

        if keys_pressed[pygame.K_q]:
            self.acceleration.x -= 2 * Config.BLOCK_SIZE / Config.dt

        if keys_pressed[pygame.K_z]:
            self.acceleration.y -= 2 * Config.BLOCK_SIZE / Config.dt

        if keys_pressed[pygame.K_s]:
            self.acceleration.y += 2 * Config.BLOCK_SIZE / Config.dt

        self.vitesse.y += self.acceleration.y * Config.dt
        self.position.y += self.vitesse.y * Config.dt

        self.vitesse.x += self.acceleration.x * Config.dt
        self.position.x += self.vitesse.x * Config.dt

    def blit_player(self, window, x_cam, y_cam):
        ncoord = (self.position.x - x_cam + Config.WINDOW_W / 2 -
                  self.taille.x / 2,
                  self.position.y - y_cam + Config.WINDOW_H / 2)
        window.blit(self.texture, ncoord)
