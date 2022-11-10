import pygame
from config import Config
from camera import *


class Block:

    def __init__(self, x, y, w, h, solide, src):
        self.texture = pygame.transform.scale(pygame.image.load(src), (w, h))
        self.position = pygame.Vector2(x, y)
        self.taille = pygame.Vector2(w, h)
        self.solide = solide

    def draw(self, window):
        window.blit(self.texture, self.rect.topleft)

    def implement_blocks():
        return [
            Block(Config.BLOCK_SIZE * i, Config.WINDOW_H - Config.BLOCK_SIZE,
                  Config.BLOCK_SIZE, Config.BLOCK_SIZE, True,
                  f'Assets/Tileset/tileMain{2}.png') for i in range(1, 20)
        ]

    def blit_blocks(blocks, window, x_cam, y_cam):
        for block in blocks:
            ncoord = (block.position.x - x_cam + Config.WINDOW_W / 2,
                      block.position.y - y_cam + Config.WINDOW_H / 2)
            window.blit(block.texture, ncoord)
