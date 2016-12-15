from networks.RBM_CDK import RBM
import json
import numpy as np
from utils.input_format import DataSet


def fit_rbm(data_set, main_dir="rbm_test"):

    input_list = json.loads(data_set)

    input_np = np.asarray(input_list)

    input = DataSet(input_np, input_np)

    rbm = RBM(784, 10, batch_size=100, epochs=300, main_dir=main_dir, gibbs_sampling_steps=1,
              learning_rate=0.1, input_to_binary=True, verbose=False)

    rbm.fit(input, validation_set=None, restore_previous_model=False, start_epoche=0)

    rbm.learning_rate = 0.05
    rbm.gibbs_sampling_steps = 3
    rbm.epochs = 300
    rbm.fit(input, validation_set=None, restore_previous_model=True, start_epoche=300)

    rbm.learning_rate = 0.01 / 100
    rbm.gibbs_sampling_steps = 5
    rbm.epochs = 300
    rbm.fit(input, validation_set=None, restore_previous_model=True, start_epoche=600)

    rbm.learning_rate = 0.001 / 100
    rbm.gibbs_sampling_steps = 10
    rbm.epochs = 300
    rbm.fit(input, validation_set=None, restore_previous_model=True, start_epoche=900)

    rbm.learning_rate = 0.0001 / 100
    rbm.gibbs_sampling_steps = 20
    rbm.epochs = 600
    rbm.fit(input, validation_set=None, restore_previous_model=True, start_epoche=1200)


def classify(input):
    rbm = RBM(784, 10, batch_size=100, epochs=300, main_dir="rbm_server", gibbs_sampling_steps=1,
              learning_rate=0.1, input_to_binary=True, verbose=False)

    rbm.classify(input, return_hstates=False, input_to_binary=False)