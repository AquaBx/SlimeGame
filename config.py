import pygame

class GameConfig:
    WINDOW_SIZE = pygame.Vector2(1280,720)
    WINDOW = pygame.display.set_mode((WINDOW_SIZE.x, WINDOW_SIZE.y))
    BLOCK_SIZE = WINDOW_SIZE.y / 12
    FPS = 144

class GameState:
    dt = 1/60