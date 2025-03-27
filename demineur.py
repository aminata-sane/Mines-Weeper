import tkinter as tk
import time
import random
from PIL import Image, ImageTk
from tkinter import messagebox

class Demineur(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # Ne pas appeler de gestionnaire de géométrie ici
        
        # Configuration de base
        self.rows = 10
        self.cols = 10
        self.mines = 15
        self.tile_size = 30  # Taille des cases en pixels
        self.game_over = False
        
        # Couleurs plus vives
        self.colors = {
            1: "#0000FF",  # Bleu
            2: "#008000",  # Vert
            3: "#FF0000",  # Rouge
            4: "#00008B",  # Bleu foncé
            5: "#8B0000",  # Rouge foncé
            6: "#008B8B",  # Cyan foncé
            7: "#000000",  # Noir
            8: "#808080",  # Gris
        }
        
        # Création du personnage
        self.player_position = [0, 0]  # Position initiale [row, col]
        self.player_image = None
        self.load_player_image()
        
        self.create_widgets()
        self.create_board()
        self.place_mines()
        self.calculate_numbers()
        self.draw_board()
        self.draw_player()
        
        # Gestion des touches pour déplacer le personnage
        self.master.bind("<Up>", lambda event: self.move_player(-1, 0))
        self.master.bind("<Down>", lambda event: self.move_player(1, 0))
        self.master.bind("<Left>", lambda event: self.move_player(0, -1))
        self.master.bind("<Right>", lambda event: self.move_player(0, 1))
        
        # Ajout d'un gestionnaire pour le clic droit (poser un drapeau)
        self.canvas.bind("<Button-3>", self.toggle_flag)
    
    def load_player_image(self):
        try:
            # Création d'une image simple au lieu de charger une image externe
            img = Image.new('RGB', (self.tile_size-4, self.tile_size-4), color='yellow')
            # Essayez d'ajouter des détails au personnage
            draw = ImageTk.Draw(img)
            # Vous pouvez essayer de dessiner des yeux, etc. si vous voulez
            self.player_image = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image du joueur: {e}")
            self.player_image = None
    
    def toggle_flag(self, event):
        if self.game_over:
            return
        
        # Convertir les coordonnées du clic en indices de grille
        col = event.x // self.tile_size
        row = event.y // self.tile_size
        
        if 0 <= row < self.rows and 0 <= col < self.cols and not self.revealed[row][col]:
            self.flagged[row][col] = not self.flagged[row][col]
            self.draw_board()
            self.draw_player()
    
    def draw_player(self):
        row, col = self.player_position
        x = col * self.tile_size + self.tile_size // 2
        y = row * self.tile_size + self.tile_size // 2
        
        # Supprimer l'ancien dessin du joueur s'il existe
        if hasattr(self, 'player_sprite'):
            self.canvas.delete(self.player_sprite)
        
        if self.player_image:
            self.player_sprite = self.canvas.create_image(x, y, image=self.player_image)
        else:
            # Dessiner un cercle jaune si l'image ne peut pas être chargée
            self.player_sprite = self.canvas.create_oval(
                x - self.tile_size//3, y - self.tile_size//3,
                x + self.tile_size//3, y + self.tile_size//3,
                fill="yellow", outline="black")
            
            # Ajouter un visage simple
            self.canvas.create_oval(x-5, y-5, x-2, y-2, fill="black")  # Œil gauche
            self.canvas.create_oval(x+2, y-5, x+5, y-2, fill="black")  # Œil droit
            self.canvas.create_arc(x-4, y-2, x+4, y+4, start=0, extent=180, style=tk.ARC)  # Sourire
    
    def move_player(self, dr, dc):
        if self.game_over:
            return
        
        new_row = self.player_position[0] + dr
        new_col = self.player_position[1] + dc
        
        # Vérifier si la nouvelle position est valide
        if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
            self.player_position = [new_row, new_col]
            self.draw_player()
            
            # Vérifier si le joueur a marché sur une mine
            if self.board[new_row][new_col] == -1:
                self.step_on_mine()
            # Révéler automatiquement la case
            elif not self.revealed[new_row][new_col]:
                self.reveal_cell(new_row, new_col)
    
    def step_on_mine(self):
        row, col = self.player_position
        x = col * self.tile_size + self.tile_size // 2
        y = row * self.tile_size + self.tile_size // 2
        
        # Animation d'explosion
        explosion = self.canvas.create_oval(
            x - self.tile_size, y - self.tile_size,
            x + self.tile_size, y + self.tile_size,
            fill="red", outline="orange")
        
        self.master.update()
        self.master.after(500, lambda: self.canvas.delete(explosion))
        
        self.game_over = True
        messagebox.showinfo("Game Over", "Oh non! Votre personnage a marché sur une mine!")
        self.reveal_all_mines()
    
    def create_widgets(self):
        # Création d'un frame principal
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)
        
        # Bouton de nouvelle partie avec style amélioré
        self.new_game_button = tk.Button(
            self.main_frame, 
            text="Nouvelle Partie", 
            command=self.reset_game,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            padx=10
        )
        self.new_game_button.pack(fill="x", padx=10, pady=5)
        
        # Amélioration visuelle du canvas
        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.cols * self.tile_size,
            height=self.rows * self.tile_size,
            bg="#BBBBBB",  # Couleur de fond plus agréable
            highlightthickness=2,
            highlightbackground="#555555"
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Ajout d'un label pour les instructions
        self.instructions = tk.Label(
            self.main_frame,
            text="Utilisez les flèches du clavier pour déplacer le personnage\nClic droit pour poser/enlever un drapeau",
            font=("Arial", 10),
            fg="#333333"
        )
        self.instructions.pack(pady=5)
        
        # Score et statistiques
        self.stats_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.stats_frame.pack(fill="x", padx=10, pady=5)
        
        self.mines_label = tk.Label(
            self.stats_frame,
            text=f"Mines: {self.mines}",
            font=("Arial", 10),
            fg="#333333",
            bg="#f0f0f0"
        )
        self.mines_label.pack(side="left", padx=10)
    
    def reset_game(self):
        # Réinitialiser le jeu
        self.game_over = False
        self.player_position = [0, 0]  # Position initiale
        
        # Recréer le plateau
        self.create_board()
        self.place_mines()
        self.calculate_numbers()
        self.draw_board()
        self.draw_player()
        
        # Mettre à jour l'état du jeu
        self.master.update()
    
    def create_board(self):
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
    
    def place_mines(self):
        # Placement aléatoire des mines
        mine_positions = []
        while len(mine_positions) < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            
            # S'assurer que la première case est sûre (pas de mine à la position initiale du joueur)
            if [row, col] == [0, 0]:
                continue
                
            pos = (row, col)
            if pos not in mine_positions:
                mine_positions.append(pos)
                self.board[row][col] = -1  # -1 représente une mine
    
    def calculate_numbers(self):
        # Calculer les nombres pour chaque case (combien de mines adjacentes)
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:  # Si c'est une mine
                    continue
                
                # Vérifier les 8 cases adjacentes
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        
                        r, c = row + dr, col + dc
                        if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == -1:
                            self.board[row][col] += 1
    
    def reveal_cell(self, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols) or self.revealed[row][col]:
            return
        
        self.revealed[row][col] = True
        
        # Si c'est une case vide, révéler récursivement les cases adjacentes
        if self.board[row][col] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    self.reveal_cell(row + dr, col + dc)
        
        self.draw_board()
        self.draw_player()  # Redessiné le joueur pour qu'il reste visible
    
    def reveal_all_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    self.revealed[row][col] = True
        self.draw_board()
        self.draw_player()  # Garder le joueur visible
    
    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.tile_size
                y1 = row * self.tile_size
                x2 = x1 + self.tile_size
                y2 = y1 + self.tile_size
                
                # Effet d'alternance de couleurs comme un échiquier pour plus de style
                if (row + col) % 2 == 0:
                    bg_color = "#CCCCCC"
                else:
                    bg_color = "#DDDDDD"
                
                # Si la case est révélée
                if self.revealed[row][col]:
                    # Une mine
                    if self.board[row][col] == -1:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FF9999", outline="#555555")
                        self.canvas.create_oval(x1+6, y1+6, x2-6, y2-6, fill="black")
                    # Un chiffre
                    else:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#EEEEEE", outline="#555555")
                        if self.board[row][col] > 0:
                            self.canvas.create_text(
                                x1 + self.tile_size // 2, y1 + self.tile_size // 2,
                                text=str(self.board[row][col]),
                                fill=self.colors[self.board[row][col]],
                                font=("Arial", 12, "bold")
                            )
                # Case non révélée
                else:
                    # Effet 3D pour les cases non révélées
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="#555555")
                    self.canvas.create_line(x1, y1, x2, y1, fill="#FFFFFF", width=2)
                    self.canvas.create_line(x1, y1, x1, y2, fill="#FFFFFF", width=2)
                    self.canvas.create_line(x2, y1, x2, y2, fill="#888888", width=1)
                    self.canvas.create_line(x1, y2, x2, y2, fill="#888888", width=1)
                    
                    # Marqueur de drapeau
                    if self.flagged[row][col]:
                        # Dessiner un drapeau rouge
                        flag_pole = self.canvas.create_line(
                            x1 + self.tile_size//2, y1 + 5,
                            x1 + self.tile_size//2, y2 - 5,
                            fill="black", width=2
                        )
                        flag = self.canvas.create_polygon(
                            x1 + self.tile_size//2, y1 + 5,
                            x1 + self.tile_size//2 + 10, y1 + 10,
                            x1 + self.tile_size//2, y1 + 15,
                            fill="red"
                        )
        
        # Redessiner le joueur
        self.draw_player()
        
    def check_win(self):
        # Le joueur gagne s'il a révélé toutes les cases sans mines
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != -1 and not self.revealed[row][col]:
                    return False
        return True