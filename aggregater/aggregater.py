import os
import argparse
import tensorflow as tf
import numpy as np

def average(modelfiles):
    if len(modelfiles) == 0:
        raise Exception('model file is not found')

    modelfiles = [os.path.abspath(path) for path in modelfiles]
    models = []
    for idx, file in enumerate(modelfiles):
        models.append(tf.keras.models.load_model(file, compile=False))
        print('%d/%d files loaded' % (idx + 1, len(modelfiles)))

    weights = [model.get_weights() for model in models]
    new_weights = list()
    for weights_list_tuple in zip(*weights):
        new_weights.append([np.array(weights_).mean(axis=0) \
             for weights_ in zip(*weights_list_tuple)])

    model = tf.keras.models.load_model(modelfiles[0], compile=False)
    model.set_weights(new_weights)
    return model

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, required=True)
    parser.add_argument("--savefile", type=str, required=True)
    args = parser.parse_args()

    dirname = os.listdir(args.dir)
    models = list()

    for file in dirname:
        filename = os.path.join(args.dir, file)
        ext = os.path.splitext(filename)[-1].strip()
        if ext == '.h5':
            models.append(filename)

    averaged_model = average(models)
    averaged_model.save(args.savefile)
