
import tensorflow as tf
import numpy as np

from networks.RBM_CDK import RBM

class DBN(object):

    def __init__(self, layer_size, size, main_dir="dbn", model_name="dbn_model", learning_rate=0.01):
        self.layer_size = layer_size
        self.size = size

        self.RBMs = {}

    def pretraining(self, epochs,

                    gibbs_sampling_steps=1,
                    learning_rate=0.01,
                    first_layer_binary=True,
                    layer_output_binary=False,
                    weight_decay=0.0001):


        for i in range(self.size):
            self.RBMs[i] = RBM(self.layer_size[i], self.layer_size[i + 1], gibbs_sampling_steps=gibbs_sampling_steps,
                               learning_rate=learning_rate)

