# ai/memory.py

class Memory:
    def __init__(self, minimax_class, check_winner_fn):
        self.check_winner = check_winner_fn
        self.minimax = minimax_class(check_winner_fn)
        self.data = []

    def generate_all_states(self, board=None, turn=-1):
        if board is None:
            board = [0] * 9

        winner = self.check_winner(board)

        # TERMINAL BOARDS ONLY
        if winner != 0:
            if winner == -1:
                value = 1
            elif winner == 1:
                value = -1
            else:
                value = 0

            self.data.append((board.copy(), value))
            return

        # recurse deeper
        for i in range(9):
            if board[i] == 0:
                board[i] = turn
                self.generate_all_states(board, -turn)
                board[i] = 0
    def save_to_csv(self, filename="data/model/games.csv"):
        import csv
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            for board, value in self.data:
                writer.writerow(board + [value])
