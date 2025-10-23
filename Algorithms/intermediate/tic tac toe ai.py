class MiniMaxAI:
    def __init__(self):
        pass

class TicTacToe:
    def __init__(self):
        # 3x3 board initialized with spaces
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X always starts

        # Map human-readable positions to board coordinates
        self.positions = {
            "top left": (0, 0), "top": (0, 1), "top right": (0, 2),
            "left": (1, 0), "center": (1, 1), "right": (1, 2),
            "bottom left": (2, 0), "bottom": (2, 1), "bottom right": (2, 2)
        }

    def display_board(self):
        print("\n")
        for i, row in enumerate(self.board):
            print(" | ".join(row))
            if i < 2:
                print("--+---+--")
        print("\n")

    def make_move(self, position):
        # Ensure position is valid
        if position not in self.positions:
            print("Invalid position. Try again.")
            return False

        row, col = self.positions[position]

        # Check if the cell is empty
        if self.board[row][col] != ' ':
            print("That spot is already taken.")
            return False

        # Make the move
        self.board[row][col] = self.current_player
        return True

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        b = self.board
        # Rows and columns
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != ' ':
                return b[i][0]
            if b[0][i] == b[1][i] == b[2][i] != ' ':
                return b[0][i]

        # Diagonals
        if b[0][0] == b[1][1] == b[2][2] != ' ':
            return b[0][0]
        if b[0][2] == b[1][1] == b[2][0] != ' ':
            return b[0][2]

        return None  # No winner yet

    def is_draw(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def play(self):
        print("Welcome to Tic Tac Toe!")
        self.display_board()

        while True:
            move = input(f"Player {self.current_player}, enter your move: ").strip().lower()
            if not self.make_move(move):
                continue

            self.display_board()

            winner = self.check_winner()
            if winner:
                print(f"Player {winner} wins!")
                break

            if self.is_draw():
                print("It's a draw!")
                break

            self.switch_player()

if __name__ == '__main__':
    game = TicTacToe()
    game.play()