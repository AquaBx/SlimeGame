from pygame import Surface, Vector2 as v2
from pygame import font
from pygame.font import Font
from string import ascii_letters

class Text:

    window: Surface
    fonts: dict[str, Font] = dict()
    font_size: int

    def init(window: Surface, font_data: dict[str,str], font_size: int):
        font.init()

        Text.window = window
        for name, path in font_data.items():
            Text.fonts[name] = Font(path, font_size)
        Text.font_size = font_size

    # Fonction permettant de diviser une chaîne de caractères en plus petites chaînes 
    def divide_string(text: str) -> list[str]:                       
        # Nombre de caractères par ligne
        k: int = 30                                                                        
        # Initialisation du tableau dont chaque case contiendra une ligne à afficher 
        t: list[str] = []                                                                  
        while True:
            # Seuillage pour couper en lignes
            if Text.font_size*len(text) > 20 :                                             
                # Création d'une nouvelle ligne     
                new_line: str = text[0:k]   
                # On répète l'opération jusqu'à arriver au bout du message                                               
                if k+1 < len(text) :                                                       
                    # Si les caractères autour du point de découpage sont des lettres 
                    # alors on ajoute un tiret à la fin de la ligne car on a coupé un mot
                    if text[k-1] in ascii_letters and text[k] in ascii_letters:            
                        new_line += "-"
                # Ajout de la nouvelle ligne dans le tableau
                t.append(new_line)                                                         
                # On retire le texte de la ligne d'origine pour en traiter la suite
                text = text[k:len(text)]                                                   
            else:
                # Si le texte restant est trop court on l'ajoute dans le tableau sans le modifier
                t.append(text)                                                             
                # On sort ensuite de la boucle
                break                                                                      
        return t

    def display_message(text: str, position: v2, font: str, color: tuple[int, int, int], divide: bool) -> None:
        # Le paramètre divide est un booléen :
        #   - si True alors on affichera le texte sur plusieurs lignes grâce à la fonction divide_string
        #   - sinon sur une seule ligne
        if divide == True:
            # Si la chaîne est trop longue on la découpe en plusieurs lignes
            text_tab = Text.divide_string(text)                    
            # On répète l'opération d'affichage de texte autant de fois qu'il y a de lignes
            for i in range (0,len(text_tab)-1) :                        
                # On crée l'image en sélectionnant la fonte associée dans le tableau, puis le texte                
                img = Text.fonts[font].render(text_tab[i], True, color) 
                # On crée le rectangle dans lequel sera affichée l'image
                display_rect = img.get_rect()                                           
                # On centre le rectangle sur les coordonnées entrées en paramètres
                display_rect.center = (position.x, position.y+i*Text.font_size)
                # On affiche l'image dans son rectangle              
                Text.window.blit(img, display_rect)                               
        else:
            # On crée l'image en sélectionnant la fonte associée dans le tableau, puis le texte
            img = Text.fonts[font].render(text, True, color)            
            # On crée le rectangle dans lequel sera affichée l'image
            display_rect = img.get_rect()                                               
            # On centre le rectangle sur les coordonnées entrées en paramètres
            display_rect.center = (position.x, position.y)                   
            # On affiche l'image dans son rectangle           
            Text.window.blit(img, display_rect)
