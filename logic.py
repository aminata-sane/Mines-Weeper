import random
import time
import tkinter as tk
from PIL import Image, ImageTk

def place_mines(self_obj, safe_r, safe_c):
    """Place les mines après le premier clic."""
    available_positions = [
        (r, c) for r in range(self_obj.rows) for c in range(self_obj.cols)
        if (r, c) != (safe_r, safe_c)
    ]
    self_obj.mines = set(random.sample(available_positions, self_obj.mines_count))

    for r, c in self_obj.mines:
        self_obj.board[r][c]["mine"] = True

def reveal_logic(self_obj, r, c):
    """Logique de révélation des cases."""
    if self_obj.first_click:
        place_mines(self_obj, r, c)
        self_obj.first_click = False
        self_obj.start_time = time.time()
        self_obj.running = True

    if self_obj.board[r][c]["revealed"] or self_obj.board[r][c]["flag"] > 0:
        return

    self_obj.board[r][c]["revealed"] = True
    self_obj.board[r][c]["btn"].config(relief=tk.SUNKEN)

    if self_obj.board[r][c]["mine"]:
        from animations import animate_explosion
        animate_explosion(self_obj, r, c, immediate=True)
        return

    mines_adj = count_adjacent_mines(self_obj, r, c)
    if mines_adj > 0:
        from animations import animate_reveal
        animate_reveal(self_obj, r, c, mines_adj)
    else:
        reveal_adjacent(self_obj, r, c)

    if check_win(self_obj):
        game_over(self_obj, True)

def flag_logic(self_obj, r, c):
    """Ajoute ou enlève un drapeau ou un point d'interrogation sur une case."""
    if self_obj.board[r][c]["revealed"]:
        return

    # Cycle entre vide, drapeau et point d'interrogation
    current_flag = self_obj.board[r][c]["flag"]
    new_flag = (current_flag + 1) % 3
    self_obj.board[r][c]["flag"] = new_flag

    # Mettre à jour le texte du bouton
    symbols = ["", "🚩", "?"]
    self_obj.board[r][c]["btn"].config(text=symbols[new_flag])

    # Mettre à jour les compteurs
    if current_flag == 0 and new_flag == 1:  # Vide → Drapeau
        self_obj.flags_count += 1
    elif current_flag == 1 and new_flag == 2:  # Drapeau → Point d'interrogation
        self_obj.flags_count -= 1
        self_obj.question_marks_count += 1
    elif current_flag == 2 and new_flag == 0:  # Point d'interrogation → Vide
        self_obj.question_marks_count -= 1

    # Mettre à jour les labels
    self_obj.update_labels()

def count_adjacent_mines(self_obj, r, c):
    """Compte le nombre de mines adjacentes à une case donnée."""
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = r + dr, c + dc
            if (dr == 0 and dc == 0) or not (0 <= nr < self_obj.rows and 0 <= nc < self_obj.cols):
                continue
            if self_obj.board[nr][nc]["mine"]:
                count += 1
    return count

def reveal_adjacent(self_obj, r, c):
    """Révèle les cases adjacentes si la case actuelle n'a pas de mines adjacentes."""
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = r + dr, c + dc
            if (dr == 0 and dc == 0) or not (0 <= nr < self_obj.rows and 0 <= nc < self_obj.cols):
                continue
            if not self_obj.board[nr][nc]["revealed"] and self_obj.board[nr][nc]["flag"] == 0:
                self_obj.reveal(nr, nc)

def check_win(self_obj):
    """Vérifie si toutes les cases non minées sont révélées."""
    for r in range(self_obj.rows):
        for c in range(self_obj.cols):
            if not self_obj.board[r][c]["mine"] and not self_obj.board[r][c]["revealed"]:
                return False
    return True

def game_over(self_obj, won):
    """Gère la fin de partie."""
    self_obj.running = False
    
    # Révéler toutes les mines
    for r in range(self_obj.rows):
        for c in range(self_obj.cols):
            if self_obj.board[r][c]["mine"] and not self_obj.board[r][c]["revealed"]:
                self_obj.board[r][c]["btn"].config(text="💣")
                
    # Désactiver tous les boutons
    for r in range(self_obj.rows):
        for c in range(self_obj.cols):
            self_obj.board[r][c]["btn"].config(state=tk.DISABLED)
    
    # Afficher le message de victoire ou défaite
    if won:
        elapsed_time = int(time.time() - self_obj.start_time)
        self_obj.timer_label.config(text=f"Victoire ! Temps: {elapsed_time}s")

def disable_all_buttons(self_obj):
    """Désactive tous les boutons du plateau pour empêcher d'autres clics."""
    try:
        for r in range(self_obj.rows):
            for c in range(self_obj.cols):
                if not self_obj.board[r][c]["revealed"]:
                    self_obj.board[r][c]["btn"].config(state=tk.DISABLED)
    except (tk.TclError, RuntimeError):
        # En cas d'erreur (widgets détruits), ignorer
        pass

def update_gif_animation(self_obj):
    """Gère l'animation d'un GIF sur la page d'accueil."""
    try:
        image_path = "images/accueille.gif"
        gif = Image.open(image_path)
        self_obj.gif_frames = []

        try:
            frame_count = 0
            while True:
                gif.seek(frame_count)
                frame = gif.copy()
                frame = frame.resize((250, 250), Image.LANCZOS)
                photoframe = ImageTk.PhotoImage(frame)
                self_obj.gif_frames.append(photoframe)
                frame_count += 1
        except EOFError:
            pass

        def animate(frame_index=0):
            if hasattr(self_obj, "gif_frames") and self_obj.gif_frames:
                frame = self_obj.gif_frames[frame_index]
                self_obj.gif_label.configure(image=frame)
                next_frame_index = (frame_index + 1) % len(self_obj.gif_frames)
                self_obj.root.after(100, animate, next_frame_index)

        animate()

    except Exception as e:
        print(f"Erreur lors du chargement ou de l'animation du GIF : {e}")