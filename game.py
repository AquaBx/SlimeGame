from morgann_textes import Messages
from menu_screen import Menu

import pygame as pg
from pygame.time import Clock

from config import GameConfig, GameState
from input import Input
from world import World

class Game:
    def __init__(self) -> None:
        pg.init();
        GameConfig.initialise()
        Input.init()
        self.clock: Clock = Clock()
        self.should_quit: bool = False
        # il faudra donner un entier qui correspond au fichier de sauvegarde demandé (1, 2 ou 3 sans doute)
        self.world: World = World(1)
        self.paused = False

    def __del__(self) -> None:
        pg.quit()

    def loop(self) -> None:
        while not self.should_quit:
            GameState.dt = 1 / self.clock.get_fps() if self.clock.get_fps() != 0 else 1 / GameConfig.FPS
            GameConfig.WINDOW.fill('Black')
            self.__process_events()
            if self.paused:
                OPTIONS_MENU = ["Nouvelle partie (N)", "Charger une partie (C)", "Sauvegarder (S)", "Quitter (Q)"] # Attention au Q, qui sert déjà à aller vers la gauche
                MAIN_BACKGROUND_IMG = "main_background.JPG"
                Menu.display_main_menu(GameConfig.WINDOW,OPTIONS_MENU,MAIN_BACKGROUND_IMG)
            else:
                self.__update()
                self.__draw()
                # self.morgann()

            pg.display.update()
            self.clock.tick_busy_loop(GameConfig.FPS)


    def morgann(self):
        msg = Messages()
        ## Partie des tests de fonction de Morgann
        LONG_TXT = "Ceci est un long long message qui va prendre plusieurs lignes et je ne sais pas quoi écrire pour prolonger ce texte mais je le prolonge quand même."
        FALLING_TXT = "You are falling !"
        IN_AIR_TXT = "Slime believes he can fly ! Slime believes he can touch the sky ! Slime..."
        font_size = 30

        msg.display_message(GameConfig.WINDOW,LONG_TXT,GameConfig.WINDOW_SIZE.x*0.6,40,font_size,msg.GREY,True)        
        if self.world.player.position.y > 888 : # Simples tests pour afficher des messages, ils seront à effacer avant la fin du projet
            msg.display_message(GameConfig.WINDOW,FALLING_TXT,GameConfig.WINDOW_SIZE.x*0.6,40,font_size,msg.RED,True)
        if self.world.player.position.y < 480 :
            msg.display_message(GameConfig.WINDOW,IN_AIR_TXT,GameConfig.WINDOW_SIZE.x*0.6,40,font_size,msg.GREEN,True)

        

    def __process_events(self) -> None:
        keypressed = pg.key.get_pressed()
        if keypressed[pg.K_ESCAPE]:
            self.paused = not ( self.paused )
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                self.should_quit = True

    def __update(self) -> None:
        self.world.update()

    def __draw(self) -> None:
        self.world.draw()

# to avoid global variable instances in main function
def main() -> None:
    Game().loop()

if __name__ == "__main__":
    main()
