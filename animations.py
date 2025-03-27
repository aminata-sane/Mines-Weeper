from PIL import Image, ImageTk
import tkinter as tk

# Fonction pour animer un GIF sur la page d'accueil
def update_gif_animation(self_obj):
    """Gère l'animation d'un GIF sur la page d'accueil."""
    try:
        # Chemin vers le GIF
        image_path = "images/accueille.gif"
        
        # Charger le GIF et récupérer les frames
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
            pass  # Fin du GIF atteinte

        # Créer un label pour afficher le GIF
        if not hasattr(self_obj, "gif_label"):
            self_obj.gif_label = tk.Label(self_obj.menu_frame)
            self_obj.gif_label.pack(pady=20)

        # Fonction pour animer le GIF
        def animate(frame_index=0):
            if hasattr(self_obj, "gif_frames") and self_obj.gif_frames:
                frame = self_obj.gif_frames[frame_index]
                self_obj.gif_label.configure(image=frame)
                next_frame_index = (frame_index + 1) % len(self_obj.gif_frames)
                self_obj.root.after(100, animate, next_frame_index)

        # Démarrer l'animation
        animate()

    except Exception as e:
        print(f"Erreur lors du chargement ou de l'animation du GIF : {e}")

# Fonction pour animer la révélation d'une case
def animate_reveal(self_obj, r, c, mines_adj):
    """Anime la révélation d'une case."""
    btn = self_obj.board[r][c]["btn"]
    cloud_stages = ["☁️", "🌫️", "💨", str(mines_adj)]

    def show_next_stage(stage_index=0):
        if stage_index < len(cloud_stages):
            if stage_index == len(cloud_stages) - 1:
                btn.config(text=cloud_stages[stage_index], fg=self_obj.colors.get(mines_adj, "black"))
            else:
                btn.config(text=cloud_stages[stage_index])
            self_obj.root.after(150, show_next_stage, stage_index + 1)

    show_next_stage()

# Fonction pour animer l'explosion d'une mine
def animate_explosion(self_obj, r, c, immediate=False):
    """Anime l'explosion d'une mine."""
    btn = self_obj.board[r][c]["btn"]
    explosion_stages = ["💣", "💥"]

    def show_explosion():
        try:
            btn.config(text=explosion_stages[1], bg="red")
            # Game over
            self_obj.timer_label.config(text="Perdu... 💥")
        except (tk.TclError, RuntimeError):
            pass

    if immediate:
        self_obj.running = False
        btn.config(text=explosion_stages[0], bg="red")
        self_obj.root.after(300, show_explosion)