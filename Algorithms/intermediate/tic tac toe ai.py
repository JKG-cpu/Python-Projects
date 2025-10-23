import math
import random

class TicTacToe:
    def __init__(self):
        # 3x3 board
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.player = "O"
        self.ai = "X"

        # Mapping for positions
        self.positions = {
            "top left": (0, 0), "top": (0, 1), "top right": (0, 2),
            "left": (1, 0), "center": (1, 1), "right": (1, 2),
            "bottom left": (2, 0), "bottom": (2, 1), "bottom right": (2, 2)
        }

    # Display the board
    def print_board(self):
        print("\n")
        for i, row in enumerate(self.board):
            print(" | ".join(row))
            if i < 2:
                print("--+---+--")
        print("\n")

    # Check winner
    def check_winner(self):
        b = self.board
        # Rows and columns
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != " ":
                return b[i][0]
            if b[0][i] == b[1][i] == b[2][i] != " ":
                return b[0][i]
        # Diagonals
        if b[0][0] == b[1][1] == b[2][2] != " ":
            return b[0][0]
        if b[0][2] == b[1][1] == b[2][0] != " ":
            return b[0][2]
        return None

    # Check draw
    def is_draw(self):
        return all(cell != " " for row in self.board for cell in row)

    # Available moves
    def available_moves(self):
        moves = []
        for name, (r, c) in self.positions.items():
            if self.board[r][c] == " ":
                moves.append(name)
        return moves

    # Make a move
    def make_move(self, position, player):
        if position not in self.positions:
            return False
        r, c = self.positions[position]
        if self.board[r][c] == " ":
            self.board[r][c] = player
            return True
        return False

    # Minimax algorithm
    def minimax(self, is_maximizing):
        winner = self.check_winner()
        if winner == self.ai:
            return 1
        elif winner == self.player:
            return -1
        elif self.is_draw():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for move in self.available_moves():
                r, c = self.positions[move]
                self.board[r][c] = self.ai
                score = self.minimax(False)
                self.board[r][c] = " "
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for move in self.available_moves():
                r, c = self.positions[move]
                self.board[r][c] = self.player
                score = self.minimax(True)
                self.board[r][c] = " "
                best_score = min(score, best_score)
            return best_score

    # Get best move for AI
    def get_best_move(self):
        best_score = -math.inf
        best_move = None
        for move in self.available_moves():
            r, c = self.positions[move]
            self.board[r][c] = self.ai
            score = self.minimax(False)
            self.board[r][c] = " "
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    # Play the game
    def play(self):
        print("Welcome to Tic Tac Toe!")
        print("You are 'O', the AI is 'X'.")
        print("Positions you can use:")
        print("top left | top | top right")
        print("left     | center | right")
        print("bottom left | bottom | bottom right\n")

        ai_turn = random.choice([True, False])

        while not self.check_winner() and not self.is_draw():
            self.print_board()

            if ai_turn:
                print("AI's turn...")
                move = self.get_best_move()
                self.make_move(move, self.ai)
            else:
                while True:
                    move = input("Your move: ").strip().lower()
                    if self.make_move(move, self.player):
                        break
                    else:
                        print("Invalid move! Try again.")

            ai_turn = not ai_turn

        # Game over
        self.print_board()
        winner = self.check_winner()
        if winner == self.ai:
            print("AI wins!")
        elif winner == self.player:
            print("You win! Congratulations!")
        else:
            print("It's a tie!")


if __name__ == "__main__":
    game = TicTacToe()
    game.play()
