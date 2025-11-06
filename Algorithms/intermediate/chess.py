import random
from rich.console import Console
from VividText import VividText as vt
from os import system, name

# Functions
def cc():
    system('cls' if name == 'nt' else 'clear')

# Chess Pieces
class Piece:
    def __init__(self, position, team, name, direction = None):
        self.position = position
        self.team = team
        self.name = name
        self.direction = direction

    def reset_position(self, row, col):
        self.position = (row, col)

    def __str__(self):
        return f"{self.name[0]}"

class Pawn(Piece):
    def __init__(self, position, team, name, direction):
        super().__init__(position, team, name, direction)

    def get_possible_moves(self, board) -> list:
        moves = []
        row, col = self.position
        direction = self.direction

        next_row = row + direction

        if 0 <= next_row < 8 and board[next_row][col] is None:
            moves.append((next_row, col))

            starting_row = 6 if direction == -1 else 1
            two_step = row + 2 * direction
            if row == starting_row and board[two_step][col] is None:
                moves.append((two_step, col))
        
        for dc in [-1, 1]:
            drow = row + direction
            dcol = col + dc
            if 0 <= drow < 8 and 0 <= dcol < 8:
                target = board[drow][dcol]
                if target and target.team != self.team:
                    moves.append((drow, dcol))

        return moves

class Knight(Piece):
    def __init__(self, position, team, name):
        super().__init__(position, team, name)
    
    def __str__(self):
        return f"{self.name[1].title()}"

    def get_possible_moves(self, board) -> list:
        moves = []
        row, col = self.position
        directions = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2),  (1, 2),
            (2, -1),  (2, 1)
        ]

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                dest_piece = board[nr][nc]

                if dest_piece is None or dest_piece.team != self.team:
                    moves.append((nr, nc))

        return moves

class Bishop(Piece):
    def __init__(self, position, team, name):
        super().__init__(position, team, name)

    def get_possible_moves(self, board) -> list:
        moves = []
        row, col = self.position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                square = board[new_row][new_col]

                if square is None:
                    moves.append((new_row, new_col))
                elif square.team != self.team:
                    moves.append((new_row, new_col))
                    break
                elif square.team == self.team:
                    break

                new_row += dr
                new_col += dc

        return moves

class Rook(Piece):
    def __init__(self, position, team, name):
        super().__init__(position, team, name)

    def get_possible_moves(self, board) -> list:
        moves = []
        row, col = self.position
        directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                square = board[new_row][new_col]

                if square is None:
                    moves.append((new_row, new_col))
                elif square.team != self.team:
                    moves.append((new_row, new_col))
                    break
                elif square.team == self.team:
                    break

                new_row += dr
                new_col += dc
        
        return moves

class Queen(Piece):
    def __init__(self, position, team, name):
        super().__init__(position, team, name)

    def get_possible_moves(self, board) -> list:
        moves = []
        row, col = self.position
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                next_square = board[new_row][new_col]

                if next_square is None:
                    moves.append((new_row, new_col))
                elif next_square.team != self.team:
                    moves.append((new_row, new_col))
                    break
                elif next_square.team == self.team:
                    break
            
                new_row += dr
                new_col += dc
        
        return moves

class King(Piece):
    def __init__(self, position, team, name):
        super().__init__(position, team, name)

    def handle_checks(self):
        pass

    def get_possible_moves(self, board) -> list:
        moves = []
        row, col = self.position
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                next_square = board[new_row][new_col]
            
                if next_square is None:
                    moves.append((new_row, new_col))
                
                elif next_square.team != self.team:
                    moves.append((new_row, new_col))
                
                else:
                    pass

# MiniMax AI
class MiniMax:
    pass

# Board Class
class Board:
    def __init__(self):
        self.piece_positions = {
            'White': {
                'Pawn':    [(6, i) for i in range(8)],
                'Rook':    [(7, 0), (7, 7)],
                'Knight':  [(7, 1), (7, 6)],
                'Bishop':  [(7, 2), (7, 5)],
                'Queen':   [(7, 3)],
                'King':    [(7, 4)],
            },
            'Black': {
                'Pawn':    [(1, i) for i in range(8)],
                'Rook':    [(0, 0), (0, 7)],
                'Knight':  [(0, 1), (0, 6)],
                'Bishop':  [(0, 2), (0, 5)],
                'Queen':   [(0, 3)],
                'King':    [(0, 4)],
            }
        }
        self.pieces = {
            "Pawn": Pawn,
            "Bishop": Bishop,
            "Knight": Knight,
            "Rook": Rook,
            "Queen": Queen,
            "King": King
        }
        self.empty = None

    # Board Methods
    def generate_board(self) -> list:
        board = [
            [self.empty for _ in range(8)] for _ in range(8)
        ]

        # Place Pieces
        for team in self.piece_positions:
            for piece in self.piece_positions[team]:
                for dr, dc in self.piece_positions[team][piece]:
                    if piece == "Pawn":
                        direction = -1 if team == "White" else 1
                        board[dr][dc] = self.pieces[piece]((dr, dc), team, piece, direction)
                    else:
                        board[dr][dc] = self.pieces[piece]((dr, dc), team, piece)

        return board

    def move_piece(self, board, r, c, nr, nc) -> None:
        piece = board[r][c]
        board[nr][nc] = piece
        board[r][c] = self.empty
        piece.reset_position(nr, nc)

    # Static Methods
    @staticmethod
    def display_board(board):
        console = Console()
        console.style = "bold white"

        columns = "abcdefgh"
        size = 8
        horizontal_line = "  +" + ("---+" * size)

        console.print('    ' + '   '.join(columns))

        for row in range(size):
            console.print(horizontal_line)
            row_cells = []
            for col in range(size):
                piece = board[row][col]
                if piece is None:
                    if (row + col) % 2 == 0:
                        cell = "   "
                    else:
                        cell = "[dim] . [/]"
                else:
                    color = "white" if piece.team == "White" else "bright_red"
                    cell = f"[bold {color}] {piece} [/]"
                row_cells.append(cell)
        
            console.print(f"{size - row} |" + "|".join(row_cells) + f"| {size - row}")

        console.print(horizontal_line)
        console.print('    ' + '   '.join(columns))

    @staticmethod
    def find_piece(board, piece_name, move) -> tuple | None:
        for row in board:
            for col in row:
                if isinstance(col, Piece):
                    if col.name == piece_name and move in col.get_possible_moves(board):
                        return col.position

        return None

# Input Parser
class InputParser:
    def __init__(self):
        self.vt = vt(color = "bright_blue", bold = True, sleep = 0.03)
        self.piece_nicknames = {
            "B": "Bishop",
            "N": "Knight",
            "R": "Rook",
            "Q": "Queen",
            "K": "King"
        }

    def parse_chessPiece_selection(self) -> tuple | bool:
        run = True

        while run:
            raw_input = self.vt.inputTypewriter("Make a move or type quit to quit")

            if raw_input.lower().startswith("q"):
                return False
        
            elif len(raw_input) == 2:
                piece_to_move = "Pawn"

                if raw_input[0].lower() in "abcdefgh" and raw_input[1] in '1345678':
                    col = 'abcdefgh'.index(raw_input[0].lower())
                    row = 8 - int(raw_input[1])
                    return (piece_to_move, (row, col))
            
            elif len(raw_input) == 3:
                piece_to_move = self.piece_nicknames[raw_input[0].upper()]

                if raw_input[1].lower() in 'abcdefgh' and raw_input[2] in '12345678':
                    col = 'abcdefgh'.index(raw_input[1].lower())
                    row = 8 - int(raw_input[2])

                    return (piece_to_move, (row, col))
        
            else:
                self.vt.typewriter("That is not a valid piece to move.")

# Main Class
class Main:
    def __init__(self):
        # Base Variables
        self.running = True

        # Classes
        self.boardClass = Board()
        self.inputParser = InputParser()

        self.board = self.boardClass.generate_board()

    def test(self):
        Board.display_board(self.board)

        return_value = self.inputParser.parse_chessPiece_selection()
        if isinstance(return_value, tuple):
            piece_to_move, pos = return_value
            
            # Find piece in chess board
            piece_position = Board.find_piece(self.board, piece_to_move, pos)

            if piece_position is None:
                print("That is not a valid move")
            
            else:
                self.boardClass.move_piece(self.board, piece_position[0], piece_position[1], pos[0], pos[1])
                Board.display_board(self.board)

        else:
            print("Quitting...")

    def play(self):
        while self.running:
            pass

if __name__ == '__main__':
    main = Main()
    main.test()