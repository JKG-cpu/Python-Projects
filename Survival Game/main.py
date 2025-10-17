from src import *

class Game:
    def __init__(self):
        # Attributes

        # Classes
        self.map = Map()
    
    def play(self, map_size):
        board, tile_key, player_pos = self.map.new_board("Forest", *board_sizes[map_size], map_size)
    
        self.map.display_board(board)
        print()
        maintp.typewriter(f"Player Pos: {player_pos}")
        
if __name__ == "__main__":
    game = Game()
    game.play("Giant")