import pygame

class Messages :

    def __init__(self):
        self.adresse_font_bradbunr = "BradBunR.ttf" # On pourra modifier l'adresse à laquelle se trouve la fonte plus facilement car elle est dans une variable
        self.adresse_fonte_blobbychug = "BLOBBYCHUG.ttf" # Il y a autant de variables d'adresses de fontes que de fontes différentes
        self.used_font = self.adresse_fonte_blobbychug # à changer à volonté !
        pygame.font.init()
        self.GREY = (51,51,0)
        self.RED = (255,0,0)
        self.FONT_TAB = [pygame.font.Font(self.used_font,1)] # construction du tableau contenant toutes les tailles de fonte possibles dans un intervalle donné    
        for i in range (2,151) :
            self.FONT_TAB.append(pygame.font.Font(self.used_font,i))
    
    def display_message(self,window,text,x,y,font_size,color) :
            
        img = self.FONT_TAB[font_size-1].render(text,True,font_size,color)
        display_rect = img.get_rect()
        display_rect.center = (x,y)
        window.blit(img,display_rect)