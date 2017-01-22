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

    rbm.fit(input, restore_previous_model=False, start_epoche=0, gibbs_sampling_steps=1,
            learning_rate=0.1, weight_decay_factor=0.001, momentum_factor=0.5, epochs=50, batch_size=10)

    rbm.fit(input, restore_previous_model=True, start_epoche=50, gibbs_sampling_steps=3,
            learning_rate=0.05, weight_decay_factor=0.001, momentum_factor=0.9, epochs=300, batch_size=100)

    rbm.fit(input, restore_previous_model=True, start_epoche=350, gibbs_sampling_steps=5,
            learning_rate=0.01, weight_decay_factor=0.001, momentum_factor=0.9, epochs=300, batch_size=100)

    rbm.fit(input, restore_previous_model=True, start_epoche=650, gibbs_sampling_steps=10,
            learning_rate=0.001, weight_decay_factor=0.001, momentum_factor=0.9, epochs=300, batch_size=100)

    rbm.fit(input, restore_previous_model=True, start_epoche=950, gibbs_sampling_steps=20,
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


def fit_dbn(data_set, main_dir="dbn/", dir="sub_dir/",supervised_train_set=None, validation_set=None, do_pretraining=True):

    '''
    Wrapper function we used to call from our server module. The function gives easy access to the learning ability of
            network. But the details of the training are already configured and hidden from the server. The server just
            provides the data_set, supervised_train_set and validation_set as json string.
            Depending on which of the 3 sets are provided the training is performed differently.
            If only a data_set is provided then the function will only perform pretraining.
    :param data_set: The training data to perform the pretraining. Has to be a JSON string with lists int a list.
    :param main_dir: The directory, where the network is saved and loaded from.
    :param dir: The newly trained network is saved into this subdirectory. The directory has to end with a slash. But
                    doesn't have to exist. It will be created automatically.
    :param supervised_train_set: A json string with two lists for the input data and the desired output.
    :param validation_set: A json string with two lists consisting of input data and desired output to validate the
                    training progress.
    :param do_pretraining: This boolean value indicates if a pretraining should be performed before the finetuning.
            Finetuning can only be performed if enough pretrained RBM's already exists in the specified main_dir. Then the
            network uses these to build the model.
    :return:

    '''

    output = _load_and_normalize(data_set)
    input = DataSet(output, output)

    # here you can change the size of the network. But keep in mind to load a already trained network the
    # loading network has to have the same layer sizes and number of layers as the saved ones
    dbn = DBN([input.input_dim, 50, 100, 200, 400, 7], main_dir=main_dir)

    print("[INFO] Dataset input size ", input.input_dim, " num examples: ", input.num_examples)

    if do_pretraining:
        dbn.pretraining(input, gibbs_sampling_steps=[1, 1, 3, 4], learning_rate=[0.1, 0.01, 0.001, 0.0001],
                        weight_decay=[0.01, 0.01, 0.01, 0.01, 0.001],
                        momentum=[0.5, 0.9, 0.9, 0.9], continue_training=[False, True, True, True],
                        epoch_steps=[10, 50, 50, 100], batch_size=[10, 10, 10, 10])

    if supervised_train_set and validation_set:

        data_np = _load_and_normalize(supervised_train_set[0])
        labels_np = _load_and_normalize(supervised_train_set[1], False)

        train_set = DataSet(data_np, labels_np)

        vdata_np = _load_and_normalize(validation_set[0])
        vlabels_np = _load_and_normalize(validation_set[1], False)

        validation_set = DataSet(vdata_np, vlabels_np)

        # the learning rate for the finetuning has to be changed in the DBN class
        dbn.supervised_finetuning(batch_size=1, data_set=train_set, epochs=1, make_dbn=True,
                                  validation_set=validation_set, finetune_save_dir=dir,
                                  finetune_load_dir=dir)

        print("[INFO] First supervised training ended succefully")

        for i in range(300):
            accuracy = dbn.supervised_finetuning(batch_size=1, data_set=train_set, epochs=1, make_dbn=False,
                                                 validation_set=validation_set, global_epoch=i,
                                                 finetune_load_dir=dir,
                                                 finetune_save_dir=dir)

            print("[INFO] accuracy ", accuracy)

            # if you uncomment these the network will classify unlabeled data
            # and appends it to the supervised:training_set

            # examples = input.next_batch(100 + 50 * i)

            # prediction = dbn.classify(examples[0], finetune_sub_dir=dir)

            # train_set.append(examples[0], prediction)

        print("[Info] supervised training set extended it's size to ", train_set.num_examples, " examples")


def classify_dbn(data_set, main_dir="dbn/", sub_dir="dbn/"):

    '''
        This function is used to load a previously trained model and returns a prediction for the given data_set.

    :param data_set: The data that you want to classify as a JSON string. The string has to be a list of lists.
    :param main_dir: A subdirectory of the models directory where the network is saved.
    :param sub_dir: The subdirectory in main_dir where the finetuned model is saved. The directory has to end with a slash.
    :return: Returns a prediction for the given dataset.
    '''

    input_np = _load_and_normalize(data_set)
    input = DataSet(input_np, input_np)

    # this network has to have the same layer size and number of layers then the trained one
    dbn = DBN([input.input_dim, 50, 100, 200, 400, 7], main_dir=main_dir)

    output = dbn.classify(input.images, build_dbn=False, finetune_sub_dir=sub_dir)

    return output


def _load_and_normalize(data, normalize=True):

    '''
        This is a helper function which takes the JSON string and converts it into a numpy array then it normalizes
        the vector and returns it. The disired into doesn't has to be normalized so the normalize flag should be set to False

    :param data: The data as JSON string.
    :param normalize: A boolean which tells the function if the given data should be normalized or not.
    :return:

    '''

    tf.reset_default_graph()

    input_list = json.loads(data)
    input_np = np.asarray(input_list)

    print("old")
    print(input_np[0])

    if normalize:
        with tf.Session() as sess:

            input_np = tf.cast(input_np, tf.float32)

            normalized = tf.nn.l2_normalize(input_np, 1)

            sess.run(tf.global_variables_initializer())
            output = sess.run(normalized)

        tf.reset_default_graph()
        return output

    else:
        return input_np


def supervised_fit_dbn(supervised_train_set, validation_set, main_dir="data_normalized/"):

    '''
        We created this function to wrap the supervised_training method. This function performs a supervised training
        without pretraining.

    :param supervised_train_set: The training set as JSON string. A list with two list in it. Each of these list as
                        multiple lists which represent the input and output vectors. Both input and ouput vector lists
                        should have the same size.
    :param validation_set: The validation set. Has the same constraints as supervised_train_set. This list is only used
                        to test the accuracy of the network.
    :param main_dir: The directory where the model and log data is saved.
    :return:

    '''

    dbn = DBN([6, 50, 100, 200, 400, 7], main_dir=main_dir)

    data_np = _load_and_normalize(supervised_train_set[0])
    labels_np = _load_and_normalize(supervised_train_set[1], False)

    train_set = DataSet(data_np, labels_np)

    vdata_np = _load_and_normalize(validation_set[0])
    vlabels_np = _load_and_normalize(validation_set[1], False)

    validation_set = DataSet(vdata_np, vlabels_np)

    dir = "supervised_training/"

    dbn.supervised_training(batch_size=1, train_set=train_set, epochs=1,
                            validation_set=validation_set, sub_dir=dir, restore_previouse_model=False)

    for i in range(100):
        accuracy = dbn.supervised_training(batch_size=1, train_set=train_set, epochs=1,
                                           validation_set=validation_set, global_epoch=i + 1, sub_dir=dir, restore_previouse_model=True)

        print("[INFO] accuracy ", accuracy)
        # examples = input.next_batch(100 + 50 * i)

        # prediction = dbn.classify(examples[0], finetune_sub_dir=dir)

        # train_set.append(examples[0], prediction)

    print("[Info] supervised training set extended it's size to ", train_set.num_examples, " examples")
