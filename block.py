import pygame
from config import Config
from camera import *


class Block:

    def __init__(self, x, y, w, h, solide, src):
        self.texture = pygame.transform.scale(pygame.image.load(src), (w, h))
        self.mask = pygame.mask.from_surface( self.texture ) 
        self.rect = pygame.Rect(x,y,w,h) 
        
        self.position = pygame.Vector2(x, y)
        self.taille = pygame.Vector2(w, h)
        self.solide = solide
    def draw(self, window):
        window.blit(self.texture, self.rect.topleft)
