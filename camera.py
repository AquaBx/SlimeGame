import pygame


class Camera:

    def __init__(self, link):
        self.link = link
        self.rect = link.rect

    def update(self):
        self.rect = self.link.rect
