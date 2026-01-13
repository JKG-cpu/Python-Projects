def valid_move(board: list[int], index: int):
    return True if board[index] == 0 else False

def check_winner(board: list[int], index: int) -> int:
    player = board[index]
    if player == 0:
        return 0

    row = index // 3
    col = index % 3

    # Check row
    if sum(board[row * 3:(row + 1) * 3]) == player * 3:
        return player

    # Check column
    if sum(board[col::3]) == player * 3:
        return player

    # Check main diagonal
    if index in (0, 4, 8):
        if board[0] + board[4] + board[8] == player * 3:
            return player

    # Check anti-diagonal
    if index in (2, 4, 6):
        if board[2] + board[4] + board[6] == player * 3:
            return player

    return 0
