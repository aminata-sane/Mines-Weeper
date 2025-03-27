import tkinter as tk
import time
import random
from PIL import Image, ImageTk

class Demineur:
    def __init__(self, root):
        self.root = root
        self.root.title("Démineur")
        # Définir une taille minimale pour la fenêtre
        self.root.minsize(400, 400)
        
        # Configuration initiale pour le redimensionnement
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.difficulty = {
            "Facile": (9, 9, 10),
            "Moyen": (16, 16, 40),
            "Difficile": (16, 30, 99)
        }
        self.start_time = None
        self.running = False

        # Couleurs pour les chiffres
        self.colors = {
            1: "blue", 2: "green", 3: "red", 4: "purple",
            5: "maroon", 6: "turquoise", 7: "black", 8: "gray"
        }

        # Initialiser les attributs nécessaires
        self.first_click = True
        self.board = []
        self.flags_count = 0
        self.question_marks_count = 0

        self.create_menu()
        
        # Configurer les événements de redimensionnement
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Gérer le redimensionnement de la fenêtre"""
        # Ne rien faire si la fenêtre est trop petite
        if event.width < 400 or event.height < 400:
            return
            
        # Si nous sommes dans le jeu, ajuster la taille des boutons
        if hasattr(self, "board_frame") and hasattr(self, "board"):
            try:
                # Calculer les nouvelles dimensions des boutons
                btn_width = max(1, event.width // (self.cols * 3))  # Diviser par 3 pour éviter des boutons trop grands
                btn_height = max(1, event.height // (self.rows * 4))
                
                # Mettre à jour tous les boutons du plateau
                for r in range(self.rows):
                    for c in range(self.cols):
                        if r < len(self.board) and c < len(self.board[r]):
                            btn = self.board[r][c]["btn"]
                            # Ajuster la taille du texte en fonction de la taille du bouton
                            font_size = min(14, max(8, min(btn_width, btn_height)))
                            btn.config(font=("Arial", font_size))
            except (AttributeError, tk.TclError):
                pass  # Ignorer les erreurs si certains widgets n'existent plus

    def create_menu(self):
        """Créer le menu de sélection du niveau avec une image GIF animée."""
        if hasattr(self, "game_frame"):
            self.game_frame.destroy()  # Détruire le cadre de jeu s'il existe

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        # Configurer le menu pour être responsive
        for i in range(3):  # Pour les 3 sections principales du menu
            self.menu_frame.grid_rowconfigure(i, weight=1)
        self.menu_frame.grid_columnconfigure(0, weight=1)

        # Ajouter une image GIF animée
        try:
            # Charger l'image depuis un fichier GIF
            image_path = "images/accueille.gif"
            
            # Ouvrir le GIF et récupérer les frames (images)
            gif = Image.open(image_path)
            self.gif_frames = []
            
            try:
                # Parcourir toutes les frames du GIF
                frame_count = 0
                while True:
                    # Copier la frame actuelle
                    gif.seek(frame_count)
                    frame = gif.copy()
                    
                    # Redimensionner si nécessaire
                    frame = frame.resize((250, 250), Image.LANCZOS)
                    
                    # Convertir pour Tkinter
                    photoframe = ImageTk.PhotoImage(frame)
                    self.gif_frames.append(photoframe)
                    
                    frame_count += 1
            except EOFError:
                # La fin du GIF a été atteinte
                pass
            
            # Créer un label pour afficher le GIF
            self.gif_label = tk.Label(self.menu_frame)
            self.gif_label.pack(pady=20, expand=True)
            
            # Fonction pour animer le GIF
            def update_gif(frame_index=0):
                if hasattr(self, "gif_frames") and self.gif_frames:
                    # Mettre à jour l'image du label
                    frame = self.gif_frames[frame_index]
                    self.gif_label.configure(image=frame)
                    
                    # Calculer l'index de la prochaine frame (boucle circulaire)
                    next_frame_index = (frame_index + 1) % len(self.gif_frames)
                    
                    # Planifier la mise à jour de la prochaine frame (100ms = 0.1s entre chaque frame)
                    self.root.after(100, update_gif, next_frame_index)
            
            # Démarrer l'animation
            update_gif()
            
        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")

        # Ajouter un titre
        title_label = tk.Label(self.menu_frame, text="Démineur", font=("Arial", 24, "bold"))
        title_label.pack(pady=10)

        # Texte d'instructions
        tk.Label(self.menu_frame, text="Choisissez la difficulté :", font=("Arial", 14)).pack(pady=10)
        
        # Cadre pour les boutons de difficulté
        buttons_frame = tk.Frame(self.menu_frame)
        buttons_frame.pack(pady=10, fill=tk.X, padx=50)
        
        # Configurer le cadre des boutons pour être responsive
        for i in range(3):  # Pour les 3 boutons de difficulté
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Boutons stylisés pour chaque niveau de difficulté
        for i, level in enumerate(self.difficulty):
            button = tk.Button(
                buttons_frame, 
                text=level, 
                command=lambda l=level: self.start_game(l),
                font=("Arial", 12),
                relief=tk.RAISED,
                bd=3
            )
            button.grid(row=0, column=i, padx=10, sticky="ew")  # "ew" pour étirer horizontalement

    def start_game(self, level):
        """Démarre une nouvelle partie avec le niveau choisi."""
        self.level = level
        self.rows, self.cols, self.mines_count = self.difficulty[level]

        # Réinitialiser les attributs pour une nouvelle partie
        self.first_click = True
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags_count = 0
        self.question_marks_count = 0

        if hasattr(self, "menu_frame"):
            self.menu_frame.destroy()
        if hasattr(self, "game_frame"):
            self.game_frame.destroy()

        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(fill=tk.BOTH, expand=True)

        # Configurer le cadre de jeu pour être responsive
        self.game_frame.grid_rowconfigure(0, weight=0)  # Timer
        self.game_frame.grid_rowconfigure(1, weight=0)  # Labels d'infos
        self.game_frame.grid_rowconfigure(2, weight=10)  # Plateau de jeu (plus d'espace)
        self.game_frame.grid_rowconfigure(3, weight=0)  # Bouton retour
        
        for i in range(self.cols):
            self.game_frame.grid_columnconfigure(i, weight=1)

        # Timer et contrôles en haut
        controls_frame = tk.Frame(self.game_frame)
        controls_frame.grid(row=0, column=0, columnspan=self.cols, sticky="ew")
        controls_frame.grid_columnconfigure(0, weight=1)  # Timer
        controls_frame.grid_columnconfigure(1, weight=0)  # Bouton réinitialiser
        
        self.timer_label = tk.Label(controls_frame, text="Temps: 0s")
        self.timer_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        restart_button = tk.Button(controls_frame, text="Réinitialiser", command=lambda: self.start_game(self.level))
        restart_button.grid(row=0, column=1, sticky="e", padx=10, pady=5)

        # Frame pour les labels d'information
        info_frame = tk.Frame(self.game_frame)
        info_frame.grid(row=1, column=0, columnspan=self.cols, sticky="ew", pady=5)
        
        # Configurer les colonnes pour les labels
        for i in range(3):
            info_frame.grid_columnconfigure(i, weight=1)
        
        # Ajouter les labels pour les mines, drapeaux et points d'interrogation
        self.mines_label = tk.Label(info_frame, text=f"Mines: {self.mines_count}", anchor="center")
        self.mines_label.grid(row=0, column=0, sticky="ew")

        self.flags_label = tk.Label(info_frame, text="Drapeaux: 0", anchor="center")
        self.flags_label.grid(row=0, column=1, sticky="ew")

        self.questions_label = tk.Label(info_frame, text="Points d'interrogation: 0", anchor="center")
        self.questions_label.grid(row=0, column=2, sticky="ew")

        # Plateau de jeu (la partie principale)
        self.board_frame = tk.Frame(self.game_frame)
        self.board_frame.grid(row=2, column=0, columnspan=self.cols, sticky="nsew", padx=10, pady=10)

        # Configurer les poids pour le plateau de jeu
        for r in range(self.rows):
            self.board_frame.grid_rowconfigure(r, weight=1)
        for c in range(self.cols):
            self.board_frame.grid_columnconfigure(c, weight=1)

        # Créer les boutons du plateau de jeu
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.board_frame, 
                    command=lambda x=r, y=c: self.reveal(x, y),
                    font=("Arial", 10)
                )
                btn.bind("<Button-3>", lambda e, x=r, y=c: self.flag(x, y))
                btn.grid(row=r, column=c, sticky="nsew")
                self.board[r][c] = {"btn": btn, "mine": False, "revealed": False, "flag": 0}

        # Ajouter un bouton "Retour" en bas
        back_frame = tk.Frame(self.game_frame)
        back_frame.grid(row=3, column=0, columnspan=self.cols, sticky="ew", pady=5)
        back_frame.grid_columnconfigure(0, weight=1)
        
        self.back_button = tk.Button(back_frame, text="Retour au menu", command=self.create_menu)
        self.back_button.grid(row=0, column=0, sticky="ew", padx=50)

        # Lancer le timer
        self.start_time = None
        self.running = False
        self.update_timer()
        
        # Déclencher un événement de redimensionnement pour ajuster les boutons
        self.root.update_idletasks()
        self.root.event_generate("<Configure>", when="now")

    def place_mines(self, safe_r, safe_c):
        """Place les mines après le premier clic."""
        available_positions = [(r, c) for r in range(self.rows) for c in range(self.cols) if (r, c) != (safe_r, safe_c)]
        self.mines = set(random.sample(available_positions, self.mines_count))

        for r, c in self.mines:
            self.board[r][c]["mine"] = True

    def reveal(self, r, c):
        """Révèle une case et applique les règles du jeu avec animation."""
        if self.first_click:
            self.place_mines(r, c)
            self.first_click = False
            self.start_time = time.time()
            self.running = True

        if self.board[r][c]["revealed"] or self.board[r][c]["flag"] > 0:
            return

        self.board[r][c]["revealed"] = True
        self.board[r][c]["btn"].config(relief=tk.SUNKEN)

        if self.board[r][c]["mine"]:
            # Animation d'explosion pour la bombe cliquée
            self.animate_explosion(r, c, immediate=True)
            return

        # Animation de dissipation du nuage pour les chiffres
        mines_adj = self.count_adjacent_mines(r, c)
        if mines_adj > 0:
            self.animate_reveal(r, c, mines_adj)
        else:
            # Pas d'animation pour les cases vides
            self.board[r][c]["btn"].config(text="")
            self.reveal_adjacent(r, c)

        if self.check_win():
            self.game_over(True)

    def animate_reveal(self, r, c, mines_adj):
        """Anime la dissipation d'un nuage pour révéler le chiffre."""
        btn = self.board[r][c]["btn"]
        # Séquence d'animation: nuage qui se dissipe graduellement
        cloud_stages = ["☁️", "🌫️", "💨", str(mines_adj)]
        
        def show_next_stage(stage_index=0):
            if stage_index < len(cloud_stages):
                if stage_index == len(cloud_stages) - 1:  # Dernière étape = chiffre
                    # Appliquer la couleur correspondant au chiffre
                    btn.config(text=cloud_stages[stage_index], fg=self.colors.get(mines_adj, "black"))
                else:
                    btn.config(text=cloud_stages[stage_index])
                self.root.after(150, show_next_stage, stage_index + 1)
        
        show_next_stage()

    def animate_explosion(self, r, c, immediate=False):
        """Anime l'explosion d'une bombe."""
        btn = self.board[r][c]["btn"]
        # Séquence d'animation: explosion
        explosion_stages = ["💣", "💥"]
        
        def show_explosion():
            # Vérifier si le widget existe toujours avant de le modifier
            try:
                btn.config(text=explosion_stages[1], bg="red")
                if immediate:
                    self.root.after(1000, lambda: self.reveal_all_mines(r, c))
            except (tk.TclError, RuntimeError):
                # Le widget n'existe plus, ignorer l'erreur
                pass
        
        # Pour la bombe cliquée, exploser immédiatement et arrêter le chrono
        if immediate:
            # Arrêter le chronomètre immédiatement quand une bombe est cliquée
            self.running = False
            
            # Désactiver tous les boutons immédiatement pour empêcher d'autres clics
            self.disable_all_buttons()
            
            try:
                btn.config(text=explosion_stages[0], bg="red")
                self.root.after(300, show_explosion)
            except (tk.TclError, RuntimeError):
                # Le widget n'existe plus, ignorer l'erreur
                pass
        else:
            # Pour les autres bombes, juste montrer l'explosion
            try:
                btn.config(text=explosion_stages[1], bg="red")
            except (tk.TclError, RuntimeError):
                # Le widget n'existe plus, ignorer l'erreur
                pass

    def disable_all_buttons(self):
        """Désactive tous les boutons du plateau pour empêcher d'autres clics."""
        try:
            for r in range(self.rows):
                for c in range(self.cols):
                    # Désactiver uniquement les boutons qui ne sont pas déjà révélés
                    if not self.board[r][c]["revealed"]:
                        # On garde l'affichage mais on désactive les interactions
                        # Cela permet de continuer à voir les drapeaux posés
                        self.board[r][c]["btn"].config(state=tk.DISABLED)
        except (tk.TclError, RuntimeError):
            # En cas d'erreur (widgets détruits), ignorer
            pass

    def reveal_all_mines(self, clicked_r, clicked_c):
        """Révèle toutes les bombes avec un délai."""
        mines_to_reveal = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c]["mine"] and not (r == clicked_r and c == clicked_c):
                    mines_to_reveal.append((r, c))
        
        # Révéler les mines une par une avec un délai
        def reveal_next_mine(index=0):
            if index < len(mines_to_reveal):
                r, c = mines_to_reveal[index]
                try:
                    self.animate_explosion(r, c)
                    self.root.after(100, reveal_next_mine, index + 1)
                except (tk.TclError, RuntimeError):
                    # En cas d'erreur, passer à la mine suivante
                    reveal_next_mine(index + 1)
            else:
                # Une fois toutes les mines révélées, terminer le jeu
                try:
                    self.root.after(500, lambda: self.game_over(False))
                except (tk.TclError, RuntimeError):
                    # En cas d'erreur, ne rien faire
                    pass
        
        reveal_next_mine()

    def count_adjacent_mines(self, r, c):
        """Compte le nombre de mines adjacentes à une case donnée."""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (dr == 0 and dc == 0) or not (0 <= r+dr < self.rows and 0 <= c+dc < self.cols):
                    continue
                if self.board[r+dr][c+dc]["mine"]:
                    count += 1
        return count

    def reveal_adjacent(self, r, c):
        """Révèle les cases vides adjacentes (récursivité)."""
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and not self.board[nr][nc]["revealed"]:
                    self.reveal(nr, nc)

    def flag(self, r, c):
        """Ajoute ou enlève un drapeau ou un point d'interrogation sur une case."""
        if self.board[r][c]["revealed"]:
            return

        current_flag = self.board[r][c]["flag"]
        new_flag = (current_flag + 1) % 3  # Cycle entre 0 (vide), 1 (drapeau), 2 (point d'interrogation)
        self.board[r][c]["flag"] = new_flag

        # Mettre à jour le texte du bouton
        symbols = ["", "🚩", "?"]
        self.board[r][c]["btn"].config(text=symbols[new_flag])

        # Mettre à jour les compteurs
        if current_flag == 0 and new_flag == 1:  # Vide → Drapeau
            self.flags_count += 1
        elif current_flag == 1 and new_flag == 2:  # Drapeau → Point d'interrogation
            self.flags_count -= 1
            self.question_marks_count += 1
        elif current_flag == 2 and new_flag == 0:  # Point d'interrogation → Vide
            self.question_marks_count -= 1

        # Mettre à jour les labels
        self.update_labels()

    def check_win(self):
        """Vérifie si toutes les cases non minées sont révélées."""
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.board[r][c]["mine"] and not self.board[r][c]["revealed"]:
                    return False
        return True

    def game_over(self, won):
        """Affiche le résultat et arrête le jeu."""
        self.running = False
        
        # Si perdu, les mines sont déjà révélées par reveal_all_mines
        if won:
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.board[r][c]["mine"]:
                        self.board[r][c]["btn"].config(text="💣")
        
        # Désactiver tous les boutons
        for r in range(self.rows):
            for c in range(self.cols):
                self.board[r][c]["btn"].config(state=tk.DISABLED)

        message = "Victoire ! 🎉" if won else "Perdu... 💥"
        self.timer_label.config(text=message)

    def update_timer(self):
        """Mise à jour du chronomètre."""
        if self.running and self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Temps: {elapsed_time}s")
        if hasattr(self, 'root'):
            self.root.after(1000, self.update_timer)

    def update_labels(self):
        """Met à jour les labels des mines, drapeaux et points d'interrogation."""
        self.flags_label.config(text=f"Drapeaux: {self.flags_count}")
        self.questions_label.config(text=f"Points d'interrogation: {self.question_marks_count}")
        self.mines_label.config(text=f"Mines: {self.mines_count - self.flags_count}")