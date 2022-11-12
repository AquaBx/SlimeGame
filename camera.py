import pygame
from config import Config

class Camera:

    def __init__(self, link):
        self.link = link

    def update(self):
        """
        update le rect de la caméra en centrant le link par rapport à celle-ci
        """
        xcam = (self.link.rect.right + self.link.rect.left)/2
        ycam = (self.link.rect.top + self.link.rect.bottom)/2
        self.rect = pygame.Rect (  xcam , ycam , 1 , 1 )
    
    def convert_coord(self,rect):
        """
        fonction qui va prendre en paramètre un rect d'un objet (entité ou block)
        et qui va ré-envoyer un nouveau rect de cet objet là ou il doit être dessiné à l'écran
        """
        
        newx = rect.left - self.rect.left + Config.WINDOW_W/2
        newy = rect.top - self.rect.top + Config.WINDOW_H/2

        return pygame.Rect( newx , newy, rect.width, rect.height ) 