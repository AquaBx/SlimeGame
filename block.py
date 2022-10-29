import pygame

class Block :
    def __init__(self,x,y,w,h,solide,src):
        self.texture = pygame.transform.scale(pygame.image.load(src), (w, h))
        self.rect = pygame.Rect(x,y,w,h)
        self.solide = solide
    
    def draw(self,window) :
        window.blit(self.texture,self.rect.topleft)