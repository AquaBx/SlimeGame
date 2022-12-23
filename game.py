import pygame
from config import Config
from camera import Camera
import world
#import debug
from morgann_textes import Messages
from menu_screen import Menu


World = world.World()

def game_loop(window):
    clock = pygame.time.Clock()
    quitting = False

    player = World.player
    blocks = World.blocks
    camera = Camera(player)

    back = Config.back
    msg = Messages()

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

    ## Partie des tests de fonction de Morgann
        LONG_TXT = "Ceci est un long long message qui va prendre plusieurs lignes et je ne sais pas quoi écrire pour prolonger ce texte mais je le prolonge quand même."
        FALLING_TXT = "You are falling !"
        IN_AIR_TXT = "Slime believes he can fly ! Slime believes he can touch the sky ! Slime..."
        font_size = 30

        msg.display_message(window,LONG_TXT,Config.WINDOW_W*0.6,40,font_size,msg.GREY,True)        
        if player.position.y > 888 : # Simples tests pour afficher des messages, ils seront à effacer avant la fin du projet
            msg.display_message(window,FALLING_TXT,Config.WINDOW_W*0.6,40,font_size,msg.RED,True)
        if player.position.y < 480 :
            msg.display_message(window,IN_AIR_TXT,Config.WINDOW_W*0.6,40,font_size,msg.GREEN,True)

        OPTIONS_MENU = ["Nouvelle partie (N)", "Charger une partie (C)", "Sauvegarder (S)", "Quitter (Q)"] # Attention au Q, qui sert déjà à aller vers la gauche
        MAIN_BACKGROUND_IMG = "main_background.JPG"
        IN_GAME_BACKGROUND_IMG = "in_game_background_dirt.png"
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_m] :
            Menu.display_main_menu(window,OPTIONS_MENU,MAIN_BACKGROUND_IMG)
        if keys_pressed[pygame.K_i] :
            Menu.display_ingame_menu(window,OPTIONS_MENU,IN_GAME_BACKGROUND_IMG)

    ## Fin de la partie de tests de fonctions

        # debug.debug(player.vitesse)
        pygame.display.update()
        clock.tick_busy_loop(Config.FPS)



if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((Config.WINDOW_W, Config.WINDOW_H))
    pygame.display.set_caption("Slime Game")
    game_loop(window)
    pygame.quit()
