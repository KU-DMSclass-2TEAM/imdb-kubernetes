import os
import argparse
import tensorflow as tf
import numpy as np
from keras.models import load_model
from keras.models import clone_model
from numpy import average
from numpy import array

def model_weight_ensemble(members, weights):
    n_layers = len(members[0].get_weights())
    avg_model_weights = list()
    for layer in range(n_layers):
        layer_weights = array([model.get_weights()[layer] for model in members])
        avg_layer_weights = average(layer_weights, axis=0, weights=weights)
        avg_model_weights.append(avg_layer_weights)
    model = clone_model(members[0])
    model.set_weights(avg_model_weights)
    return model

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, required=True)
    parser.add_argument("--savefile", type=str, required=True)
    args = parser.parse_args()

    dirname = os.listdir(args.dir)
    all_models = list()
    models = list()

    for file in dirname:
        filename = os.path.join(args.dir, file)
        ext = os.path.splitext(filename)[-1].strip()
        if ext == '.h5':
            models.append(filename)
            model = load_model(filename)
            all_models.append(model)
            print('>loaded %s' % filename)

    members = all_models
    print('Loaded %d models' % len(members))
    n_models = len(members)
    weights = [1/n_models for i in range(1, n_models+1)]
    model.summary()
    model = model_weight_ensemble(members, weights)
