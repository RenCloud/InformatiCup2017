import tensorflow as tf
import numpy as np

import os

from learning.networks.RBM_CDK import RBM

from tensorflow.examples.tutorials.mnist import input_data
from learning.utils.input_format import DataSet

# TODO
'''
 1. neuer ordner zum speichern und laden von finegetuneten models
 2. die möglichkeit das finetuning fortzusetzen
 3. für das finetunig die variable global step einführen
 4. refracturing des codes
'''


class DBN(object):
    def __init__(self,
                 layer_size,
                 main_dir="dbn",
                 model_name="dbn_model"
                 ):

        '''
            Constructor for Deep Belief Network. Sets up all Variables used by the network. In the Constructor is also
            the size of the network specified.

        :param layer_size: The parameter holds the size and the number of layers used for the network as a list:
                                e.g.[10, 20, 10], this network has 3 layers of the size 10, 20, 10.
        :param main_dir: Is used as save location for checkpoints and logdata.
        :param model_name: Is used for the checkpoint filename.
        '''

        self._layer_size = layer_size

        self._main_dir = main_dir
        self._model_name = model_name
        self._model_dir, self._data_dir, self._summary_dir = self._create_data_directories()
        self._model_path = self._model_dir + self._model_name

        self._tf_w = {}
        self._tf_bh = {}

        self._tf_global_step = None

        self._tf_input_data = None
        self._tf_desired_output = None
        self._tf_keep_prob = None

        self._tf_train_step = None
        self._tf_accuracy = None
        self._tf_output = None

        self._gibbs_sampling_steps = None
        self.learningrate = 0.1

        self._tf_session = None
        self._tf_saver = None
        self._tf_finetune_saver = None
        self._tf_merged_summaries = None
        self._tf_summary_writer = None

    def pretraining(self,
                    train_set,
                    gibbs_sampling_steps=[1],
                    learning_rate=[0.1],
                    weight_decay=[0.0001],
                    momentum=[0.9],
                    epoch_steps=[500],
                    first_layer_binary=True,
                    layer_output_binary=False,
                    continue_training=[False],
                    batch_size=[10]):

        '''
        The pretrainfunction is used to find good initial weights for the finetuning part. The arguments of the function
                contain lists which all have to have the same size to specify the training parameters.
                All layers but the top one specified in the constructor are then train with the rbm.fit() function.
                All networkparameters have default values but the should be overriden.

        :param train_set: The input data formatted as input_format.
        :param gibbs_sampling_steps: The number of Gibbs sampling steps.
        :param learning_rate: The learningrate.
        :param weight_decay: The weight decay term to punish high weight values.
        :param momentum: The momentum term to speed up or slow down learning.
        :param epoch_steps: The number of epochs that should be performed for the hyperparameters at the time .
        :param first_layer_binary: When set true the first RBM will convert the input into a dta vector with values
                                between 0 and 1.
        :param layer_output_binary: When set true all networks will return a data vector with values between 0 and 1.
        :param continue_training: Is a list with the same size as epoch_steps. If at a given index set to true the
                                RBM will restore the previously learned weights and continues training with them.
        :param batch_size:  Is a list with the same size as epoch_steps. The value at an index of the list is the size
                                of the batches.
        :return: self
        '''

        for i in range(len(self._layer_size) - 2):

            input_to_binary = False
            if i == 0 and first_layer_binary:
                input_to_binary = True

            rbm = RBM(self._layer_size[i], self._layer_size[i + 1], main_dir=self._main_dir + "/rbm_" + repr(i),
                      model_name="rbm_model_" + repr(i), input_to_binary=input_to_binary)

            # print(train_set._images.shape[0], train_set._images.shape[1])
            start_epoch = 0

            for n in range(len(epoch_steps)):

                if n != 0:
                    start_epoch += epoch_steps[n - 1]

                print("[INFO] started training periode ", n + 1, " of ", len(epoch_steps))

                rbm.fit(train_set, restore_previous_model=continue_training[n], start_epoche=start_epoch,
                        validation_set=None, learning_rate=learning_rate[n],
                        momentum_factor=momentum[n], epochs=epoch_steps[n], weight_decay_factor=weight_decay[i],
                        gibbs_sampling_steps=gibbs_sampling_steps[n], batch_size=batch_size[n])

            print("[INFO] pretraining %d ended", i)
            results = rbm.classify(train_set, input_to_binary=None, return_hstates=layer_output_binary)

            print(results.shape[0], results.shape[1])

            train_set = DataSet(results, results)
            print("[INFO] new dataset generated")

    def supervised_finetuning(self, data_set, make_dbn=False, batch_size=1, epochs=1, validation_set=None,
                              global_epoch=0, finetune_load_dir="dbn/", finetune_save_dir="dbn/"):

        '''
        The finetuning function uses a data_set to train a pretrained network. It uses the backpropagation algorithm.
                Before the training can start the DBN has to be build. Build_dbn_from_rbms combines the weights of the
                pretrained RBMs and creates the DBN weights with it. The DBN has one more softmax layer

        :param data_set: The data to train the network with. This dataset has to have the desired output.
        :param make_dbn: A boolean variable. If true the dbn will be build from the pretrained RBMs
        :param batch_size: Specifies the size of batches the data_set is slices into.
        :param epochs: Number of epochs the network should train.
        :param validation_set: If a validation_set is given the network will calculate it's accuracy after every epoch.
        :return: self
        '''

        if make_dbn:
            self._build_dbn_from_rbms()

        self._build_deterministic_model()

        self._create_finetune_dir(finetune_save_dir)

        accuracy = 0

        with tf.Session() as self._tf_session:
            self._initialize_tf_utilities_and_ops(create_from_rbms=make_dbn, finetune_load_dir=finetune_load_dir,
                                                  finetune_save_dir=finetune_save_dir)

            for i in range(epochs):
                self._run_train_step(data_set, batch_size)

                if validation_set:
                    accuracy = self._run_validation_results(validation_set, i + global_epoch)

            self._tf_finetune_saver.save(self._tf_session, self._model_dir + finetune_save_dir + self._model_name)

        tf.reset_default_graph()

        return accuracy

    def classify(self, input, build_dbn=False, finetune_sub_dir="dbn/"):

        '''
        This function is used to get predictions for a given input. The network has to be build and should be trained.

        :param input: The data used to make the prediction.
        :param build_dbn: If the prediction has to be made before the finetuning the network can be build from
                            pretrained RBMs.
        :return: The prediction
        '''

        if build_dbn:
            self._build_dbn_from_rbms()

        self._classification_model()

        with tf.Session() as self._tf_session:
            self._tf_session.run(tf.global_variables_initializer())
            self._tf_saver = tf.train.Saver()
            self._tf_saver.restore(self._tf_session, self._model_dir + finetune_sub_dir + self._model_name)

            output = self._tf_session.run(self._tf_output, feed_dict={self._tf_input_data: input})

        tf.reset_default_graph()

        return output

    def supervised_training(self, train_set, validation_set, epochs=1, batch_size=1,
                            sub_dir="dbn/", global_epoch=0, restore_previouse_model=True):
        self._build_deterministic_model()

        accuracy = 0

        with tf.Session() as self._tf_session:
            self._initialize_tf_utilities_and_ops(create_from_rbms=False, finetune_load_dir=sub_dir,
                                                  finetune_save_dir=sub_dir,
                                                  restore_previouse_model=restore_previouse_model)

            for i in range(epochs):
                self._run_train_step(train_set, batch_size)

                if validation_set:
                    accuracy = self._run_validation_results(validation_set, i + global_epoch)

            self._tf_finetune_saver.save(self._tf_session, self._model_dir + sub_dir + self._model_name)

        tf.reset_default_graph()

        return accuracy

    def _initialize_tf_utilities_and_ops(self, create_from_rbms=False, restore_previouse_model=True, finetune_load_dir="dbn/",
                                         finetune_save_dir="dbn/"):

        '''
        Helper function which initializes all tensorflow variables.
                If the network is first created from multiple RBMs only the tf_saver is used to restore only the
                pretrained variables. Otherwise an error will occure. If the network was already build the weights
                will be load completely and from a different directory.

        :return: self
        '''

        self._tf_session.run(tf.global_variables_initializer())
        self._tf_merged_summaries = tf.summary.merge_all()

        self._tf_saver = tf.train.Saver(self._create_restore_dict())
        self._tf_finetune_saver = tf.train.Saver()

        if not create_from_rbms and restore_previouse_model:
            self._tf_finetune_saver.restore(self._tf_session, self._model_dir + finetune_load_dir + self._model_name)
        else:
            self._tf_saver.restore(self._tf_session, self._model_dir + "dbn/" + self._model_name)

        self._tf_summary_writer = tf.summary.FileWriter(self._summary_dir + finetune_save_dir, self._tf_session.graph)

    def _run_train_step(self, data_set, batch_size):

        '''
        Helper function to run the training for one epoch

        :param data_set: The data_set formatted as input_format
        :param batch_size: The size for the batches
        :return: self
        '''

        iterations = (int)(data_set.num_examples / batch_size)

        for i in range(iterations):
            x, y = data_set.next_batch(batch_size)

            self._tf_session.run(self._tf_train_step, feed_dict={self._tf_input_data: x, self._tf_desired_output: y,
                                                                 self._tf_keep_prob: 0.5})

    def _run_validation_results(self, validation_set, epoch):

        '''
        This function is called every epoch to calculate the accuracy.

        :param validation_set: The data set to validate formatted as input_format
        :param epoch: Am integer to pin the result to an epoch
        :return: self
        '''

        sum, accuracy = self._tf_session.run([self._tf_merged_summaries, self._tf_accuracy],
                                             feed_dict={self._tf_input_data: validation_set.images,
                                                        self._tf_desired_output: validation_set.labels,
                                                        self._tf_keep_prob: 1})

        self._tf_summary_writer.add_summary(sum, epoch)

        return accuracy

    def _create_restore_dict(self):
        '''
        Helper function to dynamically get all names and tensorflow variables in one dictionary. This is used to load
                only these pretrained variables.

        :return: dict with the variable names as keys and the variables as values
        '''

        dict = {}

        for i in range(len(self._layer_size) - 2):
            dict[self._tf_w[i].name.split(':0')[0]] = self._tf_w[i]
            dict[self._tf_bh[i].name.split(':0')[0]] = self._tf_bh[i]

        return dict

    def _build_dbn_from_rbms(self):

        '''
        This function takes all pretrained layers weights and temporarily saves them as numpy arrays.
                With the values the tensorflow variables are initialized.

        :return: self
        '''

        rbms = {}

        if not rbms:
            print("[INFO] recreate rbm models")
            for i in range(len(self._layer_size) - 2):
                rbms[i] = RBM(self._layer_size[i], self._layer_size[i + 1], main_dir=self._main_dir + "/rbm_" + repr(i),
                              model_name="rbm_model_" + repr(i), input_to_binary=False)

        for i in range(len(self._layer_size) - 2):
            print("[INFO] get weights from network ", i)
            temp_w, temp_bh = rbms[i].get_weights()
            self._tf_w[i] = temp_w
            self._tf_bh[i] = temp_bh

        for i in range(len(self._layer_size) - 2):
            self._tf_w[i] = tf.Variable(self._tf_w[i], name="dbn_weight_" + repr(i))
            self._tf_bh[i] = tf.Variable(self._tf_bh[i], name="dbn_bias_hidden_" + repr(i))

        with tf.Session() as self._tf_session:
            self._tf_session.run(tf.global_variables_initializer())
            self._tf_saver = tf.train.Saver()
            self._tf_saver.save(self._tf_session, self._model_dir + "dbn/" + self._model_name)

        tf.reset_default_graph()

    def _build_deterministic_model(self):

        '''
        This function builds the computation graph for the supervised finetuning and the classification function.

        :return: self
        '''

        self._create_variables()
        self._create_placeholder()

        with tf.name_scope("learning"):

            output = self._tf_input_data

            with tf.name_scope("forward-pass"):

                for i in range(len(self._layer_size) - 2):
                    # dropout to prevent overfitting
                    output = tf.nn.dropout(output, keep_prob=self._tf_keep_prob)

                    output = tf.nn.relu(tf.matmul(output, self._tf_w[i]) + self._tf_bh[i])

                self._tf_output = tf.matmul(output, self._tf_w[len(self._layer_size) - 2]) + self._tf_bh[len(self._layer_size) - 2]

                # dropout to prevent overfitting
                self._tf_output = tf.nn.dropout(self._tf_output, keep_prob=self._tf_keep_prob)

            with tf.name_scope("backpropagation"):

                cross_entropy = tf.nn.softmax_cross_entropy_with_logits(self._tf_output, self._tf_desired_output)

                self.learningrate = 0.5
                learning_rate = tf.train.exponential_decay(self.learningrate, self._tf_global_step, 100, 0.99,
                                                           staircase=True)

                self._tf_train_step = tf.train.ProximalAdagradOptimizer(learning_rate=learning_rate,
                                                                        l1_regularization_strength=0.0001,
                                                                        l2_regularization_strength=0.001).\
                    minimize(cross_entropy, global_step=self._tf_global_step)

        with tf.name_scope("accuracy"):
            prediction = tf.nn.softmax(self._tf_output)
            correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(self._tf_desired_output, 1))

            # correct_prediction = tf.nn.in_top_k(prediction, tf.argmax(self._tf_desired_output, 1), 2)

            self._tf_accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        with tf.name_scope("weight_development"):
            for i in range(len(self._layer_size) - 1):
                tf.summary.scalar("weights_max_" + repr(i), tf.reduce_max(self._tf_w[i]))
                tf.summary.scalar("weights_min_" + repr(i), tf.reduce_min(self._tf_w[ i]))
        tf.summary.scalar("accuracy", self._tf_accuracy)
        tf.summary.scalar("loss", tf.reduce_mean(cross_entropy))
        tf.summary.scalar("effective_learningrate", learning_rate)

    def _classification_model(self):

        self._create_variables()
        self._create_placeholder()

        output = self._tf_input_data

        for i in range(len(self._layer_size) - 1):
            output = tf.nn.relu(tf.matmul(output, self._tf_w[i]) + self._tf_bh[i])

        self._tf_output = tf.nn.softmax(output)

    def _create_variables(self):

        '''
        A Helper function which creates the weights and bias variables.

        :return: self
        '''

        self._tf_global_step = tf.Variable(0, dtype=tf.int64, name='global_step', trainable=False)

        for i in range(len(self._layer_size) - 1):
            self._tf_w[i] = tf.Variable(tf.random_normal((self._layer_size[i], self._layer_size[i + 1]), mean=0.0,
                                                         stddev=0.1), name="dbn_weight_" + repr(i))
            self._tf_bh[i] = tf.Variable(tf.zeros([self._layer_size[i + 1]]), name="dbn_bias_hidden_" + repr(i))

    def _create_placeholder(self):

        '''
        A Helper function wich creates the placesholders for the inputdata and the desired output.

        :return:
        '''

        self._tf_input_data = tf.placeholder(tf.float32, [None, self._layer_size[0]], name="input-data")
        self._tf_desired_output = tf.placeholder(tf.float32, [None, self._layer_size[-1]], name="desired-output")
        self._tf_keep_prob = tf.placeholder(tf.float32)

    def _create_data_directories(self):

        '''
        A Helper function to create the directories to save the logs and the model weights.

        :return: Returns the path to the logs and model directories
        '''

        self._main_dir = self._main_dir + '/' if self._main_dir[-1] != '/' else self._main_dir

        models_dir = "models/" + self._main_dir
        data_dir = "data/" + self._main_dir
        summary_dir = "logs/" + self._main_dir

        for d in [models_dir, data_dir, summary_dir]:
            if not os.path.isdir(d):
                os.makedirs(d)

        if not os.path.isdir(models_dir + "dbn/"):
            os.makedirs(models_dir + "dbn/")

        return models_dir, data_dir, summary_dir

    def _create_finetune_dir(self, finetune_dir):
        if not os.path.isdir("models/" + self._main_dir + finetune_dir):
            os.makedirs("models/" + self._main_dir + finetune_dir)

        if not os.path.isdir("logs/" + self._main_dir + finetune_dir):
            os.makedirs("logs/" + self._main_dir + finetune_dir)


if __name__ == '__main__':
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

    dbn = DBN([784, 500, 500, 1500, 10], main_dir="mnist_test")

    dbn.pretraining(mnist, gibbs_sampling_steps=[1, 3, 5], learning_rate=[0.1, 0.01, 0.005],
                    weight_decay=[0.0001, 0.0001, 0.0002],
                    momentum=[0.5, 0.9, 0.9], continue_training=[False, True, True], epoch_steps=[10, 10, 10],
                    batch_size=[10, 10, 10])
