from game import *
from utils import *

b = Board()
db = b.generate_board()
b.make_move(db, 1, 1)
b.make_move(db, 3, -1)
b.make_move(db, 8, 1)

display_board(db)