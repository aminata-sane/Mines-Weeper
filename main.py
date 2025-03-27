import tkinter as tk
from demineur import Demineur

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Démineur Aventure")
    
    # Définir la taille initiale de la fenêtre
    root.geometry("800x600")
    
    # Permettre à la fenêtre d'être redimensionnée
    root.resizable(True, True)
    
    # Configurer le style global
    root.configure(bg="#f0f0f0")
    
    # Message de bienvenue 
    welcome_frame = tk.Frame(root, bg="#f0f0f0", pady=10)
    welcome_frame.pack(fill="x")
    
    title = tk.Label(
        welcome_frame, 
        text="DÉMINEUR AVENTURE", 
        font=("Arial", 20, "bold"),
        fg="#333",
        bg="#f0f0f0"
    )
    title.pack()
    
    subtitle = tk.Label(
        welcome_frame,
        text="Guidez votre personnage à travers le champ de mines !",
        font=("Arial", 12),
        fg="#555",
        bg="#f0f0f0"
    )
    subtitle.pack(pady=5)
    
    app = Demineur(root)
    app.pack(pady=10, padx=10, fill="both", expand=True)
    
    root.mainloop()