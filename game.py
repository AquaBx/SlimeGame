from turtle import back
import pygame
from config import Config
from block import Block
from camera import Camera
from entity import Entity


def game_loop(window):
    clock = pygame.time.Clock()
    quitting = False
    player = Entity.implement_player()
    camera = Camera(player)

    blocks = Block.implement_blocks()

    back = Config.back

    while not quitting:

        camera.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True

        player.move()

        window.blit(back, (0, 0))

        Block.blit_blocks(blocks, window, camera.position.x, camera.position.y)

        player.blit_player(window, camera.position.x, camera.position.y)

        pygame.display.flip()

        clock.tick_busy_loop(Config.FPS)


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((Config.WINDOW_W, Config.WINDOW_H))
    pygame.display.set_caption("Premier Jeu")
    game_loop(window)
    pygame.quit()
