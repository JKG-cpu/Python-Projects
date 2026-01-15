# ai/generate.py
from .memory import Memory
from .minimax import Minimax

def check_winner(board):
    wins = (
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    )

    for a,b,c in wins:
        s = board[a] + board[b] + board[c]
        if s == 3:
            return 1
        if s == -3:
            return -1

    if all(x != 0 for x in board):
        return 2

    return 0


if __name__ == "__main__":
    memory = Memory(Minimax, check_winner)
    memory.generate_all_states()
    memory.save_to_csv()

    print("Generated samples:", len(memory.data))
