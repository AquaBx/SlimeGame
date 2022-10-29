from cmath import rect
import pygame

class Entity:
    def __init__(self,x,y,w,h):
        self.rect = pygame.Rect(x,y,w,h)
        self.vitesse = pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)
