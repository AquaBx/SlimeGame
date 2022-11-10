from turtle import back
import pygame
from config import Config
from camera import Camera
import world

World = world.World()

def game_loop(window):
    clock = pygame.time.Clock()
    quitting = False

    player = World.player
    blocks = World.blocks
    camera = Camera(player)

    back = Config.back

    while not quitting:
        camera.update()
        dt = 1 / clock.get_fps() if clock.get_fps() != 0 else 1 / Config.FPS


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True

        player.move(dt)
        World.gravite(player,dt)


        window.blit(back, (0, 0))

        for block in blocks:
            ncoord = (block.rect.left - camera.rect.left + Config.WINDOW_W / 2,
                      block.rect.top - camera.rect.top + Config.WINDOW_H / 2)
            window.blit(block.texture, ncoord)

        player.blit_player(window, camera)

        pygame.display.flip()

        clock.tick_busy_loop(Config.FPS)


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((Config.WINDOW_W, Config.WINDOW_H))
    pygame.display.set_caption("Premier Jeu")
    game_loop(window)
    pygame.quit()
