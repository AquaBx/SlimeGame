from pygame import Vector2 as v2
from string import ascii_letters

from config import GameConfig

class Messages :    
    def divide_string(self, text: str, font_size: int) -> list[str]:                       # Fonction permettant de diviser une chaîne de caractères en plus petites chaînes 
        k: int = 30                                                                        # Nombre de caractères par ligne
        t: list[str] = []                                                                  # Initialisation du tableau dont chaque case contiendra une ligne à afficher 
        while True:
            if font_size*len(text) > 20 :                                                  # Seuillage pour couper en lignes
                new_line: str = text[0:k]                                                  # Création d'une nouvelle ligne
                if k+1 < len(text) :                                                       # On répète l'opération jusqu'à arriver au bout du message
                    if text[k-1] in ascii_letters and text[k] in ascii_letters:            # Si les caractères autour du point de découpage sont des lettres alors on ajoute un tiret à la fin de la ligne car on a coupé un mot
                        new_line += "-"
                t.append(new_line)                                                         # Ajout de la nouvelle ligne dans le tableau
                text = text[k:len(text)]                                                   # On retire le texte de la ligne d'origine pour en traiter la suite
            else:
                t.append(text)                                                             # Si le texte restant est trop court on l'ajoute dans le tableau sans le modifier
                break                                                                      # On sort ensuite de la boucle
        return t

    def display_message(self, text: str, position: v2, font: str, font_size: int, color: tuple[int, int, int], divide: bool) -> None:
        # Le paramètre divide est un booléen :
        #   - si True alors on affichera le texte sur plusieurs lignes grâce à la fonction dividing_the_string
        #   - sinon sur une seule ligne
        if divide == True:
            text_tab = Messages.divide_string(self, text, font_size)                    # Si la chaîne est trop longue on la découpe en plusieurs lignes
            for i in range (0,len(text_tab)-1) :                                        # On répète l'opération d'affichage de texte autant de fois qu'il y a de lignes
                img = GameConfig.FONT(font, font_size).render(text_tab[i], True, color) # On crée l'image en sélectionnant la fonte associée dans le tableau, puis le texte
                display_rect = img.get_rect()                                           # On crée le rectangle dans lequel sera affichée l'image
                display_rect.center = (position.x, position.y+i*font_size)              # On centre le rectangle sur les coordonnées entrées en paramètres
                GameConfig.WINDOW.blit(img, display_rect)                               # On affiche l'image dans son rectangle
        else:
            img = GameConfig.FONT(font, font_size).render(text, True, color)            # On crée l'image en sélectionnant la fonte associée dans le tableau, puis le texte
            display_rect = img.get_rect()                                               # On crée le rectangle dans lequel sera affichée l'image
            display_rect.center = (position.x, position.y)                              # On centre le rectangle sur les coordonnées entrées en paramètres
            GameConfig.WINDOW.blit(img, display_rect)                                   # On affiche l'image dans son rectangle
