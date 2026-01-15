# ai/model.py
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input

def create_model():
    model = Sequential([
        Input(shape=(9,)),          # <-- explicit input shape
        Dense(64, activation="relu"),
        Dense(64, activation="relu"),
        Dense(1, activation="linear")  # evaluation value
    ])

    model.compile(
        optimizer="adam",
        loss="mse"
    )

    return model
