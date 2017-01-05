
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
        self.layer_size = layer_size

        self.RBMs = {}

        self.train_set = None

        self.main_dir = main_dir
        self.model_name = model_name
        self.model_dir, self.data_dir, self.summary_dir = self._create_data_directories()
        self.model_path = self.model_dir + self.model_name

        self.w = {}
        self.bh = {}

        self.input_data = None
        self.y = None

        self.train_step = None
        self.accuracy = None
        self.output = None

        self.gibbs_sampling_steps = None
        self.learning_rate = 0.01

        self.tf_session = None
        self.tf_saver = None
        self.tf_finetune_saver = None
        self.tf_merged_summaries = None
        self.tf_summary_writer = None

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

        self.train_set = train_set

        for i in range(len(self.layer_size) - 2):

            input_to_binary = False
            if i == 0 and first_layer_binary:
                input_to_binary = True

            rbm = RBM(self.layer_size[i], self.layer_size[i + 1], main_dir=self.main_dir + "/rbm_" + repr(i),
                      model_name="rbm_model_" + repr(i), input_to_binary=input_to_binary)

            start_epoch = 0

            for n in range(len(epoch_steps)):

                if n != 0:
                    start_epoch += epoch_steps[n - 1]

                print("[INFO] started training periode ", n + 1, " of ", len(epoch_steps))

                rbm.fit(self.train_set, restore_previous_model=continue_training[n], start_epoche=start_epoch,
                        validation_set=None, learning_rate=learning_rate[n],
                        momentum_factor=momentum[n], epochs=epoch_steps[n], weight_decay_factor=weight_decay[n],
                        gibbs_sampling_steps=gibbs_sampling_steps[n], batch_size=batch_size[n])

            print("[INFO] pretraining %d ended", i)
            results = rbm.classify(self.train_set, input_to_binary=None, return_hstates=layer_output_binary)

            print(results.shape[0], results.shape[1])

            self.train_set = DataSet(results, results)
            print("[INFO] new dataset generated")

    def supervised_finetuning(self, data_set, make_dbn=False, batch_size=1, epochs=1, validation_set=None):

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

        with tf.Session() as self.tf_session:
            self._initialize_tf_utilities_and_ops()

            for i in range(epochs):
                self._run_train_step(data_set, batch_size)

                if validation_set:
                    self._run_validation_results(validation_set, i)

            self.tf_finetune_saver.save(self.tf_session, self.model_dir + "dbn/" + self.model_name)

        tf.reset_default_graph()

    def classify(self, input, build_dbn=False):

        '''
        This function is used to get predictions for a given input. The network has to be build and should be trained.

        :param input: The data used to make the prediction.
        :param build_dbn: If the prediction has to be made before the finetuning the network can be build from
                            pretrained RBMs.
        :return: The prediction
        '''
        if build_dbn:
            self._build_dbn_from_rbms()

        self._build_deterministic_model()

        with tf.Session() as self.tf_session:
            self.tf_session.run(tf.global_variables_initializer())
            self.tf_saver = tf.train.Saver()
            self.tf_saver.restore(self.tf_session, self.model_dir + "dbn/" + self.model_name)

            output = self.tf_session.run(self.output, feed_dict={self.input_data: input})

        tf.reset_default_graph()

        return output

    def _initialize_tf_utilities_and_ops(self):
        '''
        Helper function which initializes all tensorflow variables.

        :return: self
        '''
        self.tf_session.run(tf.global_variables_initializer())
        self.tf_merged_summaries = tf.summary.merge_all()
        self.tf_saver = tf.train.Saver(self._create_save_dict())
        self.tf_finetune_saver = tf.train.Saver()
        self.tf_saver.restore(self.tf_session, self.model_path)
        self.tf_summary_writer = tf.train.SummaryWriter(self.summary_dir, self.tf_session.graph)

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

            self.tf_session.run(self.train_step, feed_dict={self.input_data: x, self.y: y})

    def _run_validation_results(self, validation_set, epoch):

        '''
        This function is called every epoch to calculate the accuracy.

        :param validation_set: The data set to validate formatted as input_format
        :param epoch: Am integer to pin the result to an epoch
        :return: self
        '''
        sum, accuracy = self.tf_session.run([self.tf_merged_summaries, self.accuracy],
                                            feed_dict={self.input_data: validation_set.images,
                                                       self.y: validation_set.labels})

        self.tf_summary_writer.add_summary(sum, epoch)

    def _create_save_dict(self):
        '''
        Helper function to dynamically get all names and tensorflow variables in one dictionary. This is used to load
                only these pretrained variables.

        :return: dict with the variable names as keys and the variables as values
        '''

        dict = {}

        for i in range(len(self.layer_size) - 2):
            dict[self.w[i].name.split(':0')[0]] = self.w[i]
            dict[self.bh[i].name.split(':0')[0]] = self.bh[i]

        return dict

    def _build_dbn_from_rbms(self):

        '''
        This function takes all pretrained layers weights and temporarily saves them as numpy arrays.
                With the values the tensorflow variables are initialized.

        :return: self
        '''

        if not self.RBMs:
            print("[INFO] recreate rbm models")
            for i in range(len(self.layer_size) - 2):

                self.RBMs[i] = RBM(self.layer_size[i], self.layer_size[i + 1], main_dir="dbn/rbm_" + repr(i),
                                   model_name="rbm_model_" + repr(i), input_to_binary=False)

        for i in range(len(self.layer_size) - 2):
            print("[INFO] get weights from network ", i)
            temp_w, temp_bh = self.RBMs[i].get_weights()
            self.w[i] = temp_w
            self.bh[i] = temp_bh

        for i in range(len(self.layer_size) - 2):
            self.w[i] = tf.Variable(self.w[i], name="dbn_weight_" + repr(i))
            self.bh[i] = tf.Variable(self.bh[i], name="dbn_bias_hidden_" + repr(i))

        with tf.Session() as self.tf_session:
            self.tf_session.run(tf.global_variables_initializer())
            self.tf_saver = tf.train.Saver()
            self.tf_saver.save(self.tf_session, self.model_path)

        tf.reset_default_graph()

    def _build_deterministic_model(self):

        '''
        THis function builds the computation graph for the supervised finetuning and the classification function.

        :return: self
        '''
        self._create_variables()
        self._create_placeholder()

        output = self.input_data

        for i in range(len(self.layer_size) - 2):
            output = tf.nn.sigmoid(tf.matmul(output, self.w[i]) + self.bh[i])

        output = tf.matmul(output, self.w[len(self.layer_size) - 2]) + self.bh[len(self.layer_size) - 2]
        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(output, self.y))

        self.train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

        correct_prediction = tf.equal(tf.argmax(output, 1), tf.argmax(self.y, 1))
        self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        tf.summary.scalar("accuracy", self.accuracy)

    def _create_variables(self):

        '''
        A Helper function which creates the weights and bias variables.

        :return: self
        '''
        for i in range(len(self.layer_size) - 1):
            self.w[i] = tf.Variable(tf.random_normal((self.layer_size[i], self.layer_size[i + 1]), mean=0.0,
                                                     stddev=0.1), name="dbn_weight_" + repr(i))
            self.bh[i] = tf.Variable(tf.zeros([self.layer_size[i + 1]]), name="dbn_bias_hidden_" + repr(i))

    def _create_placeholder(self):
        '''
        A Helper function wich creates the placesholders for the inputdata and the desired output.

        :return:
        '''
        self.input_data = tf.placeholder(tf.float32, [None, self.layer_size[0]], name="input-data")
        self.y = tf.placeholder(tf.float32, [None, self.layer_size[-1]], name="desired-output")

    def _create_data_directories(self):

        '''
        A Helper function to create the directories to save the logs and the model weights.

        :return: Returns the path to the logs and model directories
        '''
        self.main_dir = self.main_dir + '/' if self.main_dir[-1] != '/' else self.main_dir

        models_dir = "models/" + self.main_dir
        data_dir = "data/" + self.main_dir
        summary_dir = "logs/" + self.main_dir

        for d in [models_dir, data_dir, summary_dir]:
            if not os.path.isdir(d):
                os.makedirs(d)

        return models_dir, data_dir, summary_dir

'''
if __name__ == '__main__':
    dbm = DBN([784, 500, 500, 2000, 10])

    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

    # dbm.train_set = mnist.train

    dbm.pretraining(mnist.train, gibbs_sampling_steps=[1, 3, 5], learning_rate=[0.1, 0.01, 0.005],
                    weight_decay=[0.0001, 0.0001, 0.0001],
                    momentum=[0.5, 0.9, 0.9], continue_training=[False, True, True], epoch_steps=[100, 100, 100],
                    batch_size=[10, 100, 100])


    dbm.supervised_finetuning(batch_size=100, data_set=mnist.test, epochs=1, make_dbn=True, validation_set=mnist.validation)

'''
