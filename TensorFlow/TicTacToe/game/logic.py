def valid_move(board: list[int], index: int):
    return True if board[index] == 0 else False

def check_winner(board: list[int]) -> int:
    winning_lines = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

    for a, b, c in winning_lines:
        line_sum = board[a] + board[b] + board[c]
        if line_sum == 3:
            return 1
        if line_sum == -3:
            return -1

    if all(0 != num for num in board):
        return 2

    return 0
