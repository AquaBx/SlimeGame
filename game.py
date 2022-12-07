import pygame
from config import GameConfig,GameState
from camera import Camera
import world
import debug

World = world.World()

def game_loop():
    clock = pygame.time.Clock()
    quitting = False

    camera = Camera(World.player)

    while not quitting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True

        GameState.dt = 1 / clock.get_fps() if clock.get_fps() != 0 else 1 / GameConfig.FPS
        GameConfig.WINDOW.blit(World.background, (0, 0))

        camera.update()
        World.update(camera)

        debug.debug(clock.get_fps())
        pygame.display.update()

        clock.tick_busy_loop(GameConfig.FPS)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Premier Jeu")
    game_loop()
    pygame.quit()
