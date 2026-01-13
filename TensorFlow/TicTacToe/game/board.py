from VividText import VividText as vt

class Board:
    def __init__(self):
        self.printer = vt(bold = True, sleep = 0)

    def make_move(self, board: list[int], index: int, number: int) -> None:
        board[index] = number

    def generate_board(self) -> list[int]:
        return [0, 0, 0, 0, 0, 0, 0, 0, 0]

