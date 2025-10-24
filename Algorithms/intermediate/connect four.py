import random
from os import system, name

def cc():
    system('cls' if name == 'nt' else 'clear')

class ConnectFour:
    def __init__(self):
        self.board = self.new_board()
        self.player = "X"
        self.ai = "O"

    # Board Logic
    def new_board(self) -> list:
        """
          1    2    3    4    5    6    7
        [" ", " ", " ", " ", " ", " ", " "],  # Row 0 (top)
        [" ", " ", " ", " ", " ", " ", " "],  # Row 1
        [" ", " ", " ", " ", " ", " ", " "],  # Row 2
        [" ", " ", " ", " ", " ", " ", " "],  # Row 3
        [" ", " ", " ", " ", " ", " ", " "],  # Row 4
        [" ", " ", " ", " ", " ", " ", " "]   # Row 5 (bottom)
          1    2    3    4    5    6    7
        """
        board = [
            ["" for _ in range(7)] for _ in range(6)
        ]
        return board

    def display_board(self) -> None:
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

    def play_piece(self, column: int, piece: str) -> int:
        """
        Drops a piece into the given column.
        Returns the row where the piece landed, or -1 if column is full.
        """
        column -= 1  # adjust 1-based input to 0-based index

        for row in range(5, -1, -1):
            if self.board[row][column] == "":
                self.board[row][column] = piece
                return row  # return the row for winner check
        return -1  # column is full

    def check_winner(self) -> tuple[bool, str]:
        """
        Scans the entire board to find a winner.
        Returns:
            (True, "X"/"O") if a winner is found
            (False, "") if no winner
        """
        for row in range(6):
            for col in range(7):
                piece = self.board[row][col]
                if piece == "":
                    continue  # empty cell, skip

                # Horizontal (right)
                if col <= 3:
                    if all(self.board[row][col + i] == piece for i in range(4)):
                        return (True, piece)

                # Vertical (down)
                if row <= 2:
                    if all(self.board[row + i][col] == piece for i in range(4)):
                        return (True, piece)

                # Diagonal down-right (\)
                if row <= 2 and col <= 3:
                    if all(self.board[row + i][col + i] == piece for i in range(4)):
                        return (True, piece)

                # Diagonal down-left (/)
                if row <= 2 and col >= 3:
                    if all(self.board[row + i][col - i] == piece for i in range(4)):
                        return (True, piece)

        return (False, "")

    def play(self):
        turn = random.choice([self.ai, self.player])

        run = True
        while run:
            if turn == self.player:
                # Display board
                self.display_board()
                
                # Get Move
                user_input = input("Where would you like to drop a piece? > ")
                return_value = self.play_piece(int(user_input), self.player)

                if return_value != -1:
                    turn = self.ai

                else:
                    print("That column is full!")
                    input("Press Enter to continue.")
            
            else:
                # Minimax
                run = False
            
            cc()
        
        self.display_board()

if __name__ == "__main__":
    game = ConnectFour()
    game.play()