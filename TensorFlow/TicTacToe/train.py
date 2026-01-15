# train.py
import csv
import numpy as np
from ai.model import create_model

def load_data(filename="data/model/games.csv"):
    boards = []
    values = []

    with open(filename, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            board = [int(x) for x in row[:9]]
            value = float(row[9])

            boards.append(board)
            values.append(value)

    # 🔑 Force correct shapes
    X = np.array(boards, dtype=np.float32)
    y = np.array(values, dtype=np.float32)

    return X, y


def train_model():
    X, y = load_data()

    # 🔍 sanity check (you can delete later)
    print("X shape:", X.shape)
    print("y shape:", y.shape)

    model = create_model()
    model.fit(
        X,
        y,
        epochs=50,
        batch_size=32,
        verbose=1
    )

    model.save("data/model/tictactoe_model.h5")
    print("Training complete and model saved.")


if __name__ == "__main__":
    train_model()
