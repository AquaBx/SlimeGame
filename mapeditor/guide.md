# Guide d'utilisation de l'éditeur de niveaux

## Lancement du logiciel
se placer dans le dossier courant du projet et lancer la commande `python mapeditor/main.py`.  


## Utilisation du logiciel

- Selection des assets :  
    Il est possible de sélectioner l'asset à placer à l'aide la sourie, en cliquant sur l'élément voulu en haut à droite de l'écran. Vous pouvez également selectionner les 9 premiers éléments à l'aide des touches 1 à 9 (pas le pavé numérique) du clavier.

- Placement des assets :  
    Pour placer un nouvel asset, il suffit de faire un clic gauche dans la carte, à l'endroit désiré. Le clic droit permet quant à lui de supprimé un élément placé. Enfin, le bouton "clear" permet de réinitialiser intégralement la carte.

- Import/Export des cartes :  
    L'importation et l'exportation des cartes se font à l'aide des boutons (situés en bas à droite de l'écran) prévus à cet effet 

- Calcul des interactions entre les assets :  
    Pour mettre à jour les interactions entre les différents assets de la carte, il suffit d'appuyer sur le bouton 'CT' (pour connected textures)

## Fonctionalités non implémentées

- l'ajout de nouveaux assets se faire pour le moment à l'aide de la palette disponible dans le fichier `mapeditor/config.py` du projet. Cela implique également qu'il n'est pas possible d'ajouter d'assets dans la palette d'une map déjà sauvergardée.

- le choix de fond d'écran et de taille de carte se font pour le moment uniquement dans le fichier `mapeditor/config.py` 
