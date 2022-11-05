from cmath import rect
import pygame

class Entity:
    def __init__(self,x,y,w,h,src):
        self.position = pygame.Vector2(x,y)
        self.vitesse = pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)
		
        self.taille = pygame.Vector2(w,h)
        self.texture = pygame.transform.scale(pygame.image.load(src), (w, h))