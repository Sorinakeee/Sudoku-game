import random
import tkinter as tk
from tkinter import messagebox

class SudokuBoard:

    def __init__(self, difficulty="medium"):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.difficulty = difficulty
        self.num_holes = self.set_difficulty()

    def set_difficulty(self):
        if self.difficulty == "easy":
            return random.randint(36, 41)
        elif self.difficulty == "medium":
            return random.randint(42, 47)
        elif self.difficulty == "hard":
            return random.randint(48, 53)
        else:
            raise ValueError("Invalid difficulty level")

    def is_valid(self, row, col, num):
        if num in self.board[row]:
            return False

        for i in range(9):
            if self.board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def fill_grid(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            if self.fill_grid():
                                return True
                            self.board[row][col] = 0
                    return False
        return True

    def remove_numbers(self):
        count = self.num_holes
        while count > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count -= 1

    def generate_puzzle(self):
        self.fill_grid()
        self.remove_numbers()

    def solve(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            if self.solve():
                                return True
                            self.board[row][col] = 0
                    return False
        return True


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.difficulty = tk.StringVar(value="medium")
        self.sudoku_board = None
        self.cells = [[None for _ in range(9)] for _ in range(9)]

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select Difficulty:").grid(row=0, column=0, columnspan=3)
        difficulty_menu = tk.OptionMenu(self.root, self.difficulty, "easy", "medium", "hard")
        difficulty_menu.grid(row=0, column=3, columnspan=3)

        start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        start_button.grid(row=0, column=6, columnspan=3, pady=10)

        self.create_grid()

        solve_button = tk.Button(self.root, text="Solve", command=self.solve_puzzle)
        solve_button.grid(row=10, column=3, columnspan=3, pady=20)

        reset_button = tk.Button(self.root, text="Reset", command=self.reset_board)
        reset_button.grid(row=11, column=3, columnspan=3)

    def create_grid(self):
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=3, font=('Arial', 18), justify='center')
                self.cells[row][col] = entry
                entry.grid(row=row + 1, column=col, padx=5, pady=5)

    def start_game(self):
        difficulty = self.difficulty.get()
        self.sudoku_board = SudokuBoard(difficulty)
        self.sudoku_board.generate_puzzle()
        self.update_grid()

    def update_grid(self):
        for row in range(9):
            for col in range(9):
                entry = self.cells[row][col]
                entry.config(state='normal')
                entry.delete(0, tk.END)
                cell_value = self.sudoku_board.board[row][col]
                if cell_value != 0:
                    entry.insert(0, str(cell_value))
                    entry.config(state='disabled')

    def solve_puzzle(self):
        if self.sudoku_board and self.sudoku_board.solve():
            for row in range(9):
                for col in range(9):
                    entry = self.cells[row][col]
                    entry.delete(0, tk.END)
                    entry.insert(0, str(self.sudoku_board.board[row][col]))
        else:
            messagebox.showinfo("Sudoku", "No solution exists!")

    def reset_board(self):
        if self.sudoku_board:
            self.update_grid()


def main():
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
