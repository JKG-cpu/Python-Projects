from src import *

map = Map()

board_size = "Small"

# Generate Forest
board, tile_key = map.new_board("Forest", *board_sizes[board_size], board_size)

map.display_board(board)