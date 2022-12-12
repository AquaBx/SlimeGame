import pygame

class Messages :

    def __init__(self):
        self.adresse_fonte_bradbunr = "BradBunR.ttf" # On pourra modifier l'adresse à laquelle se trouve la fonte plus facilement car elle est dans une variable
        self.adresse_fonte_blobbychug = "BLOBBYCHUG.ttf" # Il y a autant de variables d'adresses de fontes que de fontes différentes
        self.adresse_fonte_pressstart2p = "PressStart2P-Regular.ttf" # Cette police a une taille beaucoup moins régulière, ce qui ne m'arrange pas vraiment
        self.used_font = self.adresse_fonte_blobbychug # à changer à volonté !
        pygame.font.init()
        self.GREY = (51,51,51)
        self.RED = (255,0,0)
        self.BLUE = (0,0,255)
        self.GREEN = (0,255,0)

        self.FONT_TAB = 151 * [0] # construction du tableau contenant toutes les tailles de fonte possibles dans un intervalle donné
        for i in range (0,151) :
            self.FONT_TAB[i] = pygame.font.Font(self.used_font,i)
    
    def is_a_letter(letter) :
        if letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" :
            return True
        else :
            return False

    def dividing_the_string(self,text,font_size) : # Peut-être que faire ça en itératif est mieux qu'en récursif ?
        k = 30 # Ce k va devoir dépendre de font_size, il paraît ajusté pour valeur 30
        t = []
        while True :
            if font_size*len(text) > 20 : # Il faudra affiner ce seuil par l'expérimentation
                new_line = text[0:k]
                if k+1 < len(text) :
                    if Messages.is_a_letter(text[k-1]) and Messages.is_a_letter(text[k]) : # Si les caractères autour du point de découpage sont des lettres alors on ajoute un tiret à la fin de la ligne car on a coupé un mot
                        new_line += "-"
                t.append(new_line)
                text = text[k:len(text)]
            else :
                t.append(text)
                break
        return t
    
    def display_message(self,window,text,x,y,font_size,color) :

        text_tab = Messages.dividing_the_string(self,text,font_size) # Si la chaîne est trop longue on la découpe en plusieurs lignes

        for i in range (0,len(text_tab)-1) : # On répète l'opération d'affichage de texte autant de fois qu'il y a de lignes
            img = self.FONT_TAB[font_size-1].render(text_tab[i],True,color) # On crée l'image en sélectionnant la fonte associée dans le tableau, puis le texte
            display_rect = img.get_rect() # On crée le rectangle dans lequel sera affichée l'image
            display_rect.center = (x, y+i*font_size) # On centre le rectangle sur les coordonnées entrées en paramètres
            window.blit(img,display_rect) # On affiche l'image dans son rectangle