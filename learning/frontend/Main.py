from learning.networks.RBM_CDK import RBM
from learning.networks.DBN import DBN
import json
import numpy as np
from learning.utils.input_format import DataSet

import tensorflow as tf


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


def fit_dbn(data_set, main_dir="dbn/", supervised_train_set=None, validation_set=None, do_pretraining=True):

    '''
    Wrapper function we used to call from our server module. The function gives easy access to the learning ability of
            network. But the details of the training are already configured and hidden from the server. The server just
            provides the data_set, supervised_train_set and validation_set as json string.
            Depending on which of the 3 sets are provided the training is performed differently.
            If only a data_set is provided then the function will only perform pretraining.
    :param data_set: The training data to perform the pretraining.
    :param main_dir: The directory, where the network is saved and loaded from.
    :param supervised_train_set: A json string with two lists for the input data and the desired output.
    :param validation_set: A json string with two lists consisting of input data and desired output to validate the
                    training progress.
    :return:
    '''

    output = _load_and_normalize(data_set)
    input = DataSet(output, output)

    dbn = DBN([input.input_dim, 50, 100, 200, 400, 7], main_dir=main_dir)

    print("[INFO] Dataset input size ", input.input_dim, " num examples: ", input.num_examples)

    if do_pretraining:
        dbn.pretraining(input, gibbs_sampling_steps=[1, 1, 3, 4], learning_rate=[0.1, 0.01, 0.001, 0.0001],
                        weight_decay=[0.1, 0.01, 0.01, 0.01, 0.001],
                        momentum=[0.5, 0.9, 0.9, 0.9], continue_training=[False, True, True, True],
                        epoch_steps=[10, 50, 10, 10], batch_size=[10, 10, 10, 10])

    if supervised_train_set and validation_set:

        data_np = _load_and_normalize(supervised_train_set[0])
        labels_np = _load_and_normalize(supervised_train_set[1], False)

        train_set = DataSet(data_np, labels_np)

        vdata_np = _load_and_normalize(validation_set[0])
        vlabels_np = _load_and_normalize(validation_set[1], False)

        validation_set = DataSet(vdata_np, vlabels_np)

        dir = "Decent_high_lr_functioning/"

        dbn.supervised_finetuning(batch_size=1, data_set=train_set, epochs=1, make_dbn=True,
                                  validation_set=validation_set, finetune_save_dir=dir,
                                  finetune_load_dir=dir)
        print("[INFO] First pretraining ended succefully")

        accuracy = 0
        old_a = 0
        counter = 0

        for i in range(300):
            accuracy = dbn.supervised_finetuning(batch_size=1, data_set=train_set, epochs=1, make_dbn=False,
                                                 validation_set=validation_set, global_epoch=i + 1,
                                                 finetune_load_dir=dir,
                                                 finetune_save_dir=dir)

            print("[INFO] accuracy ", accuracy)
            # examples = input.next_batch(100 + 50 * i)

            # prediction = dbn.classify(examples[0], finetune_sub_dir=dir)

            # train_set.append(examples[0], prediction)

            # free the unused memory
            examples = None
            prediction = None

        print("[Info] supervised training set extended it's size to ", train_set.num_examples, " examples")


def classify_dbn(data_set, main_dir="dbn/", sub_dir="dbn/"):
    input_list = json.loads(data_set)
    input_np = np.asarray(input_list)
    input = DataSet(input_np, input_np)

    dbn = DBN([input.input_dim, 50, 100, 200, 400, 7], main_dir=main_dir)

    output = dbn.classify(input.images, build_dbn=False, finetune_sub_dir=sub_dir)

    return output


def _load_and_normalize(data, load=True):
    tf.reset_default_graph()

    input_list = json.loads(data)
    input_np = np.asarray(input_list)

    print("old")
    print(input_np[0])
    print(input_np[1])

    if load:
        with tf.Session() as sess:

            batch_size = input_np.shape[1]

            input_np = tf.cast(input_np, tf.float32)
            '''
            normalized = tf.nn.l2_normalize(input_np, 0)
            '''

            batch_mean2, batch_var2 = tf.nn.moments(input_np, [0])
            scale2 = tf.Variable(tf.ones([batch_size]))
            beta2 = tf.Variable(tf.zeros([batch_size]))
            normalized = tf.nn.batch_normalization(input_np, batch_mean2, batch_var2, beta2, scale2, 1e-3)

            sess.run(tf.global_variables_initializer())
            output = sess.run(normalized)

            print("new")
            print(output[0])
            print(output[1])
            print(output.shape[0], " ", output.shape[1])

        tf.reset_default_graph()
        return output


    else:
        return input_np


def supervised_fit_dbn(supervised_train_set, validation_set, main_dir="data_normalized/"):

    dbn = DBN([6, 50, 100, 200, 400, 7], main_dir=main_dir)

    data_np = _load_and_normalize(supervised_train_set[0])
    labels_np = _load_and_normalize(supervised_train_set[1], False)

    train_set = DataSet(data_np, labels_np)

    vdata_np = _load_and_normalize(validation_set[0])
    vlabels_np = _load_and_normalize(validation_set[1], False)

    validation_set = DataSet(vdata_np, vlabels_np)

    dir = "Decent_high_lr_functioning/"

    dbn.supervised_training(batch_size=1, train_set=train_set, epochs=1,
                            validation_set=validation_set, sub_dir=dir)
    print("[INFO] First pretraining ended succefully")

    accuracy = 0
    old_a = 0
    counter = 0

    for i in range(100):
        accuracy = dbn.supervised_training(batch_size=1, train_set=train_set, epochs=1,
                                           validation_set=validation_set, global_epoch=i + 1, sub_dir=dir)

        print("[INFO] accuracy ", accuracy)
        # examples = input.next_batch(100 + 50 * i)

        # prediction = dbn.classify(examples[0], finetune_sub_dir=dir)

        # train_set.append(examples[0], prediction)

        # free the unused memory
        examples = None
        prediction = None

    print("[Info] supervised training set extended it's size to ", train_set.num_examples, " examples")
