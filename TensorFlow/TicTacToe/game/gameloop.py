from .board import Board
from .logic import check_winner, valid_move

class GameLoop:
    def __init__(self, display_board, get_board_input, cc, ai, eval_bar) -> None:
        self.board = Board()

        self.display_board = display_board
        self.get_board_input = get_board_input
        self.cc = cc
        self.ai = ai(check_winner)
        self.eval_bar = eval_bar()

    def play(self, human_v_human: bool = True) -> None:
        self.cc()

        board = self.board.generate_board()
        turn = 1

        while check_winner(board) == 0:
            if human_v_human:
                self.display_board(board)
                # Get Eval
                print(self.eval_bar.predict(board))

                move = self.get_board_input()
                
                vmove = valid_move(board, move)
                
                if vmove:
                    self.board.make_move(board, move, turn)
                    turn = 1 if turn == -1 else -1
                
                else:
                    print("Not a valid move...")
                    input("Press Enter to continue > ")
            
            else:
                if turn == 1:
                    # Human Turn
                    self.display_board(board)
                    print(self.eval_bar.predict(board))

                    move = self.get_board_input()
                    
                    vmove = valid_move(board, move)
                    
                    if vmove:
                        self.board.make_move(board, move, turn)
                        turn = -1
                    
                    else:
                        print("Not a valid move...")
                        input("Press Enter to continue > ")
            
                elif turn == -1:
                    # Ai Turn
                    best_move = self.ai.get_best_move(board)
                    self.board.make_move(board, best_move, -1)
                    turn = 1

            self.cc()

        self.display_board(board)
        winner = check_winner(board)
        if winner == 2:
            print("It was a draw!")
        else:
            print(f"Player {"X" if winner == 1 else "O"} has won the game!")

