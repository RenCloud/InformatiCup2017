Introducing the learning mechanism
==================================

Basic Structure
---------------

This part of Project exists of three directories: :file:`frontend`, :file:`networks` and :file:`utils`.

The networks are contained in :file:`networks`. The package :file:`frontend.Main` is a wrapper for the learning process.
The :file:`utils` is a package containing all helper modules.


The networks
------------

Restricted Boltzmann machine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

"A restricted Boltzmann machine (RBM) is a generative stochastic artificial neural network that can learn a probability
distribution over its set of inputs."[WikiBoltz]_.
"As their name implies, RBMs are a variant of Boltzmann machines, with the restriction that their neurons must form a
bipartite graph: a pair of nodes from each of the two groups of units (commonly referred to as the "visible" and "hidden"
units respectively) may have a symmetric connection between them; and there are no connections between nodes within a group.
By contrast, "unrestricted" Boltzmann machines may have connections between hidden units. This restriction allows for more
efficient training algorithms than are available for the general class of Boltzmann machines, in particular the gradient-based
contrastive divergence algorithm"[WikiBoltz]_.



If you are interested in a deeper understanding of Restricted Boltzmann machines free to read this
`introduction to Restricted Roltzmann Machines <http://image.diku.dk/igel/paper/AItRBM-proof.pdf>`_.
Additionally the Paper of `Geoffrey Hinton <https://www.cs.toronto.edu/~hinton/absps/guideTR.pdf>`_ is nice read if you
are intending to use Boltzmann machines in practice.


Deep Belief Network
^^^^^^^^^^^^^^^^^^^

"In machine learning, a deep belief network (DBN) is a generative graphical model, or alternatively a type of deep neural network,
composed of multiple layers of latent variables ("hidden units"), with connections between the layers but not between units within each layer.

When trained on a set of examples in an unsupervised way, a DBN can learn to probabilistically reconstruct its inputs.
The layers then act as feature detectors on inputs.[1] After this learning step, a DBN can be further trained
in a supervised way to perform classification.[2]

DBNs can be viewed as a composition of simple, unsupervised networks such as restricted Boltzmann machines (RBMs)
or autoencoders,[3] where each sub-network's hidden layer serves as the visible layer for the next. This also leads
to a fast, layer-by-layer unsupervised training procedure, where contrastive divergence is applied to each sub-network
in turn, starting from the "lowest" pair of layers (the lowest visible layer being a training set).

The observation, due to Yee-Whye Teh,[2] that DBNs can be trained greedily, one layer at a time,
led to one of the first effective deep learning algorithms."[WikiDBN]_


How to
------

In this section we discribe how to use the :mod:`~../learning` module. You can easily utilize the :mod:`../frontend`
module to train your own GitHub-Classifier or you can use the general structure of :class:`../networks.RBM_CDK.RBM` or
:class:`../networks.DBN.DBN` to create your on learning task.

First we start with using the :mod:`~../frontend.Main`:
The :meth:`~../frontend.Main.fit_dbn` uses JSON strings to require it's data.::

    def fit_dbn(data_set, main_dir="dbn/", supervised_train_set=None, validation_set=None):
        # convert JSON string to numpy arrays
        # ...
        # initialize network
        dbn = DBN([input.input_dim, 500, 500, 1500, 7], main_dir=main_dir)

        # start pretraining
        dbn.pretraining(input, gibbs_sampling_steps=[1, 3, 5], learning_rate=[0.1, 0.01, 0.005],
                    weight_decay=[0.0001, 0.0001, 0.0001],
                    momentum=[0.5, 0.9, 0.9], continue_training=[False, True, True], epoch_steps=[100, 100, 100],
                    batch_size=[10, 100, 100])

        # our used finetuning algortihm
        dbn.supervised_finetuning(batch_size=1, data_set=train_set, epochs=1, make_dbn=True,
                                  validation_set=validation_set)

        for i in range(100):
            dbn.supervised_finetuning(batch_size=1, data_set=train_set, epochs=1, make_dbn=False,
                                      validation_set=validation_set)

            examples = train_set.next_batch(25 + i)

            prediction = dbn.classify(examples[0])

            train_set.append(examples[0], prediction)

The function uses a :class:`../networks.DBN.DBN` with 5 layers. The first four are used for pretraining. During the pretraining
the network is split in 3 :class:`../networks.RBM_CDK.RBM`. Each is trained 3 times always with different hyperparameters.
The different hyperparameters can be seen in the argument list.

After this initial phase two epochs of :meth:`~../networks.DBN.DBN.supervised_pretraining` is performed with the supervised
training set. The set was classified by hand. But the trainingset only consists of ca. 300 examples. That's why the network
predicts classes for the unsupervised traingset and adds them to the supervised trainingset.


Now let's take a look at what the :class:`../networks.DBN.DBN` is doing.
:class:`../networks.DBN.DBN` has two important public functions:::

    def pretraining(self, train_set, gibbs_sampling_steps=[1], learning_rate=[0.1], weight_decay=[0.0001], momentum=[0.9],
                    epoch_steps=[500], first_layer_binary=True, layer_output_binary=False, continue_training=[False], batch_size=[10]):















.. [WikiBoltz] https://en.wikipedia.org/wiki/Restricted_Boltzmann_machine
.. [WikiDBN] https://en.wikipedia.org/wiki/Deep_belief_network