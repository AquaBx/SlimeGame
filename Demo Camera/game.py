import pygame
from config import Config 
from block import Block
from camera import Camera
from entity import Entity

def game_loop(window):
    quitting=False
    clock = pygame.time.Clock()

    blocks = [ Block(Config.BLOCK_SIZE*i,Config.WINDOW_H-Config.BLOCK_SIZE,Config.BLOCK_SIZE,Config.BLOCK_SIZE,True,"Assets/Tileset/tileMain2.png") for i in range(0,22) ]
    
    player = Entity(10*Config.BLOCK_SIZE,Config.WINDOW_H-3*Config.BLOCK_SIZE,2*Config.BLOCK_SIZE,2*Config.BLOCK_SIZE)
    camera = Camera(player)

    while not quitting:
        dt = 1/clock.get_fps() if clock.get_fps() != 0 else 1/Config.FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting=True

        keys_pressed = pygame.key.get_pressed()
        window.fill(pygame.Color(0,0,0))

        for block in blocks:

            ncoord = ( block.rect.left-camera.rect.left+Config.WINDOW_W/2 , block.rect.top-camera.rect.top+Config.WINDOW_H/2 )
            window.blit(block.texture,ncoord)
        
        color = pygame.Color(255,0,0)
        ncoord = ( player.rect.left-camera.rect.left+Config.WINDOW_W/2 , player.rect.top-camera.rect.top+Config.WINDOW_H/2 , player.rect.width, player.rect.height)
        pygame.draw.rect(window,color, ncoord)

        player.rect.left+=1

        pygame.display.flip()
        clock.tick_busy_loop(Config.FPS)


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode(size=(Config.WINDOW_W,Config.WINDOW_H))
    pygame.display.set_caption("Premier Jeu")
    game_loop(window)
    pygame.quit()