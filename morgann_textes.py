import pygame

class Messages :

    def __init__(self):
        self.adresse_fonte_bradbunr = "BradBunR.ttf"                    # On pourra modifier l'adresse à laquelle se trouve la fonte plus facilement car elle est dans une variable
        self.adresse_fonte_blobbychug = "BLOBBYCHUG.ttf"                # Il y a autant de variables d'adresses de fontes que de fontes différentes
        self.adresse_fonte_pressstart2p = "PressStart2P-Regular.ttf"    # Cette police a une taille beaucoup moins régulière, ce qui ne m'arrange pas vraiment
        self.used_font = self.adresse_fonte_blobbychug                  # On choisit l'une des fontes de texte
        pygame.font.init()                                              # Initialisation de la fonte
        self.GREY = (51,51,51)                                          # Initialisations de plusieurs couleurs
        self.RED = (255,0,0)
        self.BLUE = (0,0,255)
        self.GREEN = (0,255,0)

        self.FONT_TAB = 151 * [0] # Construction du tableau contenant toutes les tailles de fonte possibles dans un intervalle donné
        for i in range (0,151) :
            self.FONT_TAB[i] = pygame.font.Font(self.used_font,i)
    
    def is_a_letter(letter) : # Fonction permettant de déterminer si une chaîne est une lettre (Pour savoir à quel moment mettre un tiret à la coupure d'une ligne)
        if letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" :
            return True
        else :
            return False

    def dividing_the_string(self,text,font_size) :      # Fonction permettant de diviser une chaîne de caractères en plus petites chaînes 
        k = 30                                          # Nombre de caractères par ligne
        t = []                                          # Initialisation du tableau dont chaque case contiendra une ligne à afficher 
        while True :
            if font_size*len(text) > 20 :               # Seuillage pour couper en lignes
                new_line = text[0:k]                    # Création d'une nouvelle ligne
                if k+1 < len(text) :                    # On répète l'opération jusqu'à arriver au bout du message
                    if Messages.is_a_letter(text[k-1]) and Messages.is_a_letter(text[k]) : # Si les caractères autour du point de découpage sont des lettres alors on ajoute un tiret à la fin de la ligne car on a coupé un mot
                        new_line += "-"
                t.append(new_line)                      # Ajout de la nouvelle ligne dans le tableau
                text = text[k:len(text)]                # On retire le texte de la ligne d'origine pour en traiter la suite
            else :
                t.append(text)                          # Si le texte restant est trop court on l'ajoute dans le tableau sans le modifier
                break                                   # On sort ensuite de la boucle
        return t
    
    def display_message(self,window,text,x,y,font_size,color,divide) :
        # Le paramètre divide est un booléen : si True alors on affichera le texte sur plusieurs lignes grâce à la fonction dividing_the_string, sinon sur une seule ligne
        if divide == True :
            text_tab = Messages.dividing_the_string(self,text,font_size)        # Si la chaîne est trop longue on la découpe en plusieurs lignes
            for i in range (0,len(text_tab)-1) :                                # On répète l'opération d'affichage de texte autant de fois qu'il y a de lignes
                img = self.FONT_TAB[font_size-1].render(text_tab[i],True,color) # On crée l'image en sélectionnant la fonte associée dans le tableau, puis le texte
                display_rect = img.get_rect()                                   # On crée le rectangle dans lequel sera affichée l'image
                display_rect.center = (x, y+i*font_size)                        # On centre le rectangle sur les coordonnées entrées en paramètres
                window.blit(img,display_rect)                                   # On affiche l'image dans son rectangle
        
        else :
            img = self.FONT_TAB[font_size-1].render(text,True,color)    # On crée l'image en sélectionnant la fonte associée dans le tableau, puis le texte
            display_rect = img.get_rect()                               # On crée le rectangle dans lequel sera affichée l'image
            display_rect.center = (x, y)                                # On centre le rectangle sur les coordonnées entrées en paramètres
            window.blit(img,display_rect)                               # On affiche l'image dans son rectangle