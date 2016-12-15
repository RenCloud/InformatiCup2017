
import tensorflow as tf
import numpy as np

import os

from networks.RBM_CDK import RBM

from tensorflow.examples.tutorials.mnist import input_data
from utils.input_format import DataSet


class DBN(object):

    def __init__(self,
                 layer_size,
                 size,
                 main_dir="dbn",
                 model_name="dbn_model"
                 ):
        self.layer_size = layer_size
        self.size = size

        self.RBMs = {}

        self.train_set = None

        self.main_dir = main_dir
        self.model_name = model_name
        self.model_dir, self.data_dir, self.summary_dir = self._create_data_directories()
        self.model_path = self.model_dir + self.model_name

        self.w = {}
        self.bv = {}
        self.bh = {}

        self.hrand = {}
        self.vrand = {}

        self.input_data = None
        self.output = None
        self.y = None

        self.gibbs_sampling_steps = None


        self.tf_session = None
        self.tf_saver = None

    def pretraining(self,
                    gibbs_sampling_steps=[1],
                    learning_rate=[0.1],
                    weight_decay=[0.0001],
                    momentum=[0.9],
                    epoch_steps=[500],
                    first_layer_binary=True,
                    layer_output_binary=False,
                    validation_set=None,
                    continue_training=[False]):
        for i in range(self.size):

            input_to_binary = False
            if i == 0 and first_layer_binary:
                input_to_binary = True

            self.RBMs[i] = RBM(self.layer_size[i], self.layer_size[i + 1], main_dir="dbn/rbm_" + repr(i),
                               input_to_binary=input_to_binary)

            start_epoch = 0

            for n in range(len(epoch_steps)):
                self.RBMs[i].learning_rate = learning_rate[n]
                self.RBMs[i].momentum_factor = momentum[n]
                self.RBMs[i].epochs = epoch_steps[n]
                self.RBMs[i].weight_decay_factor = weight_decay[n]
                self.RBMs[i].gibbs_sampling_steps = gibbs_sampling_steps[n]



                if n != 0:
                    start_epoch += epoch_steps[n - 1]

                self.RBMs[i].fit(self.train_set, restore_previous_model=continue_training[n], start_epoche=start_epoch,
                                 validation_set=validation_set)

            print("[INFO] pretraining %d ended", i)
            self.train_set = self.RBMs[i].classify(self.train_set, input_to_binary=None, return_hstates=None)

            self.train_set = DataSet(self.train_set, self.train_set)
            print("[INFO] new dataset generated")

    def classify(self, input, build_dbn=False):
        if build_dbn:
            self._build_dbn_from_rbns()

        self._build_deterministic_model()

        with tf.Session() as self.tf_session:
            self.tf_session.run(tf.global_variables_initializer())
            self.tf_saver = tf.train.Saver()
            self.tf_saver.restore(self.tf_session, self.model_path)

            return self.tf_session.run(self.output, feed_dict={self.input_data: input})

    def _build_dbn_from_rbns(self):

        for i in range(self.size):
            temp_w, temp_bh, temp_bv = self.RBMs[i].get_weights()
            self.w[i] = tf.Variable(tf.float32, temp_w, name="dbn_weight_" + i)
            self.bv[i] = tf.Variable(tf.float32, temp_bv, name="dbn_bias_visible_" + i)
            self.bh[i] = tf.Variable(tf.float32, temp_bh, name="dbn_bias_hidden_" + i)

        with tf.Session() as self.tf_session:
            self.tf_session.run(tf.global_variables_initializer())
            self.tf_saver = tf.train.Saver()
            self.tf_saver.save(self.tf_session, self.model_path)

    def _build_deterministic_model(self):
        self._create_variables()
        self._create_placeholder()

        act_prob = self.input_data

        for i in range(self.size):
            act_prob = self._propup(act_prob)

        self.output = act_prob

    # TODO
    # da der code aus dem paper mit row vectors arbeitet muss in und output noch transponiert werden, ganuso wie auch desired output

    def _build_up_down_algorithm(self):
        self._create_variables()
        self._create_placeholder()

        probs = self.input_data
        states = None

        # Bottom-up pass
        for i in range(self.size - 2):
            probs = tf.nn.sigmoid(probs * self.w[i] + self.bh[i])
            states = self._sample_prob(probs, self.hrand[i])

        waketopprobs = tf.nn.sigmoid(states * self.w[-2] + self.y * self.w[-1] + self.bh[-1]) # nicht sicher was man für tobiases einsetzten soll
        waketopstates = self._sample_prob(waketopprobs, self.hrand[-1]) # noch nicht sicher welches rand man nehmen sollte
        # eigentlich müsste ja ein rand für jeden layer ausreichen

        # positive phase statistics for constrative divergence
        poslabtopstatistics = tf.matmul(self.y, waketopstates, transpose_a=True)
        pospentopstatistics = tf.matmul(states, waketopstates, transpose_a=True)

        # perform numCDiters gibbs sampling iterations unsing the top level unidirected associative memory
        negtopstates = waketopstates
        for i in range(1, self.gibbs_sampling_steps):
            negpenprobs = tf.nn.sigmoid(tf.matmul(negtopstates, self.w[-2], transpose_b=True) + self.bv[-2])
            negpenstates = self._sample_prob(negpenprobs, self.vrand[-2])
            neglabprops = tf.nn.softmax(tf.matmul(negtopstates, self.w[-1], transpose_b=True) + self.bv[-1]) # wenn ein fehler auftritt könnte es an der
            # axis liegen auf die softmax perfromed wird. Denn der code dieser funtion is transposed
            negtopprobs = tf.nn.sigmoid(negpenstates * self.w[-2] + neglabprops * self.w[-1] + self.bv[-1]) # nicht sicher ob bv oder bh
            negtopstates = self._sample_prob(negtopprobs, self.bv[-1])

        #negative phase for constrative divergence
        for i in reversed(range(1, self.size - 2)):
            sleeppenstates = negpenstates
            sleephidprobs = tf.nn.sigmoid(sleeppenstates * self.w[-i] + self.bv[-i])

        # predictions
        # psleepstates =

    def _create_variables(self):
        for i in range(self.size):
            self.w[i] = tf.Variable(tf.float32, tf.zeros([self.layer_size[i], self.layer_size[i + 1]]),
                                    name="dbn_weight_" + i)
            self.bv[i] = tf.Variable(tf.float32, tf.zeros([self.layer_size[i]]), name="dbn_bias_visible_" + repr(i))
            self.bh[i] = tf.Variable(tf.float32, tf.zeros([self.layer_size[i + 1]]), name="dbn_bias_hidden_" + repr(i))

    def _create_placeholder(self):
        self.input_data = tf.placeholder(tf.float32, [None, self.layer_size[0]], name="input-data")
        self.y = tf.placeholder(tf.float32, [None, self.layer_size[-1]], name="desired-output")

        for i in range(self.size):
            self.vrand[i] = tf.placeholder(tf.float32, [self.layer_size[i]], name="vrand_" + repr(i))
            self.hrand[i] = tf.placeholder(tf.float32, [self.layer_size[i + 1]], name="hrand_" + repr(i))

    # Passt hier nicht rein
    def _propup(self, input):
        return tf.nn.sigmoid(tf.matmul(input, self.w) + self.bh)

    def _sample_prob(self, probs, rand):
        return tf.nn.relu(tf.sign(probs - rand))

    def _create_data_directories(self):
        self.main_dir = self.main_dir + '/' if self.main_dir[-1] != '/' else self.main_dir

        models_dir = "models/" + self.main_dir
        data_dir = "data/" + self.main_dir
        summary_dir = "logs/" + self.main_dir

        for d in [models_dir, data_dir, summary_dir]:
            if not os.path.isdir(d):
                os.makedirs(d)

        return models_dir, data_dir, summary_dir


if __name__ == '__main__':
    dbm = DBN([784, 500, 250, 25, 10], 4)

    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
    dbm.train_set = mnist.train
    dbm.pretraining(gibbs_sampling_steps=[1, 3, 5], learning_rate=[0.1, 0.01, 0.005], weight_decay=[0.0001, 0.0001, 0.0001],
                    momentum=[0.5, 0.9, 0.9], continue_training=[False, False, False], epoch_steps=[1, 1, 1])
