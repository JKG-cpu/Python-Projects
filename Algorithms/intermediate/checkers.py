import random
from rich.console import Console
from os import system, name

def cc():
    system("cls" if name == 'nt' else "clear")

class CheckerPiece:
    def __init__(self, color: str, position: tuple):
        self.color = color
        self.position = position
        self.is_king = False
    
    def __str__(self):
        return f"{self.color}"
    
    def get_possible_moves(self, board: list) -> list:
        max_x, max_y = len(board), len(board[0])
        normal_moves = []
        jump_moves = []

        # Define directions
        if self.color == "B":
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if self.is_king else [(-1, -1), (-1, 1)]
        elif self.color == "R":
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if self.is_king else [(1, -1), (1, 1)]

        x, y = self.position

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < max_x and 0 <= new_y < max_y:
                target = board[new_x][new_y]
                if target == "":
                    normal_moves.append((new_x, new_y))
                elif isinstance(target, CheckerPiece) and target.color != self.color:
                    jump_x, jump_y = new_x + dx, new_y + dy
                    if 0 <= jump_x < max_x and 0 <= jump_y < max_y and board[jump_x][jump_y] == "":
                        jump_moves.append((jump_x, jump_y))

        return jump_moves if jump_moves else normal_moves

    def reset_position(self, r, c):
        self.position = (r, c)

class Checkers:
    def __init__(self) -> None:
        self.printer = Console()
        self.printer.style = "bold white"
        
        self.board = self._generate_board()
        self.player = "R"
        self.ai = "B"

    # Generate / Display Board
    #region
    def _generate_board(self, size=8) -> list:
        board = []

        for row in range(size):
            board_row = []
            for col in range(size):
                # Top 3 rows: Black pieces on alternating squares
                if row < 3 and (row + col) % 2 == 1:
                    board_row.append(CheckerPiece("R", (row, col)))
                # Bottom 3 rows: Red pieces on alternating squares
                elif row >= size - 3 and (row + col) % 2 == 1:
                    board_row.append(CheckerPiece("B", (row, col)))
                else:
                    board_row.append("")
            board.append(board_row)

        return board

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
    #endregion

    # Logic
    #region
    def make_move(self, row: int, col: int, nrow: int, ncol: int) -> bool:
        square = self.board[row][col]
        if (nrow, ncol) in square.get_possible_moves(self.board):
            square.reset_position(row, col)
            self.board[row][col], self.board[nrow][ncol] = "", square
            return True
        return False
    
    def select_piece(self, row, col) -> list:
        return self.board[row][col].get_possible_moves(self.board) if isinstance(self.board[row][col], CheckerPiece) else "Not A Piece"
    
    def check_game_over(self) -> str | None:
        def any_piece(board, color):
            return any(
                isinstance(cell, CheckerPiece) and cell.color == color
                for row in board for cell in row
            )

        def any_moves(board, color):
            return any(
                isinstance(cell, CheckerPiece) and cell.color == color and cell.get_possible_moves(board)
                for row in board for cell in row
            )

        red_exists = any_piece(self.board, "R")
        black_exists = any_piece(self.board, "B")
        red_can_move = any_moves(self.board, "R")
        black_can_move = any_moves(self.board, "B")

        # Check for winner based on pieces or moves
        if not red_exists or not red_can_move:
            return "B"
        elif not black_exists or not black_can_move:
            return "R"
        else:
            return None
    #endregion

    # Play Game
    def play(self):
        pass

if __name__ == '__main__':
    game = Checkers()
    game.display_board(game.board)
