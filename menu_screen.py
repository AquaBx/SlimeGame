import pygame
from pygame import Vector2 as v2

from morgann_textes import Text
from config import GameConfig

class Menu :
    """
    Cette classe permet d'afficher deux menus : le menu principal hors-partie et le menu en jeu

    Le menu principal contient :
    Une image de fond
    Un rectangle par option de menu
    Dans chaque rectangle, on affiche une option
    """

    def display_main_menu(options) :
        """
        Fonction permettant d'afficher le menu principal
        options est le tableau contenant les string des options affichées dans les rectangles : 
            options = ["Continuer (C)", "Nouvelle partie (N)", "Charger une partie (H)", "Sauvegarder (S)", "Quitter (Q)"]
        """

        window = GameConfig.WINDOW
        messages = Text()
        n_rect = len(options)                                    # Nombre de rectangles dans lesquels on affiche les options du menu
        intervalle = int(GameConfig.WINDOW_SIZE.y/(2*n_rect))    # Intervalle vertical de pixels entre les rectangles
        longueur_x = int(0.35*GameConfig.WINDOW_SIZE.x)          # Longueur horizontale de chaque rectangle
        cote_gauche = int(0.325*GameConfig.WINDOW_SIZE.x)        # Côté gauche de chaque rectangle

        # background_scaled = pygame.transform.scale(pygame.image.load(background), (GameConfig.WINDOW_SIZE.x, GameConfig.WINDOW_SIZE.y))   # On met l'image de fond à l'échelle de la fenêtre de jeu 
        # window.blit(background_scaled,(0,0))                                                                                              # On affiche l'image de fond sur la fenêtre

        for i in range (0,n_rect) :
            cote_haut = 10+int(intervalle/2)+i*intervalle*2                                                                                                  # On détermine le côté haut des rectagnles un par un
            pygame.draw.rect(window, pygame.Color('brown'), (cote_gauche, cote_haut, longueur_x, intervalle))                                                # On dessine les rectangles
            messages.display_message(options[i], v2(GameConfig.WINDOW_SIZE.x/2, cote_haut+(intervalle/2)), "PressStart2P", pygame.Color('black'), False)     # On affiche le texte de l'option


    def display_ingame_menu(options) :
        """
        Fonction permettant d'afficher le menu en jeu
        """
        window = GameConfig.WINDOW
        messages = Text()
        n_rect = len(options)                                        # Nombre de rectangles dans lesquels on affiche les options du menu
        intervalle = int((GameConfig.WINDOW_SIZE.x-20)/(2*n_rect))   # Intervalle vertical de pixels entre les rectangles
        longueur_x = int(0.35*GameConfig.WINDOW_SIZE.x)              # Longueur horizontale de chaque rectangle
        cote_gauche = int(0.325*GameConfig.WINDOW_SIZE.x)            # Côté gauche de chaque rectangle

        # Pour le tracé de l'image de fond, 2 choix : rectangle uni ou image
        #pygame.draw.rect(window, pygame.Color('red'), (int(0.3*GameConfig.WINDOW_W),10,int(0.4*GameConfig.WINDOW_W),GameConfig.WINDOW_H-20))           # Affichage du fond uni

        # background_scaled = pygame.transform.scale(pygame.image.load(background), (int(0.4*GameConfig.WINDOW_SIZE.x),GameConfig.WINDOW_SIZE.y-20))    # Mise à l'échelle d'une image de fond (menu central ne recouvrant pas toute la fenêtre)
        # window.blit(background_scaled,(int(0.3*GameConfig.WINDOW_SIZE.x),10))                                                                         # Affichage du menu central

        for i in range (0,n_rect) :   # Affichage des textes des options
            cote_haut = 10+int(intervalle/2)+i*intervalle*2                                                                                              # On détermine le côté haut des rectagnles un par un
            pygame.draw.rect(window, pygame.Color('blue'), (cote_gauche, cote_haut, longueur_x, intervalle))                                             # On dessine les rectangles
            messages.display_message(options[i], v2(GameConfig.WINDOW_SIZE.x/2, cote_haut+(intervalle/2)), "PressStart2P", pygame.Color("black"), False) # On affiche le texte de l'option
