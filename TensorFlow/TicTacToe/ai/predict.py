# ai/predict.py
import numpy as np
import tensorflow as tf

class TF_AI:
    def __init__(self, model_path="data/model/tictactoe_model.h5"):
        self.model = tf.keras.models.load_model(model_path)

    def get_best_move(self, board: list[int]):
        """
        Chooses the move with the highest predicted evaluation for AI (-1).
        """
        best_value = -float('inf')
        best_move = None

        for i in range(9):
            if board[i] == 0:
                board[i] = -1  # AI move
                value = self.model.predict(np.array([board]), verbose=0)[0][0]
                board[i] = 0
                if value > best_value:
                    best_value = value
                    best_move = i

        return best_move
