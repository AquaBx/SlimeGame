import pygame
from morgann_textes import Messages
from config import Config

class Menu :
    # Cette classe permet d'afficher deux menus : le menu principal de début de jeu et le menu en jeu

    # Menu principal contient :
    # Image de fond
    # n rectangles (n est variable, pas de hardcode !!!)
    # Dans les rectangles : "Nouvelle partie", "Quitter" ... 

    # pygame.draw.rect(window, pygame.Color(255, 0, 0), (230,250,100,50))

    def __init__(self) :
        print("init menu")
        self.adresse_fonte_blobbychug = "BLOBBYCHUG.ttf"
        pygame.font.init()

    def display_main_menu(window,options,background) :
        # options est le tableau contenant les string des options affichées dans les rectangles : options = ["Nouvelle partie (N)", "Charger une partie (C)", "Quitter (Q)"] (changeable)

        # Objectif de la fonction : afficher des rectangles avec les options, on met une image de fond qui recouvre la fenêtre
        
        messages = Messages()
        n_rect = len(options)
        intervalle = int(Config.WINDOW_H/(2*n_rect))
        longueur_x = int(0.35*Config.WINDOW_W)
        cote_gauche = int(0.325*Config.WINDOW_W)

        background_scaled = pygame.transform.scale(pygame.image.load(background), (Config.WINDOW_W, Config.WINDOW_H))
        window.blit(background_scaled,(0,0))

        for i in range (0,n_rect) :
            cote_haut = 10+int(intervalle/2)+i*intervalle*2
            pygame.draw.rect(window, pygame.Color('brown'), (cote_gauche, cote_haut, longueur_x, intervalle))
            messages.display_message(window, options[i], int(Config.WINDOW_W/2), cote_haut+int(intervalle/2), 30, pygame.Color('black'), False)


    def display_ingame_menu(window,options,background) :
        
        messages = Messages()
        n_rect = len(options)                               # Nombre de rectangles dans lesquels on affiche les options du menu
        intervalle = int((Config.WINDOW_H-20)/(2*n_rect))   # Intervalle vertical de pixels entre les rectangles
        #longueur_y = intervalle
        longueur_x = int(0.35*Config.WINDOW_W)              # Longueur horizontale de chaque rectangle
        cote_gauche = int(0.325*Config.WINDOW_W)            # Côté gauche de chaque rectangle

        # Pour le tracé de l'image de fond, 2 choix : rectangle uni ou image
        #pygame.draw.rect(window, pygame.Color('red'), (int(0.3*Config.WINDOW_W),10,int(0.4*Config.WINDOW_W),Config.WINDOW_H-20))

        background_scaled = pygame.transform.scale(pygame.image.load(background), (int(0.4*Config.WINDOW_W),Config.WINDOW_H-20))
        window.blit(background_scaled,(int(0.3*Config.WINDOW_W),10))

        for i in range (0,n_rect) :   # Affichage des textes des options
            cote_haut = 10+int(intervalle/2)+i*intervalle*2
            pygame.draw.rect(window, pygame.Color('blue'), (cote_gauche, cote_haut, longueur_x, intervalle))
            messages.display_message(window, options[i], int(Config.WINDOW_W/2), cote_haut+int(intervalle/2), 30, pygame.Color("black"), False)