from turtle import back
import pygame
from config import Config 
from block import Block
from camera import Camera
from entity import Entity

def game_loop(window):
    quitting=False
    clock = pygame.time.Clock()

    blocks = [ Block(Config.BLOCK_SIZE*i,Config.WINDOW_H-Config.BLOCK_SIZE,Config.BLOCK_SIZE,Config.BLOCK_SIZE,True,f'Assets/Tileset/tileMain{2}.png') for i in range(1,20) ]
    
    player = Entity(10*Config.BLOCK_SIZE,Config.WINDOW_H-2*Config.BLOCK_SIZE,Config.BLOCK_SIZE,Config.BLOCK_SIZE,"Assets/GreenSlime/Grn_Idle1.png")
    camera = Camera(player)

    back = pygame.transform.scale(pygame.image.load("Assets/Background/BG-sky.png"), (1920, 1080))

    while not quitting:
        dt = 1/clock.get_fps() if clock.get_fps() != 0 else 1/Config.FPS
        
        camera.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting=True

        keys_pressed = pygame.key.get_pressed()

        player.acceleration.x = - player.vitesse.x*1000/Config.BLOCK_SIZE
        player.acceleration.y = - player.vitesse.y*1000/Config.BLOCK_SIZE

        if keys_pressed[pygame.K_d]:
            player.acceleration.x += 2*Config.BLOCK_SIZE/dt

        if keys_pressed[pygame.K_q]:
            player.acceleration.x -= 2*Config.BLOCK_SIZE/dt

        if keys_pressed[pygame.K_z]:
            player.acceleration.y -= 2*Config.BLOCK_SIZE/dt

        if keys_pressed[pygame.K_s]:
            player.acceleration.y += 2*Config.BLOCK_SIZE/dt

        player.vitesse.y += player.acceleration.y*dt
        player.position.y += player.vitesse.y*dt

        player.vitesse.x += player.acceleration.x*dt
        player.position.x += player.vitesse.x*dt

        window.blit(back,(0,0))

        for block in blocks:
            ncoord = ( block.position.x-camera.position.x+Config.WINDOW_W/2 , block.position.y-camera.position.y+Config.WINDOW_H/2 )
            window.blit(block.texture,ncoord)
        
        ncoord = ( player.position.x-camera.position.x+Config.WINDOW_W/2-player.taille.x/2 , player.position.y-camera.position.y+Config.WINDOW_H/2)
        window.blit(player.texture,ncoord)

        pygame.display.flip()
        clock.tick_busy_loop(Config.FPS)


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((Config.WINDOW_W,Config.WINDOW_H),pygame.FULLSCREEN)
    pygame.display.set_caption("Premier Jeu")
    game_loop(window)
    pygame.quit()