import tkinter as tk
from demineur import Demineur

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Démineur")
    
    # Définir la taille initiale de la fenêtre
    root.geometry("800x600")
    
    # Permettre à la fenêtre d'être redimensionnée
    root.resizable(True, True)
    
    app = Demineur(root)
    root.mainloop()