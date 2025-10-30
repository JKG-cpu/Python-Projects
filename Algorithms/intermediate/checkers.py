import random
from rich.console import Console

class Checkers:
    def __init__(self) -> None:
        self.printer = Console()
        self.printer.style = "bold white"
        
        self.board = self._generate_board()
        self.player = "R"
        self.ai = "B"

    # Generate / Display Board
    def _generate_board(self, size=7) -> list:
        return [
            [
                "R" if (row < (size//2 - 1) and (row + col) % 2) else
                "B" if (row > size - (size//2) and (row + col) % 2) else
                ""
                for col in range(size)
            ]
            for row in range(size)
        ]

    def display_board(self, board):
        size = len(board)
        square_width = 3  # width of each square including spaces
        horizontal_border = "+-" + ("-" * (square_width + 1) * size) + "+"

        self.printer.print(horizontal_border)

        for row in board:
            row_str = " |"
            for col in row:
                if col != "":
                    row_str += f" {col} |"
                else:
                    row_str += "   |"
            self.printer.print(row_str)
            self.printer.print(horizontal_border)

    # Logic
    # Get all of player X's move
    def get_possible_moves(self, player: str = "R" | "B") -> list:
        pieces = []

        for i in range(7):
            for j in range(7):
                if self.board[i][j] == player:
                    pieces.append((i, j))

        return pieces

    def make_move(self, row: int, col: int, nrow: int, ncol: int) -> None:
        self.board[row][col], self.board[nrow][ncol] = "", self.board[row][col]

    # Play Game
    def play(self):
        pass

if __name__ == '__main__':
    game = Checkers()
    game.display_board(game.board)