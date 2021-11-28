import argparse
import numpy as np
import tensorflow as tf
import os

if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--n_container", type=int, required=True)
    #parser.add_argument("--savedir", type=str, required=True)

    #args = parser.parse_args()

    # Create output path if not exists
    if not os.path.exists("/imdb/data"):
        os.makedirs("/imdb/data")

    (train_x, train_y), (test_x, test_y) = tf.keras.datasets.imdb.load_data(num_words = 10000)

    max_len = 500
    print("flag1")
    train_x = tf.keras.preprocessing.sequence.pad_sequences(train_x, maxlen=max_len)
    test_x = tf.keras.preprocessing.sequence.pad_sequences(test_x, maxlen=max_len)
    print("flag2")


    n_data = len(train_x) // 5
    for name, i in enumerate(range(0, len(train_x), n_data)):
        start, end = i, i + n_data
        np.savez(os.path.join("/imdb/data", str(name)), x=train_x[start:end], y=train_y[start:end])
    print("flag3")
