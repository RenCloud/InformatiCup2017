import numpy as np


class DataSet(object):

    def __init__(self, input, output):
        self._num_examples = len(input)
        self._images = input
        self._labels = output
        self._index_in_epoch = 0
        self._epochs_completed = 0
        self.batch_size = 100

    def next_batch(self, size):
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

    @property
    def num_examples(self):
        return self._images.shape[0]

    @property
    def input_dim(self):
        return self._images.shape[1]

    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels
