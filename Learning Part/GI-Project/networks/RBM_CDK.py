import tensorflow as tf
import numpy as np

import os
import ZConfig
from utils import utilities

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
'''

from tensorflow.examples.tutorials.mnist import input_data

class RBM(object):

    def __init__(self, input_size, hidden_size, main_dir="rbm", model_name="rbm_model", learning_rate=0.01,
                 gibbs_sampling_steps=1, batch_size=100, standard_derivation=0.1, epochs=10,
                 input_to_binary=False, verbose=False, momentum_factor=0.9, weight_decay_factor=0.00001):

        self.input_size = input_size
        self.hidden_size = hidden_size

        self.gibbs_sampling_steps = gibbs_sampling_steps
        self.batch_size = batch_size
        self.momentum_factor = momentum_factor

        self.learning_rate = learning_rate / batch_size
        self.weight_decay_factor = weight_decay_factor * learning_rate
        self.input_to_binary = input_to_binary

        self.standard_derivation = standard_derivation
        self.epochs = epochs

        self.W = None
        self.bh = None
        self.bv = None

        self.delta_w = None
        self.delta_bh = None
        self.delta_bv = None

        self.lr = None
        self.momentum = None
        self.alpha = None
        self.gibbs_steps = None

        self.w_upd8 = None
        self.bh_upd8 = None
        self.bv_upd8 = None

        self.input_data = None
        self.hrand = None
        self.vrand = None
        self.y = None

        self.encode = None

        self.tf_session = None
        self.loss_function = None

        '''Profiling and Saving of Modellparameters'''
        self.main_dir = main_dir
        self.model_name = model_name
        self.model_dir, self.data_dir, self.summary_dir = self._create_data_directories()
        self.model_path = self.model_dir + self.model_name

        self.tf_merged_summaries = None
        self.tf_summary_writer = None
        self.tf_saver = None

        self.verbose = verbose
        self.accuracy = None

    def fit(self, train_set, validation_set=None, restore_previous_model=None, start_epoche=0):
        self._build_model()
        self._create_summary_nodes()

        with tf.Session() as self.tf_session:
            self._initatlize_tf_utilities_and_ops(restore_previous_model)
            self._train_model(train_set, validation_set, start_epoche)
            self.tf_saver.save(self.tf_session, self.model_path)

        tf.reset_default_graph()

    def classify(self, input, input_to_binary=False, return_hstates=False):
        with tf.Session() as self.tf_session:
            init_op = tf.global_variables_initializer()
            self.tf_session.run(init_op)
            self.tf_saver = tf.train.Saver()
            self.tf_saver.restore(self.tf_session, self.model_path)

            processed_input = input

            if input_to_binary:
                processed_input = self._sample_prob(input, self.vrand)

            hprobs, hstates = self.tf_session.run(self.sample_hidden_from_visible(processed_input))

            if return_hstates:
                return hstates
            else:
                return hprobs

    def _initatlize_tf_utilities_and_ops(self, restore_previous_model):
        init_op = tf.global_variables_initializer()

        self.tf_merged_summaries = tf.summary.merge_all()
        self.tf_saver = tf.train.Saver()

        self.tf_session.run(init_op)

        if restore_previous_model:
            self.tf_saver.restore(self.tf_session, self.model_path)

        self.tf_summary_writer = tf.train.SummaryWriter(self.summary_dir, self.tf_session.graph)

    def _train_model(self, train_set, validation_set, start_epoche):
        for i in range(start_epoche, self.epochs):
            self._run_train_step(train_set)

            if i == 200:
                self.learning_rate = 0.05 / self.batch_size

            if i == 600:
                self.learning_rate = 0.01 / self.batch_size

            if i == 1000:
                self.learning_rate = 0.002 / self.batch_size

            if i % 10 == 0:
                self._run_test(validation_set, i)

    def _run_train_step(self, train_set):

        updates = [self.w_upd8, self.bh_upd8, self.bv_upd8]

        iterations = (int)(train_set.num_examples / self.batch_size)

        for i in range(iterations):
            self.tf_session.run(updates, feed_dict=self._create_feed_dict(train_set))

    def _run_test(self, mnist, epoch):

        input = mnist.test.images

        validation_results = self.tf_session.run([self.accuracy, self.tf_merged_summaries],
                                                 feed_dict={self.input_data: input,
                                                            self.hrand: np.random.rand(input.shape[0], self.hidden_size),
                                                            self.vrand: np.random.rand(input.shape[0], self.input_size),
                                                            self.y: mnist.test.labels,
                                                            self.lr: self.learning_rate,
                                                            self.momentum: self.momentum_factor,
                                                            self.alpha: self.weight_decay_factor,
                                                            self.gibbs_steps: self.gibbs_sampling_steps}
                                                 )
        self.tf_summary_writer.add_summary(validation_results[1], epoch)
        if self.verbose:
            print("[Accuracy]: ", validation_results[0])

    def _create_feed_dict(self, data):
        x, y = data.next_batch(self.batch_size)
        return{
            self.input_data: x,
            self.hrand: np.random.rand(x.shape[0], self.hidden_size),
            self.vrand: np.random.rand(x.shape[0], self.input_size),
            self.lr: self.learning_rate,
            self.momentum: self.momentum_factor,
            self.alpha: self.weight_decay_factor,
            self.gibbs_steps: self.gibbs_sampling_steps
        }

    def _create_validation_data(self, data):
        x = data.test.images
        return{
            self.input_data: x,
            self.hrand: np.random.rand(x.shape[0], self.hidden_size),
            self.vrand: np.random.rand(x.shape[0], self.input_size),
            self.lr: self.learning_rate,
            self.momentum: self.momentum_factor,
            self.alpha: self.weight_decay_factor,
            self.gibbs_steps: self.gibbs_sampling_steps
        }

    def _build_model(self):

        self.input_data, self.hrand, self.vrand, self.y, self.lr, self.momentum, self.alpha, self.gibbs_steps = self._create_placeholders()

        self.w, self.bh, self.bv, self.delta_w, self.delta_bh, self.delta_bv = self._create_variables()

        with tf.name_scope('learning_process'):

            with tf.name_scope('gibbs_sapmling_step'):
                hprobs0, hstates0, vprobs, hprobs1, hstates1 = self.gibbs_sampling_step(
                    self._sample_prob(self.input_data, self.vrand)
                )
            with tf.name_scope('compute_positive_association'):
                positive = self.compute_positive_association(self.input_data, hprobs0, hstates0)

            with tf.name_scope('gibbs_sampling_steps'):
                nn_input = vprobs
                '''
                i = tf.constant(1, tf.float32)

                def gibbs_sampling_loop(i, gibbs_steps, hprobs, hstates, vprobs, hprobs1, hstates1):
                    hprobs, hstates, vprobs, hprobs1, hstates1 = self.gibbs_sampling_step(vprobs)
                    return i + 1, gibbs_steps, hprobs, hstates, vprobs, hprobs1, hstates1

                def gibbs_loop_condition(i, gibbs_steps, hprobs, hstates, vprobs, hprobs1, hstates1):
                    return i < gibbs_steps

                a, b, hprobs, hstates, vprobs, hprobs1, hstates1 = tf.while_loop(gibbs_sampling_loop,
                                                                                 gibbs_loop_condition,
                                                                                 [i, self.gibbs_steps,
                                                                                  hprobs0, hstates0,
                                                                                  vprobs, hprobs1, hstates1],
                                                                                 parallel_iterations=1,
                                                                                 back_prop=False,
                                                                                 shape_invariants=None)
                '''
                for step in range(self.gibbs_sampling_steps - 1):
                    hprobs, hstates, vprobs, hprobs1, hstates1 = self.gibbs_sampling_step(nn_input)
                    nn_input = vprobs

            with tf.name_scope('compute_negative_association'):
                negative = tf.matmul(tf.transpose(vprobs), hprobs1)

            self.encode = hprobs1

            with tf.name_scope('calculate_delta_weights'):
                d_w = self.delta_w.assign(self.lr * (positive - negative)
                                          + tf.scalar_mul(self.momentum, self.delta_w)
                                          - tf.scalar_mul(self.alpha, self.w))
                d_bh = self.delta_bh.assign(self.lr * tf.reduce_mean(hprobs0 - hprobs1, 0))
                d_bv = self.delta_bv.assign(self.lr * tf.reduce_mean(self.input_data - vprobs, 0))

            with tf.name_scope('update_weights'):
                self.w_upd8 = self.w.assign_add(d_w)
                self.bh_upd8 = self.bh.assign_add(d_bh)
                self.bv_upd8 = self.bv.assign_add(d_bv)

        with tf.name_scope('accuracy'):
            result = self.sample_hidden_from_visible(self.input_data)

            correct_prediction = tf.equal(tf.argmax(result[0], 1), tf.argmax(self.y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        with tf.name_scope('loss'):
            self.loss_function = tf.sqrt(tf.reduce_mean(tf.square(self.input_data - vprobs)))

    def _create_placeholders(self):
        x = tf.placeholder(tf.float32, [None, self.input_size], name="x-input")
        hrand = tf.placeholder(tf.float32, [None, self.hidden_size], name="hrand")
        vrand = tf.placeholder(tf.float32, [None, self.input_size], name="vrand")
        y = tf.placeholder(tf.float32, [None, self.hidden_size], name="Desired_Output")
        lr = tf.placeholder(tf.float32, [], name="learning_rate")
        momen = tf.placeholder(tf.float32, [], name="momentum_term")
        alpha = tf.placeholder(tf.float32, [], name="alpha")
        gibbs_steps = tf.placeholder(tf.float32, [], name="gibbs_sampling_steps")

        return x, hrand, vrand, y, lr, momen, alpha, gibbs_steps

    def _create_variables(self):
        w = tf.Variable(tf.random_normal((self.input_size, self.hidden_size), mean=0.0, stddev=self.standard_derivation),
                        name="weights")
        bh = tf.Variable(tf.zeros([self.hidden_size]), name="hidden_bias")
        bv = tf.Variable(tf.zeros([self.input_size]), name="visible_bias")

        d_w = tf.Variable(tf.zeros([self.input_size, self.hidden_size]), name="delta_w")
        d_bh = tf.Variable(tf.zeros([self.hidden_size]), name="delta_bh")
        d_bv = tf.Variable(tf.zeros([self.input_size]), name="delta_bv")

        return w, bh, bv, d_w, d_bh, d_bv

    def gibbs_sampling_step(self, visible):
        hprobs, hstates = self.sample_hidden_from_visible(visible)
        vprobs = self.sample_visible_from_hidden(hprobs)
        hprobs1, hstates1 = self.sample_hidden_from_visible(vprobs)

        return hprobs, hstates, vprobs, hprobs1, hstates1

    def sample_hidden_from_visible(self, visible):
        hprobs = tf.nn.sigmoid(tf.matmul(visible, self.w) + self.bh)
        hstates = self._sample_prob(hprobs, self.hrand)

        return hprobs, hstates

    def sample_visible_from_hidden(self, hidden):
        return tf.nn.sigmoid(tf.matmul(hidden, tf.transpose(self.w)) + self.bv)

    def compute_positive_association(self, visible, hidden_probs, hidden_states):
        return tf.matmul(tf.transpose(visible), hidden_states)

    def _sample_prob(self, probs, rand):
        return tf.nn.relu(tf.sign(probs - rand))

    def _create_summary_nodes(self):
        with tf.name_scope('summaries'):
            with tf.name_scope('learning_progress'):
                tf.summary.scalar("accuracy", self.accuracy)
                tf.summary.scalar("loss", self.loss_function)
            with tf.name_scope('weight_development'):
                tf.summary.scalar("max_Weight", tf.reduce_max(self.w))
                tf.summary.scalar("min_weight", tf.reduce_min(self.w))
                tf.summary.histogram("delta_weights", self.delta_w)
                tf.summary.histogram("weights", self.w)
            with tf.name_scope('hyperparameter'):
                tf.summary.scalar("learning_rate", self.learning_rate)
                tf.summary.scalar("Gibbs_sampling_steps", self.gibbs_sampling_steps)

    def _create_data_directories(self):
        self.main_dir = self.main_dir + '/' if self.main_dir[-1] != '/' else self.main_dir

        models_dir = "models/" + self.main_dir
        data_dir = "data/" + self.main_dir
        summary_dir = "logs/" + self.main_dir

        for d in [models_dir, data_dir, summary_dir]:
            if not os.path.isdir(d):
                os.makedirs(d)

        return models_dir, data_dir, summary_dir

    def get_weights(self):
        with tf.Session() as self.tf_session:
            init_op = tf.global_variables_initializer()
            self.tf_session.run(init_op)
            self.tf_saver = tf.train.Saver()
            self.tf_saver.restore(self.tf_session, self.model_path)

            return {
                "w": self.w.eval(),
                "bh": self.bh.eval(),
                "bv": self.bv.eval()
            }

if __name__ == "__main__":
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

    rbm = RBM(784, 10, batch_size=100, epochs=300, main_dir="rbm_variable_hyperparameter", gibbs_sampling_steps=1,
              learning_rate=0.1, input_to_binary=True, verbose=False)

    #rbm.fit(mnist.train, validation_set=mnist, restore_previous_model=False, start_epoche=0)
    #rbm.gibbs_sampling_steps = 3
    #rbm.epochs = 600
    #rbm.fit(mnist.train, validation_set=mnist, restore_previous_model=True, start_epoche=300)
    #rbm.gibbs_sampling_steps = 5
    #rbm.epochs = 900
    #rbm.fit(mnist.train, validation_set=mnist, restore_previous_model=True, start_epoche=600)
    rbm.gibbs_sampling_steps = 10
    rbm.epochs = 1200
    rbm.fit(mnist.train, validation_set=mnist, restore_previous_model=True, start_epoche=900)
