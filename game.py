from turtle import back
import pygame
from config import Config
from camera import Camera
import world
import debug

World = world.World()

def game_loop(window):
    clock = pygame.time.Clock()
    quitting = False

    player = World.player
    blocks = World.blocks
    camera = Camera(player)

    back = Config.back

    while not quitting:
        dt = 1 / clock.get_fps() if clock.get_fps() != 0 else 1 / Config.FPS
        window.blit(back, (0, 0))

        camera.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True


        player.move(dt)
        World.gravite(player,dt)

        player.blit_player(window, camera)

        # square_mid = pygame.Rect((Config.WINDOW_W-Config.BLOCK_SIZE)/2,(Config.WINDOW_H-Config.BLOCK_SIZE)/2,Config.BLOCK_SIZE,Config.BLOCK_SIZE)
        # pygame.draw.rect(window,pygame.Color(255,0,0),square_mid,)
        
        for block in blocks:
            ncoord = camera.convert_coord(block.rect)
            window.blit(block.texture, ncoord)

        # debug.debug(player.vitesse)
        pygame.display.update()
        clock.tick_busy_loop(Config.FPS)



if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((Config.WINDOW_W, Config.WINDOW_H))
    pygame.display.set_caption("Premier Jeu")
    game_loop(window)
    pygame.quit()
