import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, w, h):
        super().__init__(groups)
        self.image = (pygame.transform.scale(pygame.image.load("Assets/Tileset/tileMain2.png"), (w, h))).convert_alpha()
        self.position = pygame.Vector2(pos[0],pos[1])
        self.taille = pygame.Vector2(w,h)
        self.rect = self.image.get_rect(topleft=pos)