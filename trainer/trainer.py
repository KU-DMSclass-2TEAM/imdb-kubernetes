import argparse
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Embedding, Bidirectional, Dense
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--epoch", type=int, required=True)
    parser.add_argument("--batch", type=int, required=True)
    parser.add_argument("--savemodel", type=str, required=True)
    args = parser.parse_args()

    dir_path = os.path.dirname(args.savemodel)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    imdb = np.load(args.data)
    train_x, train_y = imdb['x'], imdb['y']

    model = tf.keras.models.Sequential()
    model.add(Embedding(10000, 100))
    model.add(Bidirectional(GRU(128, return_sequences=True)))
    model.add(Bidirectional(GRU(128)))
    model.add(Dense(1,activation='sigmoid'))
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(x=train_x, y=train_y, epochs=args.epoch, batch_size=args.batch)
    model.save(args.savemodel)
