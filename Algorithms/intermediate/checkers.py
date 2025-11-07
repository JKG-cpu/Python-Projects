from VividText import VividText as vt

class CheckerPiece:
    def __init__(self, position, team, color):
        self.position = position
        self.team = team
        self.color = color
        self.is_king = False
    
    def get_valid_moves(self, board) -> list[tuple[int, int, bool]]:
        moves = []
        if self.is_king:
            directions = [
                (-1, -1), (-1, 1),
                (1, -1), (1, 1)
            ]
        else:
            directions = [
                (-1, -1), (-1, 1)
            ]
        row, col = self.position

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                next_square = board[new_row][new_col]
                if next_square is None:
                    moves.append((new_row, new_col, False))
                elif isinstance(next_square, CheckerPiece):
                    if next_square.team == self.team:
                        pass

                    elif next_square.team != self.team:
                        new_row, new_col = new_row + dr, new_col + dc
                        if 0 <= new_row < 8 and 0 <= new_col < 8:
                            next_square = board[new_row][new_col]
                            if next_square is None:
                                moves.append((new_row, new_col, True))

        return moves

    def reset_position(self, row, col) -> None:
        self.position = (row, col)

class CheckerBoard:
    def __init__(self):
        self.vt = vt(bold = True, sleep = 0)
    
    def _generate_board(self) -> list:
        board = []
        
        for row in range(8):
            board_row = []
            for col in range(8):
                if row < 3 and (row + col) % 2 == 1:
                    board_row.append(CheckerPiece((row, col), "R", "red"))
                elif row >= 8 - 3 and (row + col) % 2 == 1:
                    board_row.append(CheckerPiece((row, col), "B", "blue"))
                else:
                    board_row.append(None)
            board.append(board_row)

        return board

    def _display_board(self, board):
        top_row = "abcdefgh"
        
        for row in board:
            for col in row:
                square = ""

class MiniMax:
    pass

class Main:
    def __init__(self):
        # Variables
        self.running = True
        self.vt = vt(color = "White", bold = True, sleep = .03)

        self.boardClass = CheckerBoard()
        self.board = self.boardClass._generate_board()

    def test(self):
        pass