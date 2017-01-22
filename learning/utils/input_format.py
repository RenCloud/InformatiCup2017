import numpy as np


class DataSet(object):

    def __init__(self, input, output):

        '''
        This is a helper class. Most of the code is used from tensorflow.examples.tutorials.mnist.input_data.
                The structure contains two numpy arrays. The RBM and DBN are using this wrapper for their input and desired
                output data.
                The class offers some helpful functions to get only parts of the data to train one batch. New data can also be
                added at any time.

        :param input: numpy array as inputdata vector
        :param output: numpy array with the desired output
        '''
        self._num_examples = len(input)
        self._images = input
        self._labels = output
        self._index_in_epoch = 0
        self._epochs_completed = 0
        self.batch_size = 100

    def next_batch(self, size):

        '''
        A function used in every trainingfunction where batches are required. The function generates a random
         permutation of the data and returns a chunk of the specified size of the data.

        :param size: The size of the batch.
        :return: Returns a random chunk of the data with the size of the size parameter.
        '''
        start = self._index_in_epoch
        self.batch_size = size
        self._index_in_epoch += self.batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Shuffle the data
            perm = np.arange(self._num_examples)
            np.random.shuffle(perm)
            self._images = self._images[perm]
            self._labels = self._labels[perm]
            # Start next epoch
            start = 0
            self._index_in_epoch = self.batch_size
            assert self.batch_size <= self._num_examples
        end = self._index_in_epoch

        return self._images[start:end], self._labels[start:end]

    def append(self, data, labels):

        '''
        The image and labels array can be increased at any time.

        :param data: The data that should be appended to the image array
        :param labels: The labels that should be appended to the labels array. Has to have the same size as data.
        :return: self
        '''

        if data.shape[0] != labels.shape[0]:
            print("[ERROR] uneven length of added Vectors")
            assert data.shape[0] == labels.shape[0]

        self._images = np.append(self._images, data, axis=0)
        self._labels = np.append(self._labels, labels, axis=0)

        self._num_examples = len(self._images)


    @property
    def num_examples(self):

        '''
            A getter method for the number of examples

        :return: Number of examples
        '''

        return self._images.shape[0]

    @property
    def input_dim(self):

        '''
            A getter function for the input size.

        :return: Returns the size of a single vector
        '''

        return self._images.shape[1]

    @property
    def images(self):

        '''
            A getter function to get the input data for the network.

        :return: Returns the image numpy array.
        '''

        return self._images

    @property
    def labels(self):

        '''
            A getter function to get the labeled data for the network.

        :return: Returns the labeles numpy array.
        '''

        return self._labels
