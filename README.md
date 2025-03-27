# Mines-Weeper

À l’aide de la programmation orientée objet et de la récursivité, j'ai créer un jeu
de démineur avec Tkinter; dont l'objectif est de découvrir et déminer un terrain parsemé de
mines, représenté par une matrice de cases. Chaque clic sur une case la
dévoile.

STRUCTURE DU JEU :

/Mines-weeper/

├── main.py                # Point d'entrée principal

├── demineur.py            # Classe principale Demineur

├── ui.py                  # Gestion de l'interface utilisateur (menu et jeu)

├── logic.py               # Logique du jeu (mines, drapeaux, etc.)

└── animations.py          # Gestion des animations (GIF, explosions, etc.)

INSTRUCTIONS POUR UTILISER LE JEU : (Branche├── Mode-emoji)

Utilisez les flèches directionnelles pour déplacer votre personnage sur le plateau.
Le clic droit permet de poser ou d'enlever un drapeau sur une case (utile pour marquer les mines suspectées).
Lorsque votre personnage se déplace sur une case, celle-ci est automatiquement révélée.
Si vous marchez sur une mine, le jeu se termine.

