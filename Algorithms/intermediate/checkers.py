from VividText import VividText as vt
from rich.console import Console

class CheckerPiece:
    def __init__(self, position, team, color):
        self.position = position
        self.team = team
        self.color = color
        self.is_king = False

    def __str__(self):
        return self.team[0].title()

    def get_valid_moves(self, board) -> list[tuple[int, int, bool]]:
        moves = []
        if self.is_king:
            directions = [
                (-1, -1), (-1, 1),
                (1, -1), (1, 1)
            ]
        else:
            if self.color == "red":
                directions = [(1, -1), (1, 1)]
            else:
                directions = [(-1, -1), (-1, 1)]

        row, col = self.position

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                next_square = board[new_row][new_col]
                if next_square is None:
                    moves.append((new_row, new_col, False))
                elif isinstance(next_square, CheckerPiece):
                    if next_square.team != self.team:
                        jump_row = new_row + dr
                        jump_col = new_col + dc
                        if 0 <= jump_row < 8 and 0 <= jump_col < 8:
                            if board[jump_row][jump_col] is None:
                                moves.append((jump_row, jump_col, True))

        return moves

    def reset_position(self, row, col) -> None:
        self.position = (row, col)

class CheckerBoard:
    def __init__(self):
        self.console = Console()
        self.console.style = "bold white"

    def _generate_board(self) -> list:
        board = []
        for row in range(8):
            board_row = []
            for col in range(8):
                if row < 3 and (row + col) % 2 == 1:
                    board_row.append(CheckerPiece((row, col), "R", "red"))
                elif row >= 5 and (row + col) % 2 == 1:
                    board_row.append(CheckerPiece((row, col), "B", "blue"))
                else:
                    board_row.append(None)
            board.append(board_row)
        return board

    def display_board(self, board) -> None:
        # slot_space = 3
        top_row = "    A   B   C   D   E   F   G   H"
        split_row = " +" + "----" * 8 + "-+"

        self.console.print(top_row)
        self.console.print(split_row)

        for i, row in enumerate(board, 1):
            self.console.print(f"{i} | ", end = '')
            for col in row:
                if isinstance(col, CheckerPiece):
                    square = col
                    self.console.print(f"[{square.color}]{square}[/]", end = ' | ')

                else:
                    square = " "
                    self.console.print(square, end = ' | ')
            self.console.print(i)

        self.console.print(split_row)
        self.console.print(top_row)

    def move_piece(self, board, row, col, trow, tcol, kill=False):
        if kill:
            mid_row = (row + trow) // 2
            mid_col = (col + tcol) // 2
            board[mid_row][mid_col] = None
        board[trow][tcol], board[row][col] = board[row][col], None

class MiniMax:
    pass

class Main:
    def __init__(self):
        # Variables
        self.running = True
        self.vt = vt(color = "White", bold = True, sleep = .03)

        self.boardClass = CheckerBoard()
        self.board = self.boardClass._generate_board()

    def main(self):
        # DONE: Check Piece Double hopping (killing)
        # TODO: Start asking user for input and moving check pieces
        # TODO: Start forcing kills
        while self.running:
            self.running = False

if __name__ == "__main__":
    main = Main()
