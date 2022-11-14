import pygame
from config import Config
from camera import Camera
import world
import debug
from morgann_textes import Messages


World = world.World()

def game_loop(window):
    clock = pygame.time.Clock()
    quitting = False

    player = World.player
    blocks = World.blocks
    camera = Camera(player)

    back = Config.back
    msg = Messages()
    text = "Hello World"

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

        #créer une condition pour afficher un message (astuce, panneau, dialogue...), ainsi que la possibilté de modifier le contenu du message
        FALLING_TXT = "You are falling !"
        IN_AIR_TXT = "Slime believes he can fly !"
        if player.position.y > 516 : # Simple test pour afficher le message selon une condition particulière, il sera à effacer
            msg.display_message(window,FALLING_TXT,Config.WINDOW_W*0.8,30,40,(0,255,255))
        if player.position.y < 560 :
            msg.display_message(window,IN_AIR_TXT,Config.WINDOW_W*0.8,30,50,msg.GREY)

        # debug.debug(player.vitesse)
        pygame.display.update()
        clock.tick_busy_loop(Config.FPS)



if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((Config.WINDOW_W, Config.WINDOW_H))
    pygame.display.set_caption("Slime Game")
    game_loop(window)
    pygame.quit()
