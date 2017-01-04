from networks.RBM_CDK import RBM
import json
import numpy as np
from utils.input_format import DataSet


def fit_rbm(data_set, main_dir="rbm_test"):

    input_list = json.loads(data_set)

    input_np = np.asarray(input_list)

    input = DataSet(input_np, input_np)

    # TODO
    # größe anpassen

    rbm = RBM(input.input_dim, 7, main_dir=main_dir, input_to_binary=True, verbose=False)

    rbm.fit(input, validation_set=None, restore_previous_model=False, start_epoche=0, gibbs_sampling_steps=1,
            learning_rate=0.1, weight_decay_factor=0.001, momentum_factor=0.5, epochs=50, batch_size=10)

    rbm.fit(input, validation_set=None, restore_previous_model=True, start_epoche=50, gibbs_sampling_steps=3,
            learning_rate=0.05, weight_decay_factor=0.001, momentum_factor=0.9, epochs=300, batch_size=100)

    rbm.fit(input, validation_set=None, restore_previous_model=True, start_epoche=350, gibbs_sampling_steps=5,
            learning_rate=0.01, weight_decay_factor=0.001, momentum_factor=0.9, epochs=300, batch_size=100)

    rbm.fit(input, validation_set=None, restore_previous_model=True, start_epoche=650, gibbs_sampling_steps=10,
            learning_rate=0.001, weight_decay_factor=0.001, momentum_factor=0.9, epochs=300, batch_size=100)

    rbm.fit(input, validation_set=None, restore_previous_model=True, start_epoche=950, gibbs_sampling_steps=20,
            learning_rate=0.0001, weight_decay_factor=0.001, momentum_factor=0.9, epochs=600, batch_size=100)


def classify(input):
    rbm = RBM(784, 10, main_dir="rbm_server", input_to_binary=True, verbose=False)

    rbm.classify(input, return_hstates=False, input_to_binary=False)
