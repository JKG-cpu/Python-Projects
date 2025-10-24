import random
import math
from os import system, name

# Clear screen helper
def cc():
    system('cls' if name == 'nt' else 'clear')


class MiniMax:
    def __init__(self, ai_symbol: str, player_symbol: str, max_depth: int = 4):
        self.ai = ai_symbol
        self.player = player_symbol
        self.max_depth = max_depth

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        winner, piece = self.check_winner(board)
        if winner:
            if piece == self.ai:
                return 1000 - depth  # prefer faster wins
            elif piece == self.player:
                return -1000 + depth  # prefer slower losses

        if depth >= self.max_depth:
            return self.heuristic_score(board)

        if all(cell != "" for row in board for cell in row):
            return 0  # draw

        if is_maximizing:
            max_eval = -math.inf
            for r, c in self.available_moves(board):
                board[r][c] = self.ai
                eval = self.minimax(board, depth + 1, alpha, beta, False)
                board[r][c] = ""
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # beta cut-off
            return max_eval
        else:
            min_eval = math.inf
            for r, c in self.available_moves(board):
                board[r][c] = self.player
                eval = self.minimax(board, depth + 1, alpha, beta, True)
                board[r][c] = ""
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # alpha cut-off
            return min_eval

    def best_move(self, board):
        best_score = -math.inf
        best_move = None
        for r, c in self.available_moves(board):
            board[r][c] = self.ai
            score = self.minimax(board, 0, -math.inf, math.inf, False)
            board[r][c] = ""
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move

    @staticmethod
    def available_moves(board):
        # Prefer center columns first for stronger play
        order = [3, 2, 4, 1, 5, 0, 6]
        moves = []
        for col in order:
            for row in range(5, -1, -1):
                if board[row][col] == "":
                    moves.append((row, col))
                    break
        return moves

    @staticmethod
    def check_winner(board):
        for row in range(6):
            for col in range(7):
                piece = board[row][col]
                if piece == "":
                    continue
                # Horizontal
                if col <= 3 and all(board[row][col + i] == piece for i in range(4)):
                    return True, piece
                # Vertical
                if row <= 2 and all(board[row + i][col] == piece for i in range(4)):
                    return True, piece
                # Diagonal down-right
                if row <= 2 and col <= 3 and all(board[row + i][col + i] == piece for i in range(4)):
                    return True, piece
                # Diagonal down-left
                if row <= 2 and col >= 3 and all(board[row + i][col - i] == piece for i in range(4)):
                    return True, piece
        return False, ""

    def heuristic_score(self, board):
        """
        Simple heuristic: count 2-in-a-row and 3-in-a-row for AI (+) and Player (-)
        """
        score = 0
        for row in range(6):
            for col in range(7):
                piece = board[row][col]
                if piece == "":
                    continue
                # Horizontal
                if col <= 3:
                    line = [board[row][col + i] for i in range(4)]
                    score += self.line_score(line)
                # Vertical
                if row <= 2:
                    line = [board[row + i][col] for i in range(4)]
                    score += self.line_score(line)
                # Diagonal down-right
                if row <= 2 and col <= 3:
                    line = [board[row + i][col + i] for i in range(4)]
                    score += self.line_score(line)
                # Diagonal down-left
                if row <= 2 and col >= 3:
                    line = [board[row + i][col - i] for i in range(4)]
                    score += self.line_score(line)
        return score

    def line_score(self, line):
        if line.count(self.ai) == 4:
            return 100
        elif line.count(self.ai) == 3 and line.count("") == 1:
            return 5
        elif line.count(self.ai) == 2 and line.count("") == 2:
            return 2
        elif line.count(self.player) == 3 and line.count("") == 1:
            return -4
        elif line.count(self.player) == 2 and line.count("") == 2:
            return -2
        else:
            return 0


class ConnectFour:
    def __init__(self):
        self.board = [["" for _ in range(7)] for _ in range(6)]
        self.player = "X"
        self.ai = "O"
        self.minimax = MiniMax(self.ai, self.player, max_depth=4)

    def display_board(self):
        numbered_row = "   1   2   3   4   5   6   7"
        split_row = "+-----------------------------+"
        print(numbered_row)
        print(split_row)
        for row in self.board:
            print(" |", end="")
            for col in row:
                square = col if col != "" else " "
                print(f" {square} |", end="")
            print()
        print(split_row)
        print(numbered_row)

    def play_piece(self, column, piece):
        column -= 1
        for row in range(5, -1, -1):
            if self.board[row][column] == "":
                self.board[row][column] = piece
                return row
        return -1

    def check_draw(self):
        return all(cell != "" for row in self.board for cell in row)

    def play(self):
        turn = random.choice([self.player, self.ai])
        run = True

        while run:
            cc()
            self.display_board()
            if turn == self.player:
                try:
                    col = int(input("Your move (1-7): "))
                    if not 1 <= col <= 7:
                        print("Invalid column. Try 1-7.")
                        input("Press Enter to continue...")
                        continue
                except ValueError:
                    print("Invalid input. Enter a number 1-7.")
                    input("Press Enter to continue...")
                    continue

                row = self.play_piece(col, self.player)
                if row == -1:
                    print("Column full! Try again.")
                    input("Press Enter to continue...")
                    continue

                winner, piece = MiniMax.check_winner(self.board)
                if winner:
                    cc()
                    self.display_board()
                    print("You win!")
                    break

                if self.check_draw():
                    cc()
                    self.display_board()
                    print("It's a draw!")
                    break

                turn = self.ai

            else:
                print("AI is thinking...")
                move = self.minimax.best_move(self.board)
                row, col = move
                self.play_piece(col + 1, self.ai)

                winner, piece = MiniMax.check_winner(self.board)
                if winner:
                    cc()
                    self.display_board()
                    print("AI wins!")
                    break

                if self.check_draw():
                    cc()
                    self.display_board()
                    print("It's a draw!")
                    break

                turn = self.player


if __name__ == "__main__":
    game = ConnectFour()
    game.play()
