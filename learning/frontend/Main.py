from learning.networks.RBM_CDK import RBM
from learning.networks.DBN import DBN
import json
import numpy as np
from learning.utils.input_format import DataSet


def fit_rbm(data_set, main_dir="rbm_test"):

    '''
    This is an old fragment of a network learning algorithm. It demonstrates how a RBM is learning. This algorithm is
    unsupervised and only consists of two layers. The learned RBM's output is only a permutation of the right
    prediction. The shallow structure makes it also pretty unlikely that it makes the right predictions for the given
    data.

    :param data_set: A set of vectors with the data to learn.
    :param main_dir: The name for the network. This specifies where the logs and model data is saved. It is also used to
                    reload a halfway trained model. Only with the correct main_dir is this possible.
    :return: self
    '''

    input_list = json.loads(data_set)
    input_np = np.asarray(input_list)
    input = DataSet(input_np, input_np)

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


def classify_rbm(data_set, main_dir="rbm_test"):

    '''
    This function shows how a RBM can make a prediction for a given input

    :param data_set: The dataset to make the predictions.
    :param main_dir: This argument is used to load the right model.
    :return: The prediction the network made
    '''
    input_list = json.loads(data_set)
    input_np = np.asarray(input_list)
    input = DataSet(input_np, input_np)

    rbm = RBM(input.input_dim, 7, main_dir="main_dir", input_to_binary=True, verbose=False)

    output = rbm.classify(input, return_hstates=False, input_to_binary=False)

    return output


def fit_dbn(data_set, main_dir="dbn/", supervised_train_set=None, validation_set=None):

    '''


    :param data_set:
    :param main_dir:
    :param supervised_train_set:
    :param validation_set:
    :return:
    '''

    input_list = json.loads(data_set)
    input_np = np.asarray(input_list)
    input = DataSet(input_np, input_np)

    data = json.loads(supervised_train_set[0])
    labels = json.loads(supervised_train_set[1])
    data_np = np.asarray(data)
    labels_np = np.asarray(labels)
    train_set = DataSet(data_np, labels_np)

    vdata = json.loads(validation_set[0])
    vlabels = json.loads(validation_set[1])
    vdata_np = np.asarray(vdata)
    vlabels_np = np.asarray(vlabels)
    validation_set = DataSet(vdata_np, vlabels_np)

    dbn = DBN([input.input_dim, 500, 500, 1500, 7], main_dir=main_dir)

    dbn.pretraining(input, gibbs_sampling_steps=[1, 3, 5], learning_rate=[0.1, 0.01, 0.005],
                    weight_decay=[0.0001, 0.0001, 0.0001],
                    momentum=[0.5, 0.9, 0.9], continue_training=[False, True, True], epoch_steps=[100, 100, 100],
                    batch_size=[10, 100, 100])

    dbn.supervised_finetuning(batch_size=1, data_set=train_set, epochs=1, make_dbn=True,
                              validation_set=validation_set)

    for i in range(100):
        dbn.supervised_finetuning(batch_size=1, data_set=train_set, epochs=1, make_dbn=False,
                                  validation_set=validation_set)

        examples = train_set.next_batch(25 + i)

        prediction = dbn.classify(examples[0])

        train_set.append(examples[0], prediction)


def classify_dbn(data_set, main_dir="dbn/"):
    input_list = json.loads(data_set)
    input_np = np.asarray(input_list)
    input = DataSet(input_np, input_np)

    dbn = DBN([input.input_dim, 500, 500, 1500, 7], main_dir=main_dir)

    output = dbn.classify(input.images, build_dbn=False)

    return output
