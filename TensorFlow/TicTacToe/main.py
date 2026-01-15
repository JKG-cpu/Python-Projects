import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0 = all, 1 = info, 2 = warning, 3 = error only

from game import *
from utils import *
from ai import *
from eval_bar import EvalBar

game = GameLoop(display_board, get_board_input, cc, Minimax, EvalBar)
game.play(False)
