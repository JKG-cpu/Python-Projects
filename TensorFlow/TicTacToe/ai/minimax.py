from math import inf

class Minimax:
    def __init__(self, check_winner):
        self.check_winner = check_winner

    def possible_moves(self, board: list[int]) -> list:
        return [i for i, spot in enumerate(board) if spot == 0]

    def minimax(self, board: list[int], is_maximizing: bool):
        winner = self.check_winner(board)
        if winner == 1:
            return -1
        
        elif winner == -1:
            return 1

        elif winner == 2:
            return 0

        if is_maximizing:
            best_score = -inf
            for move in self.possible_moves(board):
                board[move] = -1
                score = self.minimax(board, False)
                board[move] = 0
                best_score = max(score, best_score)
            return best_score
    
        else:
            best_score = inf
            for move in self.possible_moves(board):
                board[move] = 1
                score = self.minimax(board, True)
                board[move] = 0
                best_score = min(score, best_score)
            return best_score

    def get_best_move(self, board: list[int]) -> int:
        best_score = -inf
        best_move = None
        for move in self.possible_moves(board):
            board[move] = -1
            score = self.minimax(board, False)
            board[move] = 0
            if score > best_score:
                best_score = score
                best_move = move
            
        return best_move