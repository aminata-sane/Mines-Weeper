import tkinter as tk
from animations import update_gif_animation

def create_menu(self_obj):
    """Créer le menu de sélection du niveau avec une image GIF animée."""
    if hasattr(self_obj, "game_frame"):
        self_obj.game_frame.destroy()

    self_obj.menu_frame = tk.Frame(self_obj.root)
    self_obj.menu_frame.pack(fill=tk.BOTH, expand=True)

    self_obj.root.grid_rowconfigure(0, weight=1)
    self_obj.root.grid_columnconfigure(0, weight=1)

    # Ajouter l'animation GIF
    update_gif_animation(self_obj)

    # Ajouter un titre
    title_label = tk.Label(self_obj.menu_frame, text="Démineur", font=("Arial", 24, "bold"))
    title_label.pack(pady=10)

    # Instructions et boutons
    tk.Label(self_obj.menu_frame, text="Choisissez la difficulté :", font=("Arial", 14)).pack(pady=10)
    buttons_frame = tk.Frame(self_obj.menu_frame)
    buttons_frame.pack(pady=10)

    for i, level in enumerate(self_obj.difficulty):
        button = tk.Button(
            buttons_frame, 
            text=level, 
            command=lambda l=level: self_obj.start_game(l),
            width=10,
            height=2,
            font=("Arial", 12),
            relief=tk.RAISED,
            bd=3
        )
        button.grid(row=0, column=i, padx=10)

def setup_game_interface(self_obj):
    """Configure l'interface de jeu."""
    if hasattr(self_obj, "menu_frame"):
        self_obj.menu_frame.destroy()

    self_obj.game_frame = tk.Frame(self_obj.root)
    self_obj.game_frame.pack(fill=tk.BOTH, expand=True)

    # Configuration responsive
    self_obj.root.grid_rowconfigure(0, weight=1)
    self_obj.root.grid_columnconfigure(0, weight=1)
    self_obj.game_frame.grid_rowconfigure(2, weight=1)
    self_obj.game_frame.grid_columnconfigure(0, weight=1)

    # Timer
    self_obj.timer_label = tk.Label(self_obj.game_frame, text="Temps: 0s")
    self_obj.timer_label.grid(row=0, column=0, columnspan=self_obj.cols, sticky="nsew")

    # Labels pour mines, drapeaux et points d'interrogation
    self_obj.mines_label = tk.Label(self_obj.game_frame, text=f"Mines: {self_obj.mines_count}", anchor="center")
    self_obj.mines_label.grid(row=1, column=0, sticky="nsew")

    self_obj.flags_label = tk.Label(self_obj.game_frame, text="Drapeaux: 0", anchor="center")
    self_obj.flags_label.grid(row=1, column=1, sticky="nsew")

    self_obj.questions_label = tk.Label(self_obj.game_frame, text="Points d'interrogation: 0", anchor="center")
    self_obj.questions_label.grid(row=1, column=2, sticky="nsew")

    # Plateau de jeu
    self_obj.board_frame = tk.Frame(self_obj.game_frame)
    self_obj.board_frame.grid(row=2, column=0, columnspan=self_obj.cols, sticky="nsew")

    for r in range(self_obj.rows):
        self_obj.board_frame.grid_rowconfigure(r, weight=1)
    for c in range(self_obj.cols):
        self_obj.board_frame.grid_columnconfigure(c, weight=1)

    for r in range(self_obj.rows):
        for c in range(self_obj.cols):
            btn = tk.Button(
                self_obj.board_frame, 
                width=2, height=1, 
                command=lambda x=r, y=c: self_obj.reveal(x, y)
            )
            btn.bind("<Button-3>", lambda e, x=r, y=c: self_obj.flag(x, y))
            btn.grid(row=r, column=c, sticky="nsew")
            self_obj.board[r][c] = {"btn": btn, "mine": False, "revealed": False, "flag": 0}