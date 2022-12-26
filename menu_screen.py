import pygame
from morgann_textes import Messages
from config import Config

class Menu :
    # Cette classe permet d'afficher deux menus : le menu principal hors-partie et le menu en jeu

    # Le menu principal contient :
        # Une image de fond
        # Un rectangle par option de menu
        # Dans chaque rectangle, on affiche une option

    def __init__(self) :
        self.adresse_fonte_blobbychug = "BLOBBYCHUG.ttf"    # On donne l'adresse de la fonte de texte utilisée
        pygame.font.init()                                  # On initialise la fonte

    def display_main_menu(window,options,background) :  # Fonction permettant d'afficher le menu principal
        # options est le tableau contenant les string des options affichées dans les rectangles : options = ["Continuer (C)", "Nouvelle partie (N)", "Charger une partie (H)", "Sauvegarder (S)", "Quitter (Q)"]
        
        messages = Messages()
        n_rect = len(options)                           # Nombre de rectangles dans lesquels on affiche les options du menu
        intervalle = int(Config.WINDOW_H/(2*n_rect))    # Intervalle vertical de pixels entre les rectangles
        longueur_x = int(0.35*Config.WINDOW_W)          # Longueur horizontale de chaque rectangle
        cote_gauche = int(0.325*Config.WINDOW_W)        # Côté gauche de chaque rectangle

        background_scaled = pygame.transform.scale(pygame.image.load(background), (Config.WINDOW_W, Config.WINDOW_H))   # On met l'image de fond à l'échelle de la fenêtre de jeu 
        window.blit(background_scaled,(0,0))                                                                            # On affiche l'image de fond sur la fenêtre

        for i in range (0,n_rect) :
            cote_haut = 10+int(intervalle/2)+i*intervalle*2                                                                                         # On détermine le côté haut des rectagnles un par un
            pygame.draw.rect(window, pygame.Color('brown'), (cote_gauche, cote_haut, longueur_x, intervalle))                                       # On dessine les rectangles
            messages.display_message(window, options[i], int(Config.WINDOW_W/2), cote_haut+int(intervalle/2), 30, pygame.Color('black'), False)     # On affiche le texte de l'option


    def display_ingame_menu(window,options,background) :    # Fonction permettant d'afficher le menu en jeu
        
        messages = Messages()
        n_rect = len(options)                               # Nombre de rectangles dans lesquels on affiche les options du menu
        intervalle = int((Config.WINDOW_H-20)/(2*n_rect))   # Intervalle vertical de pixels entre les rectangles
        longueur_x = int(0.35*Config.WINDOW_W)              # Longueur horizontale de chaque rectangle
        cote_gauche = int(0.325*Config.WINDOW_W)            # Côté gauche de chaque rectangle

        # Pour le tracé de l'image de fond, 2 choix : rectangle uni ou image
        #pygame.draw.rect(window, pygame.Color('red'), (int(0.3*Config.WINDOW_W),10,int(0.4*Config.WINDOW_W),Config.WINDOW_H-20))   # Affichage du fond uni

        background_scaled = pygame.transform.scale(pygame.image.load(background), (int(0.4*Config.WINDOW_W),Config.WINDOW_H-20))    # Mise à l'échelle d'une image de fond (menu central ne recouvrant pas toute la fenêtre)
        window.blit(background_scaled,(int(0.3*Config.WINDOW_W),10))                                                                # Affichage du menu central

        for i in range (0,n_rect) :   # Affichage des textes des options
            cote_haut = 10+int(intervalle/2)+i*intervalle*2                                                                                     # On détermine le côté haut des rectagnles un par un
            pygame.draw.rect(window, pygame.Color('blue'), (cote_gauche, cote_haut, longueur_x, intervalle))                                    # On dessine les rectangles
            messages.display_message(window, options[i], int(Config.WINDOW_W/2), cote_haut+int(intervalle/2), 30, pygame.Color("black"), False) # On affiche le texte de l'option