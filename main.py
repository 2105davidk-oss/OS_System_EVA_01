import tkinter as tk
from tkinter import messagebox
import subprocess
import chess
import chess.engine

# Funktion zum Installieren der benötigten Programme
def install_required_programs():
    needed_progs = ["opencv-python", "python-chess", "wit"]
    for prog in needed_progs:
        try:
            subprocess.check_call(["pip", "install", prog])
        except subprocess.CalledProcessError:
            messagebox.showerror("Fehler", f"Fehler beim Installieren von {prog}")
            return
    messagebox.showinfo("Erfolg", "Alle benötigten Programme wurden erfolgreich installiert.")

# Funktion zum Starten des Schachspiels
def play_chess():
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    board = chess.Board()

    def make_move(move):
        nonlocal board
        if board.turn == chess.WHITE:
            result = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(result.move)
            update_board()
            if board.is_game_over():
                messagebox.showinfo("Spiel beendet", "Spiel beendet!")
        else:
            board.push_san(move)
            update_board()
            if board.is_game_over():
                messagebox.showinfo("Spiel beendet", "Spiel beendet!")

    def update_board():
        for widget in chess_board.winfo_children():
            widget.destroy()
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                label = tk.Label(chess_board, text=str(piece), font=("Helvetica", 16))
                label.grid(row=7 - square // 8, column=square % 8)
            else:
                label = tk.Label(chess_board, text="", font=("Helvetica", 16))
                label.grid(row=7 - square // 8, column=square % 8)

    def on_click(event):
        square = 8 * (7 - (event.y // 64)) + (event.x // 64)
        move = chess.square_name(square)
        make_move(move)

    root = tk.Tk()
    root.title("Schachspiel")

    chess_board = tk.Frame(root, width=512, height=512)
    chess_board.bind("<Button-1>", on_click)
    chess_board.grid(row=0, column=0)

    update_board()

    root.mainloop()

# Hauptprogramm
if __name__ == "__main__":
    install_required_programs()
    play_chess()
