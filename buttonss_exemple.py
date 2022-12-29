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


pygame.init()

window = display.set_mode((500,500))
clock = Clock()
texture = image.load(f"{ASSET_DIR}/UI/button1.png")
should_quit = False

Input.init()
ButtonManager.init(window)
Text.init({"BradBunR": f"{GameConfig.FONT_DIR}/BradBunR.ttf"}, GameConfig.FONT_SIZE)

b = Button("bouton1", "bonjour", Rect(10,10,100,100),ButtonScript(ButtonScript.print_mouse_pos, pygame.mouse),texture,alive=True,enabled=True,label_color=Color("red"))

while not should_quit:
    #l'appel de get est important pour update notamment les inputs claviers 
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            should_quit = True

    Input.update()

    if Input.is_pressed_once(pygame.K_z):
        if ButtonManager.is_alive(b.id):
            ButtonManager.kill(b.id)
        else:
            ButtonManager.set_alive(b.id)

    window.fill("black")
    ButtonManager.update()
    display.update()

    clock.tick_busy_loop(70)
