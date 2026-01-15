import numpy as np
from tensorflow.keras.models import load_model

from ai import *

class EvalBar:
    def __init__(self):
        self.model = load_model("data/model/tictactoe_model.h5", compile = False)

    def predict(self, board_state: list[int]):
        board = np.array(board_state, dtype = np.float32).reshape(1, 9)
        return self.model.predict(board)[0][0]
