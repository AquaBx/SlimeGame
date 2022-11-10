import pygame


class Camera:

    def __init__(self, link):
        self.link = link
        self.position = pygame.Vector2(0, 0)

    def update(self):
        self.position.x = self.link.position.x
        self.position.y = self.link.position.y
