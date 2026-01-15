class Board:
    def make_move(self, board: list[int], index: int, number: int) -> None:
        board[index] = number

    def generate_board(self) -> list[int]:
        return [0, 0, 0, 0, 0, 0, 0, 0, 0]

