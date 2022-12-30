# À supprimer avant de merge

import pygame
from pygame import Rect, Color
from pygame import image, display
from pygame.time import Clock

from buttons import Button, ButtonManager
from button_script import ButtonScript
from assets import ASSET_DIR
from input import Input

from morgann_textes import Text
from config import GameConfig

from menu_screen import Menu


class Game:
    def __init__(self):
        self.should_quit = False


def button_example():

    pygame.init()

    game = Game()
    window = display.set_mode((500,500))
    clock = Clock()
    texture = image.load(f"{ASSET_DIR}/UI/button1.png")
    should_quit = False

    Input.init()
    Text.init(window, {"BradBunR": f"{GameConfig.FONT_DIR}/BradBunR.ttf"}, GameConfig.FONT_SIZE)
    ButtonManager.init(window)

    Bid = "bouton1"
    Button(Bid, "bonjour", Rect(10,10,100,100),ButtonScript(ButtonScript.print_mouse_pos, pygame.mouse),texture,alive=True,enabled=True,label_color=Color("red"))
    
    while not game.should_quit:
            #l'appel de get est important pour update notamment les inputs claviers 
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    game.should_quit = True

            Input.update()

            if Input.is_pressed_once(pygame.K_z):
                if ButtonManager.is_alive(Bid):
                    ButtonManager.kill(Bid)
                else:
                    ButtonManager.set_alive(Bid)

            window.fill("black")
            ButtonManager.update()
            display.update()

            clock.tick_busy_loop(70)

def menu_example():
    """il faut modifier les valeurs de la taille du menu dans menu_screen : Menu#__create_ingame_menu
    """

    pygame.init()

    game = Game()
    window = display.set_mode((500,500))
    clock = Clock()
    texture = image.load(f"{ASSET_DIR}/UI/button1.png")
    should_quit = False

    Input.init()
    Text.init(window, {"BradBunR": f"{GameConfig.FONT_DIR}/BradBunR.ttf"}, GameConfig.FONT_SIZE)
    ButtonManager.init(window)
    Menu.init(game)

    while not game.should_quit:
        #l'appel de get est important pour update notamment les inputs claviers 
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                game.should_quit = True

        Input.update()

        if Input.is_pressed_once(pygame.K_z):
            if Menu.is_open("ingame_pause"):
                Menu.close_menu("ingame_pause")
            else:
                Menu.open_menu("ingame_pause")

        window.fill("black")
        ButtonManager.update()
        display.update()

        clock.tick_busy_loop(70)


if __name__ == "__main__":
    # button_example()
    menu_example()
