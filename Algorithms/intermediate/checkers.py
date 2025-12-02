from VividText import VividText as vt
from rich.console import Console
from os import system, name

def cc():
    system("cls" if name == "nt" else "clear")

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
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            directions = [(1, -1), (1, 1)] if self.color == "red" else [(-1, -1), (-1, 1)]

        row, col = self.position

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                next_square = board[new_row][new_col]

                # Normal move
                if next_square is None:
                    moves.append((new_row, new_col, False))

                # Jump
                elif isinstance(next_square, CheckerPiece) and next_square.team != self.team:
                    jump_row, jump_col = new_row + dr, new_col + dc
                    if 0 <= jump_row < 8 and 0 <= jump_col < 8:
                        if board[jump_row][jump_col] is None:
                            moves.append((jump_row, jump_col, True))
        return moves

    def reset_position(self, row, col):
        self.position = (row, col)

class CheckerBoard:
    def __init__(self):
        self.console = Console()
        self.console.style = "bold white"

    def _generate_board(self):
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

    def display_board(self, board):
        top_row = "    A   B   C   D   E   F   G   H"
        split_row = " +" + "----" * 8 + "-+"

        self.console.print(top_row)
        self.console.print(split_row)

        for i, row in enumerate(board, 1):
            self.console.print(f"{i} | ", end='')
            for j, col in enumerate(row):
                coord = (i - 1, j)

                # Normal piece rendering
                if isinstance(col, CheckerPiece):
                    self.console.print(f"[{col.color}]{col}[/]", end=' | ')
                else:
                    self.console.print(" ", end=' | ')
            self.console.print(i)

        self.console.print(split_row)
        self.console.print(top_row)

    def check_force_kill(self, team, board):
        """
        Returns a tuple (forced_start_pieces_list, forced_target_positions_set)
        - forced_start_pieces_list: list of CheckerPiece objects that have at least one capture
        - forced_target_positions_set: set of (row, col) tuples that are landing spots for captures
        Returns ([], set()) if none.
        """
        forced_pieces = []
        forced_targets = set()

        for row in board:
            for piece in row:
                if isinstance(piece, CheckerPiece) and piece.team == team:
                    moves = piece.get_valid_moves(board)
                    has_kill = False
                    for r, c, kill in moves:
                        if kill:
                            forced_targets.add((r, c))
                            has_kill = True
                    if has_kill:
                        forced_pieces.append(piece)

        return forced_pieces, forced_targets

    def check_valid_move(self, board, row, col, trow, tcol):
        piece = board[row][col]
        if isinstance(piece, CheckerPiece):
            for r, c, kill in piece.get_valid_moves(board):
                if r == trow and c == tcol:
                    return True, kill
        return False, False

    def move_piece(self, board, row, col, trow, tcol, kill=False):
        piece = board[row][col]
        if kill:
            mid_row = (row + trow) // 2
            mid_col = (col + tcol) // 2
            board[mid_row][mid_col] = None
        board[trow][tcol], board[row][col] = piece, None
        piece.reset_position(trow, tcol)

class MiniMax:
    def __init__(self, team: str, player_team: str, max_depth: int) -> None:
        self.team = team
        self.player_team = player_team
        self.max_depth = max_depth

class InputParser:
    def __init__(self):
        self.vt = vt(bold=True, sleep=0.03)
        self.letters = "abcdefgh"

    def convert(self, msg):
        msg = msg.lower().strip()
        if len(msg) != 4:
            return None
        a, b, c, d = msg
        if a not in self.letters or c not in self.letters:
            return None
        if not b.isdigit() or not d.isdigit() or not (1 <= int(b) <= 8) or not (1 <= int(d) <= 8):
            return None
        return [int(b)-1, self.letters.index(a), int(d)-1, self.letters.index(c)]

    def parse_piece(self):
        while True:
            user_input = self.vt.inputTypewriter("Enter a move (e.g., b1a2) or type quit").lower().strip()
            if user_input.startswith("q"):
                return False
            coords = self.convert(user_input)
            if coords:
                return coords
            self.vt.typewriter("Invalid input. Use format letter-number-letter-number (e.g., b1a2).")

class Main:
    def __init__(self):
        self.running = True
        self.vt = vt(color="White", bold=True, sleep=0.03)
        self.movevt = vt(color="bright_blue", bold=True, sleep=0.03)
        self.turn = 0  # 0 = Blue, 1 = Red

        self.boardClass = CheckerBoard()
        self.board = self.boardClass._generate_board()
        self.inputParser = InputParser()

    def main(self):
        while self.running:
            team_color = "blue" if self.turn == 0 else "red"

            # Display board with highlights
            self.boardClass.display_board(self.board)

            # Announce turn
            if self.turn == 0:
                self.movevt.reset_style(color="bright_blue", bold=True)
                self.movevt.typewriter("Blue's Turn!")
            else:
                self.movevt.reset_style(color="bright_red", bold=True)
                self.movevt.typewriter("Red's Turn!")

            move = self.inputParser.parse_piece()
            if move is False:
                self.running = False
                cc()
                continue

            row, col, nrow, ncol = move
            piece = self.board[row][col]

            # Validate current player's piece
            if piece is None or (self.turn == 0 and piece.color != "blue") or (self.turn == 1 and piece.color != "red"):
                self.vt.typewriter("You must move your own piece!")
                cc()
                continue

            valid, kill = self.boardClass.check_valid_move(self.board, row, col, nrow, ncol)
            if valid:
                self.boardClass.move_piece(self.board, row, col, nrow, ncol, kill)
                self.turn = 1 - self.turn
            else:
                self.vt.typewriter("That is not a valid move...")
                self.vt.inputTypewriter("Press Enter to continue.", end=" ")
            
            cc()

if __name__ == "__main__":
    main = Main()
    main.main()
