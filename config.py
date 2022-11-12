import pygame


class Config:
    clock = pygame.time.Clock()

    WINDOW_H = 720
    WINDOW_W = 1280
    Y_PLATEFORM = 516

    BLOCK_SIZE = WINDOW_H / 12

    FPS = 144

    back = pygame.transform.scale(
        pygame.image.load("Assets/Background/BG-sky.png"), (WINDOW_W, WINDOW_H))
