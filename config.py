import pygame


class Config:
    clock = pygame.time.Clock()

    WINDOW_H = 800
    WINDOW_W = 1200
    Y_PLATEFORM = 516

    BLOCK_SIZE = WINDOW_H / 12

    FPS = 144

    back = pygame.transform.scale(
        pygame.image.load("Assets/Background/BG-sky.png"), (1920, 1080))
