import pygame
from config import GameConfig

class Messages :    
    def is_a_letter(letter) : # Fonction permettant de déterminer si une chaîne est une lettre (Pour savoir à quel moment mettre un tiret à la coupure d'une ligne)
        return letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def dividing_the_string(self,text,font_size) :                                         # Fonction permettant de diviser une chaîne de caractères en plus petites chaînes 
        k = 30                                                                             # Nombre de caractères par ligne
        t = []                                                                             # Initialisation du tableau dont chaque case contiendra une ligne à afficher 
        while True :
            if font_size*len(text) > 20 :                                                  # Seuillage pour couper en lignes
                new_line = text[0:k]                                                       # Création d'une nouvelle ligne
                if k+1 < len(text) :                                                       # On répète l'opération jusqu'à arriver au bout du message
                    if Messages.is_a_letter(text[k-1]) and Messages.is_a_letter(text[k]) : # Si les caractères autour du point de découpage sont des lettres alors on ajoute un tiret à la fin de la ligne car on a coupé un mot
                        new_line += "-"
                t.append(new_line)                                                         # Ajout de la nouvelle ligne dans le tableau
                text = text[k:len(text)]                                                   # On retire le texte de la ligne d'origine pour en traiter la suite
            else :
                t.append(text)                                                             # Si le texte restant est trop court on l'ajoute dans le tableau sans le modifier
                break                                                                      # On sort ensuite de la boucle
        return t
    
    def display_message(self,window,text,x,y,font,font_size,color,divide) :
        # Le paramètre divide est un booléen : si True alors on affichera le texte sur plusieurs lignes grâce à la fonction dividing_the_string, sinon sur une seule ligne
        if divide == True :
            text_tab = Messages.dividing_the_string(self,text,font_size)             # Si la chaîne est trop longue on la découpe en plusieurs lignes
            for i in range (0,len(text_tab)-1) :                                     # On répète l'opération d'affichage de texte autant de fois qu'il y a de lignes
                img = GameConfig.FONT(font,font_size).render(text_tab[i],True,color) # On crée l'image en sélectionnant la fonte associée dans le tableau, puis le texte
                display_rect = img.get_rect()                                        # On crée le rectangle dans lequel sera affichée l'image
                display_rect.center = (x, y+i*font_size)                             # On centre le rectangle sur les coordonnées entrées en paramètres
                window.blit(img,display_rect)                                        # On affiche l'image dans son rectangle
        else :
            img = GameConfig.FONT(font,font_size).render(text,True,color)            # On crée l'image en sélectionnant la fonte associée dans le tableau, puis le texte
            display_rect = img.get_rect()                                            # On crée le rectangle dans lequel sera affichée l'image
            display_rect.center = (x, y)                                             # On centre le rectangle sur les coordonnées entrées en paramètres
            window.blit(img,display_rect)                                            # On affiche l'image dans son rectangle