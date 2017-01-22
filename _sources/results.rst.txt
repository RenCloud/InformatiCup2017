
Experiment Results
==================

Test and Validation that the network is working
-----------------------------------------------

To test that our implementation we let the network learn with the MNIST dataset. We used the dataset provided in the Tensorlow API.
Every machine learning program should perform well with MNIST. So if our program is learning this dataset then it is
most likely that we implemented it right.


RBM
^^^

The :class:`RBM` got first tested with the MNIST dataset provided by `google <https://www.tensorflow.org/tutorials/mnist/beginners/>`_.
After the training we couldn't test the accuracy because the unsupervised learning network didn't knew which value in the solution vector
corresponds to which number in the dataset.
It just could see the differences. But with the getImage function from `GitHub <https://github.com/blackecho/Deep-Learning-TensorFlow/blob/master/yadlt/utils/utilities.py>`_
we got a nice representation of our learned states.

DBN
^^^

The :class:`DBN` was also tested by the mnist dataset. We succeeded in learning the MNIST data up to 92% accuracy.
That was the prove that it worked. We first pretrained the network and then used the standard training process as described in
the `Tensorflow tutorials <https://www.tensorflow.org/tutorials/mnist/pros/>`_.


The idea
--------

The task was to write an automated classifier for GitHub repositorys.

Our idea was it to use a unsupevised network. We found out that you can stack multiple restricted Boltzmann machines to form a
Deep Belief network which has a much better problem solving ability then a single RBM. But we needed a discriminative model. That's why we classified
some repositories by hand. With this data set we could finetune the DBN and then use the DBN to generate new training data and continue the training.

For your network we used Tensorflow with numpy to build the network. The introduction on how to use them can be found on the
:doc:`introduction` page. All testresults are visualized with Tensorboard.

Most of the general ideas and informations are from Youtube. [youtubeDeep]


First Experiments
-----------------

Our first run with only 4700 unlabeled datasets wasn't really succefull. The hyperparameters were as followed:

================== ================== ================== ==================
Hyperparameter         Values 1         Values 2         Values 3
================== ================== ================== ==================
Epochs                  100              100               100
Batchsize               10               100               100
learningrate            0.1              0.01              0.005
Gibbssamplingsteps      1                3                 5
Momentumterm            0.5              0.9               0.9
Weightdecay             0.0001           0.0001            0.0001
================== ================== ================== ==================

Each layer is trained with the same 3 values.

Network structure: [1370, 500, 500, 1500, 7]

Accuracy got never over 16%. Sometimes way worse. But the weights stayed small which we interpreted as a good sign.
The choice of Opitmizer and learning rate for the finetuning part didn't had any effect on the testresults.


Next we tried it with almost the same parameters but this time with 31700 unlabeled data sets. The initialization was long and the
input vector got up to 7300. The program took just 3GB but after the first epoch the memory usage doubled. We decided to
shorten our input vector.

Every word which happens to occured to few or too much is cut out of the vector.

After this we ended up with an input vector with the size of 1636. The hyperparameters for the third test were as followed:


================== ================== ================== ================== ==================
Hyperparameter         Values 1         Values 2         Values 3            Values 4
================== ================== ================== ================== ==================
Epochs                  10               50                50                50
Batchsize               10               10                10                10
learningrate            0.1              0.01              0.005             0.001
Gibbssamplingsteps      1                1                 3                 4
Momentumterm            0.5              0.9               0.9               0.9
Weightdecay             0.0001           0.0001            0.0002            0.0002
================== ================== ================== ================== ==================

Network structure: [1636, 500, 500, 1500, 7]

We tested all possible optimizers, network structures and hyperparameters and came to the conclusion that single words aren't
usefull for a classification problem if they are used without a context.


New Inputvector
---------------

So we tried a new short input vector. Which encoded the following things:

#. Number of files in the repository
#. Number of commits
#. Number of open issues
#. Number of closed issues
#. Number of closed issues
#. Number of Users who left a comment
#. Number of Users who commited something

Every of these parameters was normalized relative to the number maximal possible number they could have which is 1000.
Because the GitHub API only returns the first 1000 issues, comments and so on.
But we observed that the network couldn't even learn a small dataset. To prove this we let the network train with our
supervised dataset and test every epoch how many of them it could classify correctly.
We never came above the 21% accuracy rate. That's why we reworked the vector again. This time we made the value relative
to the other values in the same repository because we expected that all of the given parameters are also dependent on how
big the repository is.

New vector:

#. Number of Files / the number of maximal possible files
#. Number of comments / Number of commits
#. Number of open issues / number of closed issues
#. Number of authors / number of files
#. Number of users who commited / number of files

But still the network couldn't even find a relatively good solution for all our 300 trainsets.

New Normalization Methods
-------------------------

Our hypotheses is that we chose a poor input vector. The network could't tell 300 networks apart by the presented values.

That's why we tried to find a better fitting one. If the network could tell our 300 vectors apart
it probably could learn more and generalise this idea.

The new vector we tested uses almost the same input values but this time we weren't trying to make them relative to each other.
We just used the absolute value but we normalized the whole vector later on.

Inputvalues:
#. Number of comments
#. Number of commits
#. Number of open issues
#. Number of closed issues
#. Number of users who commented
#. Number of users who commited

We tried a new method of normalizing the values between 1 and 0.
We used the :meth:`tensorflow.nn.l2_normalize` function. The trainingresults with a [6, 50, 100, 200, 400, 7] net
were slightly over our previously tested ones. we got up to 33% accuracy.

The shown graphs present the training progress of this netowork. We used a exponential decaying learning rate with a :class:`ProximalAdagradOptimizer`.
The l1 = 0.0001 and l2 0.001. Pretraining was with the following paramenters:

================== ================== ================== ================== ==================
Hyperparameter         Values 1         Values 2         Values 3            Values 4
================== ================== ================== ================== ==================
Epochs                  10               45                10                10
Batchsize               10               10                10                10
learningrate            0.1              0.01              0.001             0.0001
Gibbssamplingsteps      1                1                 3                 4
Momentumterm            0.5              0.9               0.9               0.9
================== ================== ================== ================== ==================

.. image:: finetuning_normalized_2.png

.. image:: finetuning_normalized_2_loss.png

.. image:: finetuning_normalized_2_lr.png

Keep in mind that the graph is smoothed by Tensorboard. That's why the 30% accuracy isn't visible.

During the pretraining we could observe that the first networks had really big weights and the following RBM's had too small weights.
That's why we changed the weight decay mechanic. Each entry in weight_dacy parameter corresponds to one RBM network.
That allowed us to tweak the weight decay for every RBM independently.
With this change the networks had a better weight development. The highest or lowest weights have a good initial value for the finetuning as
it can be seen here:

.. image:: pretraining_max_weights_normalized_2.png

.. image:: pretraining_min_weights_normalized_2.png


The graphs are saved in logs data_normalized_2. With Tensorboard you can display the graphs yourself, together with additional
information about the training. (:doc:`introduction`)


We also tested to shift the values of our training_set with a mean of 1 and
variance of 0.
In `this tutorial <http://r2rt.com/implementing-batch-normalization-in-tensorflow.html>`_ they used this normalization technique to normalize
the output of every layer in the neural network. We tried to use it as a way to normalize our input data into the first layer.
In our testcase with the same pretraining as done before, only with differently normalized data, hadn't any effect on the accuracy.



Other changes
-------------

Throughout the testing of the project we always did change parts of it here and there. But because we initially hadn't a working network
we couldn't determine if these changes were more or less useful. Simply because it had no effect on the networks accuracy.


The learningrate

The learning rate during pretraining was initially 0.001 - 0.00001 divided by the batch size. This value was originally from our tests with the
MNIST dataset. With a higher learning rate the loss couldn't decrement because the learning rate was too high.

After some time we decided to start with higher learningrate and degrade them over time. The pretraining results were much better
because the change in the loss was higher and most of the networks had an 20% accuracy after the first finetuning epoch.


Network topology

The network shrunk naturally after we thinned the input vector.
But during the testing process we tried different topologies:

#. [1600, 500, 500, 2000, 7]
    The vector is transposed into a smaller dimension where features are extrated. The second last layer then represents a vector with
    2000 features. The supervised training can now extract the features it needs to make the classification. The network learns more features
    than it needs but we can be sure the right one will be in there. This technique is inspired by the MNIST approach with pretraining.


#. [1600, 700, 500, 200, 500, 7000, 20000, 7]
    This is a huge network. But it can also be done with a smaller input vector and therefore smaller interior layers.
    This topology is inspired by autoencoders. First the input value is slowly compressed into a smaller vector.
    The second half of the network then reconstructs the input and gives an prediction.

#. [6, 200, 100, 50, 25, 7] or [1600, 800, 400, 200, 100, 7]
    This is the standard way of composing a neural network. The First layer is either turned into a bigger one or directly transformed
    into a smaller vector. The first version had some problems because the if we choose the second layer to big the weight tended to explode in
    the first weight matrix. That's why we used the above method to slowly higher the layer size.s

#. [6, 75, 7]
    This is the shallow version of a network. We tried this version to test if maybe the additional layers lower the accuracy of our network
    because they may not be needed.


Neurontypes

We started with a simple sigmoid activation function and a softmax layer at the last layer.
But in some literature and forums was suggested that the reLU neuron can improve the performance of a network by reducing the
effect vanishing gradient.
We also added a dropout rate of 50% to the network to prevent overfitting because we had just a small training set.

The training set

Because we had just so few training examples we early on decided to use pretraining to shorten the time our network needs to train
and maybe prevent it from overfitting.
Another idea to prevent overfitting is to let the network predict classes for the unlabeled data and add them to the supervised trainingset.
This idea can be seen in :meth:`Main.fit_dbn`. It's not used at the moment because the network itself isn't learning properly.


Optimizers and errorfunctions

We tetsted most of the available optimizers of Tensorflow. The obvious gradient decent algorithm was unstable when we didn't used the
prefect hyperparameters. Additionally the weights tended to overfit. The AdagradOptimizer got the most stable learning progress.
The :class:`ProximalAdagradOptimizer` and :class:`ProximalGradientDecentOptimizer` can be used as their not proximal counter part but
they offer additional build-in l1 and l2 regulation. So they prevented the network effectively from too high values.

As an error function we used the :meth:`tensorflow.nn.softmax_cross_entropy_with_logits`. This allows just one of the neurons to be active.
An alternative would have been the cross entropy as the sum of the squared error. This would have allowed multiple neurons to be active at
the same time. But our trainingset consisted of only one class solutions.
So we use the softmax version as default.


Pretraining

We varied the pretraining a little bit but we always stuck to the same plan of decaying the learning rate over time and meanwhile
increasing the number of gibbs sampling steps.
We tried to set the learning rate of the third trainingstep to 0.1. The network should use this as an opportunity to escape the
local minimas it might be stuck in. But instead it just provoked higher weights values and a worse loss value. Then when the next training
step started the network got back to it's state after the second training iteration.
One change that we kept is to set the initial momentum term to 0.5 for a short amount of time
we couldn't really detect a difference.
One bigger change was to use binary states as input for all networks. Previously we just turned the input for the first layer
into binary digits. But because we had the theory that the network is stuck in a local minima the stochastic natur of pretraining
with binary states should prevent this.


Evaluation
^^^^^^^^^^

The concept of pretraining a Deep Neural Network with RBM's and then finetune it with backpropagation proofed to be ineffective.
With the modular development the network could be easily modified. Also was the Tensorflow API easy to understand and to use.
That gave us the chance to test different input vectors,
neuron type, optimizers and learning rates. But none of the experiments performed well in our test setups.

The network itself was tested with the MNIST dataset. So it's capability of learning complex interactions with only raw pixel
is proofed.
We expect the error either in the input vector or in the chosen structure of our network. For example we couldn't find a
working network topology. Mostlikely it is a combination of all the above.

This high complexity makes it extremely difficult to find a solution. In addition to that the field of Deep Neural Networks
is a pretty new. Many different theories in how to interpret and improve their performance are available. Most of them
can't be proven mathematically. We had only the possibility to try out different things that worked in other networks and test
them in our.
Also is it difficult to interpret the output of the network. The low accuracy for example can be a result of a poor input vector,
poor trainingsdata or it can simply be stuck in a bad local minima.

To improve the performace we have different options:
#. The network would defently profit from more trainingdata because it helps generalising the problem.
#. We could use a more complex network like a convolutional network which can find solutions for more complex tasks.
#. If we retrieve more information from the GitHub API we could find a better suited input vector. Additionally we could
    perform something like Principal Component Analysis (PCA) to filter with value has  a real impact on our classification problem.
#. The normalisation could also be improved. The values should be between 0 and 1 which our method does. But most of the
    values getting to small which isn't optimal for the network.

All in all there are many possible ways to improve the classification ability of our network. But it is really difficult to tell
which should be used.

.. [youtubeDeep] https://www.youtube.com/channel/UC9OeZkIwhzfv-_Cb7fCikLQ