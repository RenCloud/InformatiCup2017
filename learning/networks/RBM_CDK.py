import tensorflow as tf
import numpy as np

import os

from tensorflow.examples.tutorials.mnist import input_data
from learning.utils.input_format import DataSet

# TODO
'''
10. Runtime profiling
12. Weight decay L2
13. Variable zum speichern der epochen die bereits abgelaufen sind
14. Learning rate auch außerhalb der Klasse setzen
15. Mehrere Checkpoints erstellen damit man die gewichte von unterschiedlichen zeiten wiederherstellen kann
16. Erkennung für overtraining mit validation set einführen
17. die run_test funktion und den test mit validationset trennen für bessere verwendbarkeit
18. Eine allgemeine Form für die übergabe der Trainingsdaten einbauen damit es für das Porjekt ohne Probleme funktioniert

19. eine property function für das setzen von weight decay und learning rate, da die noch durch durch batch_size geteilt werden müssen
'''

'''
############# Documentation #################
    #Python code for a restricted boltzmann machine (RBM). The neural network is learning unsupervised.

    #Userinteraction: Initialise the class
        As a user you can instantiate a RBM class with the arguments input and hidden size. The parameters are mandatory.
        The inputsize is determind by the number of features your vector has. For an image it's the number of pixels.
        The hiddensize is the number of classes you want your network to be divided into.

        The 3 hyperparameters in this network are learningrate, momentumterm and weight decay. They are set during
        initialisation automatically, but can be changed afterwards.
        Additionally the number of Gibbs-Sampling-Steps is set to 1 by default. An increased Samplingrate highers the
        precision but also increases the computation costs linearly.

        The dataset feed by every call of fit is sliced into mini-batches determind by the batch_size parameter.
        The whole data set is processed by the number of epochs specified in the constructor. The epochs can also be
        changed between the trainingcalls.

        If the verbose parameter is set true, the programm will be printing every 20 epochs the reconstruction error.

        The input_to_binary parameter converts every scalar on the input vector to 0 or 1.


    #Userinteraction: Train your Net
        The trainingprocess will start with the call fit. The function needs a trainset as input. The input can be
        formated with input_format.py. The contained python class uses a numpy array manage the input.
        During the training ever mini-batch will be processed and then the network will updates it's weights.

        The trainingprogress will be saved after every succefull call of fit.
        If one succesfull training with the fit function finished the trained weights can be restored by using the
        restore_previous_model parameter. In this case also a start_epoche should be specified, otherwise the visualisation
        of Tensorboard will be compromised.

        Every 20 epochs the network will calculate the loss. The result and some other statistically important values
        will be saved into the logs folder. Tensorboard can be used to visualize the progress of the network.

    #Userinteraction: Use the train Net
        After succesfully training the net, the classify function can be used to create prediction for a given input.
        The result will be provided as a numpy array. The input is again a input format. The user can specifiy if he
        wants to convert the input and/or output into binary digits. These options can influence the results of the
        network.
'''


class RBM(object):
    def __init__(self, input_size, hidden_size, main_dir="rbm", model_name="rbm_model",
                 standard_derivation=0.01, input_to_binary=False, verbose=False, ):
        '''
        :param input_size: Number of features used in the input vector
        :param hidden_size: Number of classes the output should be devided in
        :param main_dir: Directory where trainingdata, modeldata and imagedata should be saved to
        :param model_name: Name of the model
        :param standard_derivation: Standard-derivation for the random initialised weights
        :param input_to_binary: Determines if the network converts input into binary digits
        :param verbose: If true it will print the result of loss_function
        '''

        # Sets network-size
        self._input_size = input_size
        self._hidden_size = hidden_size

        # parameters to influence the learning process
        self._gibbs_sampling_steps = None
        self._batch_size = None
        self._momentum_factor = None
        self._learning_rate = None
        self._weight_decay_factor = None

        self._input_to_binary = input_to_binary
        self._standard_derivation = standard_derivation
        self._epochs = None

        # Tensorflow: variabales
        self._tf_w = None
        self._tf_bh = None
        self._tf_bv = None

        self._tf_delta_w = None
        self._tf_delta_bh = None
        self._tf_delta_bv = None

        self._tf_w_upd8 = None
        self._tf_bh_upd8 = None
        self._tf_bv_upd8 = None

        # Tesorflow: Placeholders
        self._tf_lr = None
        self._tf_momentum = None
        self._tf_weight_decay = None
        self._tf_gibbs_steps = None

        self._tf_input_data = None
        self._tf_hrand = None
        self._tf_vrand = None
        self._tf_desired_output = None

        # Varaibles to profile the training progress
        self._tf_loss_function = None
        self._tf_accuracy = None

        # Tensoflow: Manage tensoflow interactions
        self._tf_session = None
        self._tf_merged_summaries = None
        self._tf_summary_writer = None
        self._tf_saver = None

        # Profiling and Saving of Modellparameters
        self._main_dir = main_dir
        self._model_name = model_name
        self._model_dir, self._data_dir, self.summary_dir = self._create_data_directories()
        self._model_path = self._model_dir + self._model_name
        self._verbose = verbose

    def fit(self, train_set, validation_set=None, restore_previous_model=None, start_epoche=0, epochs=300,
            gibbs_sampling_steps=1, learning_rate=0.01, momentum_factor=0.9, weight_decay_factor=0.0001, batch_size=10):

        '''

        :param train_set: Trainset formatted as input_format.
        :param validation_set: Validationset formatted as input_format.
        :param restore_previous_model: If true restores learned model weights.
        :param start_epoche: Already passed epochs to keep the Tensorboard graph well formatted.
        :param epochs: Number of epochs the learning should last.
        :param gibbs_sampling_steps: Number of gibbs sampling steps the net should performs.
        :param learning_rate: Hyperparameter Learning rate parameter; will be devided by batch_size.
        :param momentum_factor: Specifies the momentumterm.
        :param weight_decay_factor:Specifies how strong the high weights are penetalized.
        :param batch_size: The trainingset is sliced in mini batches. One batch has the size of batch_size.
        :return: self.
        '''

        self._epochs = epochs
        self._learning_rate = learning_rate / batch_size
        self._momentum_factor = momentum_factor
        self._weight_decay_factor = weight_decay_factor * self._learning_rate
        self._gibbs_sampling_steps = gibbs_sampling_steps
        self._batch_size = batch_size

        self._build_model()
        self._create_summary_nodes(validation_set)

        with tf.Session() as self._tf_session:
            self._initialize_tf_utilities_and_ops(restore_previous_model)
            self._train_model(train_set, validation_set, start_epoche)
            self._tf_saver.save(self._tf_session, self._model_path)

        tf.reset_default_graph()

    def classify(self, input, input_to_binary=False, return_hstates=False):

        '''

        :param input: the input vectors to classify as input_format
        :param input_to_binary: if true input is normalized to 0 or 1
        :param return_hstates: if true returns only the values of 0 or 1
        :return: binary vector or probabilty which indicates the corresponding class of the inputdata
        '''

        self._create_placeholders()
        self._create_variables()

        if input_to_binary:
            self._tf_input_data = self._sample_prob(self._tf_input_data, self._tf_vrand)

        classification = self.sample_hidden_from_visible(self._tf_input_data)

        with tf.Session() as self._tf_session:
            init_op = tf.global_variables_initializer()
            self._tf_session.run(init_op)
            self._tf_saver = tf.train.Saver()
            self._tf_saver.restore(self._tf_session, self._model_path)

            hprobs, hstates = self._tf_session.run(classification, feed_dict=self._create_complete_dict(input))

        tf.reset_default_graph()

        if return_hstates:
            return hstates
        else:
            return hprobs

    def _initialize_tf_utilities_and_ops(self, restore_previous_model):

        '''

        :param restore_previous_model: if set to true the lastest learned weights are loaded to continue training
        :return: self
        '''
        init_op = tf.global_variables_initializer()

        self._tf_session.run(init_op)

        self._tf_merged_summaries = tf.summary.merge_all()
        self._tf_saver = tf.train.Saver()

        if restore_previous_model:
            self._tf_saver.restore(self._tf_session, self._model_path)

        self._tf_summary_writer = tf.train.SummaryWriter(self.summary_dir, self._tf_session.graph)

    def _train_model(self, train_set, validation_set, start_epoche):

        '''
            Devides the training process into the number of epochs. Every epoch run_train_step is called to iterate
            over the whole train_set.

        :param train_set: The input data formatted as input_format
        :param validation_set: The validation data formatted as input_format
        :param start_epoche:
        :return: self
        '''
        for i in range(self._epochs):
            self._run_train_step(train_set)

            if i % 20 == 0:
                self._run_summary(train_set, i + start_epoche)
                if validation_set:
                    self._run_validation_results(validation_set)

    def _run_train_step(self, train_set):

        '''
            Iterates over the whole training set.

        :param train_set: The input data formatted as input_format
        :return: self
        '''
        updates = [self._tf_w_upd8, self._tf_bh_upd8, self._tf_bv_upd8]

        iterations = (int)(train_set.num_examples / self._batch_size)

        for i in range(iterations):
            self._tf_session.run(updates, feed_dict=self._create_feed_dict(train_set))

    def _run_summary(self, train_set, epoch):

        '''
            After every 20 completed epochs the network performs a mergesummary call. The in create_summary_node
            called tensors are save to the logs file. Also the loss is calculated and also saved. The progress of the
            network can be monitored by tensorboard.

        :param train_set: [Update Needed] Can either operate the validation or the trainset
        :param epoch: An integer to plot the summary data to an x-value
        :return: self
        '''

        loss, summary_str = self._tf_session.run([self._tf_loss_function, self._tf_merged_summaries],
                                                 feed_dict=self._create_feed_dict(train_set))

        self._tf_summary_writer.add_summary(summary_str, epoch)

        if self._verbose:
            print("[loss]: ", loss)

    def _run_validation_results(self, mnist):

        '''
            [Update Needed] Not in use
        :param mnist:
        :return:
        '''

        validation_results = self._tf_session.run([self._tf_accuracy, self._tf_merged_summaries],
                                                  feed_dict=self._create_complete_dict(mnist))

        if self._verbose:
            print("[Accuracy]: ", validation_results[0])

    def _create_feed_dict(self, data):

        '''
            Helper function, which slices the inputdata at every iteration and feeds the data in a dictionary.
            The dictionary is used to feed the tensorplaceholders.

        :param data: takes the whole train_set in form of input_format
        :return: A dictionary with the data to feed to the network
        '''
        x, y = data.next_batch(self._batch_size)
        return {
            self._tf_input_data: x,
            self._tf_hrand: np.random.rand(x.shape[0], self._hidden_size),
            self._tf_vrand: np.random.rand(x.shape[0], self._input_size),
            self._tf_lr: self._learning_rate,
            self._tf_momentum: self._momentum_factor,
            self._tf_weight_decay: self._weight_decay_factor,
            self._tf_gibbs_steps: self._gibbs_sampling_steps
        }

    def _create_complete_dict(self, data):

        '''
            This function works like create_feed_dict but it also feeds a placeholder(self._tf_desired_output) with the desired output
            of the network.

        :param data: Validation data as input_format
        :return: A Dictionary with all data that needs to be feed to the network
        '''
        x = data.images
        return {
            self._tf_input_data: x,
            self._tf_hrand: np.random.rand(x.shape[0], self._hidden_size),
            self._tf_vrand: np.random.rand(x.shape[0], self._input_size),
            self._tf_lr: self._learning_rate,
            self._tf_momentum: self._momentum_factor,
            self._tf_weight_decay: self._weight_decay_factor,
            self._tf_gibbs_steps: self._gibbs_sampling_steps
        }

    def _build_model(self):

        '''
            For Tensorflow we need to specify the graph we want to run beforehand. A need graph is build by every call
            of fit. the build model has every needed to train the network.
            It creates the placeholders and variables. Then it performs the gibbs sampling steps to update the weights.
            The steps are structured with tf.name_scope to format the graph displayed in tensorboard.
            The build function also includes a graph for the accuracy and loss function.

        :return: self
        '''

        self._create_placeholders()

        self._create_variables()

        with tf.name_scope('learning_process'):
            with tf.name_scope('gibbs_sapmling_step'):
                hprobs0, hstates0, vprobs, hprobs1, hstates1 = self.gibbs_sampling_step(
                    self._sample_prob(self._tf_input_data, self._tf_vrand)
                )
            with tf.name_scope('compute_positive_association'):
                positive = self.compute_positive_association(self._tf_input_data, hprobs0, hstates0)

            with tf.name_scope('gibbs_sampling_steps'):
                nn_input = vprobs

                for step in range(self._gibbs_sampling_steps - 1):
                    hprobs, hstates, vprobs, hprobs1, hstates1 = self.gibbs_sampling_step(nn_input)
                    nn_input = vprobs

            with tf.name_scope('compute_negative_association'):
                negative = tf.matmul(tf.transpose(vprobs), hprobs1)

            self.encode = hprobs1

            with tf.name_scope('calculate_delta_weights'):
                d_w = self._tf_delta_w.assign(self._tf_lr * (positive - negative)
                                              + tf.scalar_mul(self._tf_momentum, self._tf_delta_w)
                                              - tf.scalar_mul(self._tf_weight_decay, self._tf_w))
                d_bh = self._tf_delta_bh.assign(self._tf_lr * tf.reduce_mean(hprobs0 - hprobs1, 0))
                d_bv = self._tf_delta_bv.assign(self._tf_lr * tf.reduce_mean(self._tf_input_data - vprobs, 0))

            with tf.name_scope('update_weights'):
                self._tf_w_upd8 = self._tf_w.assign_add(d_w)
                self._tf_bh_upd8 = self._tf_bh.assign_add(d_bh)
                self._tf_bv_upd8 = self._tf_bv.assign_add(d_bv)

        with tf.name_scope('accuracy'):
            result = self.sample_hidden_from_visible(self._tf_input_data)

            correct_prediction = tf.equal(tf.argmax(result[0], 1), tf.argmax(self._tf_desired_output, 1))
            self._tf_accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        with tf.name_scope('loss'):
            self._tf_loss_function = tf.sqrt(tf.reduce_mean(tf.square(self._tf_input_data - vprobs)))

    def _create_placeholders(self):

        '''
            Creates all needed Placeholders in one call. The placeholders can be feed at runtime.

        :return: self
        '''
        self._tf_input_data = tf.placeholder(tf.float32, [None, self._input_size], name="x-input")
        self._tf_hrand = tf.placeholder(tf.float32, [None, self._hidden_size], name="hrand")
        self._tf_vrand = tf.placeholder(tf.float32, [None, self._input_size], name="vrand")
        self._tf_desired_output = tf.placeholder(tf.float32, [None, self._hidden_size], name="Desired_Output")
        self._tf_lr = tf.placeholder(tf.float32, [], name="learning_rate")
        self._tf_momentum = tf.placeholder(tf.float32, [], name="momentum_term")
        self._tf_weight_decay = tf.placeholder(tf.float32, [], name="alpha")
        self._tf_gibbs_steps = tf.placeholder(tf.float32, [], name="gibbs_sampling_steps")

    def _create_variables(self):

        '''
            Creates all Variables in one function call. The variables contain the weights and weight changes.
            Tensor specified as tf.Variable are save by the tf.train.Saver after every succefull call of fit.
            If restore_previous_model is true the pre-initialised values we'll be overwritten by the previously save one.

        :return: self
        '''
        self._tf_w = tf.Variable(
            tf.random_normal((self._input_size, self._hidden_size), mean=0.0, stddev=self._standard_derivation),
            name="weights_" + self._model_name)
        self._tf_bh = tf.Variable(tf.zeros([self._hidden_size]), name="hidden_bias_" + self._model_name)
        self._tf_bv = tf.Variable(tf.zeros([self._input_size]), name="visible_bias_" + self._model_name)

        self._tf_delta_w = tf.Variable(tf.zeros([self._input_size, self._hidden_size]),
                                       name="delta_w_" + self._model_name)
        self._tf_delta_bh = tf.Variable(tf.zeros([self._hidden_size]), name="delta_bh_" + self._model_name)
        self._tf_delta_bv = tf.Variable(tf.zeros([self._input_size]), name="delta_bv_" + self._model_name)

    def gibbs_sampling_step(self, visible):

        '''
            Performes a complete Gibbs-Sapmling-Step

        :param visible: input vector
        :return: probality of the hidden layer, visible layer and a new hidden layer after one down up pass. Also the
                    binary staes of the hidden and the new hidden layer.
        '''
        hprobs, hstates = self.sample_hidden_from_visible(visible)
        vprobs = self.sample_visible_from_hidden(hprobs)
        hprobs1, hstates1 = self.sample_hidden_from_visible(vprobs)

        return hprobs, hstates, vprobs, hprobs1, hstates1

    def sample_hidden_from_visible(self, visible):

        '''
            Helper function. Performs an up-pass from the visible into the hidden layer.

        :param visible: Input vector with size of the visible layer
        :return: The probability and the states of the hidden layer after the up-pass
        '''
        hprobs = tf.nn.sigmoid(tf.matmul(visible, self._tf_w) + self._tf_bh)
        hstates = self._sample_prob(hprobs, self._tf_hrand)

        return hprobs, hstates

    def sample_visible_from_hidden(self, hidden):

        '''
        Helper function. Performs an down-pass from the hidden into the visible layer.

        :param hidden: Input vector with size of hidden layer.
        :return: The
        '''
        return tf.nn.sigmoid(tf.matmul(hidden, tf.transpose(self._tf_w)) + self._tf_bv)

    def compute_positive_association(self, visible, hidden_probs, hidden_states):
        '''
        Helper function to compute the positive association in one function call.

        :param visible:
        :param hidden_probs:
        :param hidden_states:
        :return:
        '''
        return tf.matmul(tf.transpose(visible), hidden_states)

    def _sample_prob(self, probs, rand):
        '''

        :param probs:
        :param rand:
        :return:
        '''
        return tf.nn.relu(tf.sign(probs - rand))

    def _create_summary_nodes(self, validation_set):
        '''

        :param validation_set:
        :return:
        '''
        with tf.name_scope('summaries'):
            with tf.name_scope('learning_progress'):
                # if validation_set:
                # tf.summary.scalar("accuracy", self._tf_accuracy)
                tf.summary.scalar("loss", self._tf_loss_function)
            with tf.name_scope('weight_development'):
                tf.summary.scalar("max_Weight", tf.reduce_max(self._tf_w))
                tf.summary.scalar("min_weight", tf.reduce_min(self._tf_w))
                tf.summary.histogram("delta_weights", self._tf_delta_w)
                tf.summary.histogram("weights", self._tf_w)
            with tf.name_scope('hyperparameter'):
                tf.summary.scalar("_learning_rate", self._learning_rate)
                tf.summary.scalar("Gibbs_sampling_steps", self._gibbs_sampling_steps)

    def _create_data_directories(self):
        '''

        :return:
        '''
        self._main_dir = self._main_dir + '/' if self._main_dir[-1] != '/' else self._main_dir

        models_dir = "models/" + self._main_dir
        data_dir = "data/" + self._main_dir
        summary_dir = "logs/" + self._main_dir

        for d in [models_dir, data_dir, summary_dir]:
            if not os.path.isdir(d):
                os.makedirs(d)

        return models_dir, data_dir, summary_dir

    def get_weights(self):
        '''

        :return:
        '''

        self._create_variables()
        with tf.Session() as self._tf_session:
            self._tf_saver = tf.train.Saver()
            self._tf_saver.restore(self._tf_session, self._model_path)

            w = self._tf_w.eval()
            bh = self._tf_bh.eval()

        tf.reset_default_graph()

        return w, bh

    def get_weights_as_images(self, width, height, outdir='img/', n_images=10, img_type='grey'):
        """ Create and save the weights of the hidden units with respect to the
        visible units as images.
        :param width:
        :param height:
        :param outdir:
        :param n_images:
        :param img_type:
        :return: self
        """

        outdir = self._data_dir + outdir
        self._build_model()
        with tf.Session() as self._tf_session:
            self._tf_saver = tf.train.Saver()

            self._tf_saver.restore(self._tf_session, self._model_path)

            weights = self._tf_w.eval()

            perm = np.random.permutation(self._hidden_size)[:n_images]

            for p in perm:
                w = np.array([i[p] for i in weights])
                image_path = outdir + self._model_name + '_{}.png'.format(p)

                utils.utilities.gen_image(w, width, height, image_path, img_type)


if __name__ == "__main__":
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

    rbm = RBM(784, 10, main_dir="Test", input_to_binary=True, verbose=False)

    rbm.fit(mnist.train, validation_set=None, restore_previous_model=False, start_epoche=0, gibbs_sampling_steps=1,
            learning_rate=0.1, weight_decay_factor=0.001, momentum_factor=0.5, epochs=1, batch_size=10)

    rbm.fit(mnist.train, validation_set=None, restore_previous_model=True, start_epoche=1, gibbs_sampling_steps=3,
            learning_rate=0.05, weight_decay_factor=0.001, momentum_factor=0.9, epochs=1, batch_size=100)

    rbm.fit(mnist.train, validation_set=None, restore_previous_model=True, start_epoche=2, gibbs_sampling_steps=5,
            learning_rate=0.01, weight_decay_factor=0.001, momentum_factor=0.9, epochs=1, batch_size=100)

    rbm.fit(mnist.train, validation_set=None, restore_previous_model=True, start_epoche=3, gibbs_sampling_steps=10,
            learning_rate=0.001, weight_decay_factor=0.001, momentum_factor=0.9, epochs=1, batch_size=100)

    rbm.fit(mnist.train, validation_set=None, restore_previous_model=True, start_epoche=4, gibbs_sampling_steps=20,
            learning_rate=0.0001, weight_decay_factor=0.001, momentum_factor=0.9, epochs=1, batch_size=100)

# bis 2880 gelernt
