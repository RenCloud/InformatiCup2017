Experiment Results
==================

The task was to write a automated classifier for GitHub repositorys.

Our idea was it to use a unsupevised network. We found out that you can stack multiple restricted Boltzmann machines to form a
Deep Belief network which has much better problem solving abilities. But we needed a discriminativ model. That's why we classified
some repositorys by hand. With this data set we could finetune the DBN and then use the DBN to generate new training data and contiune the training.

For your network we used Tensorflow with numpy to build the network. The introduction on how to use them can be found on the
:doc:`introduction` page. All testresults are visualized with Tensorboard.

First Experiment
----------------

Our first run with only 4700 unlabeled datasets wasn't really succefull. The hyperparameters were as followed:

===================== ================ ================ ================
Hyperparameter         Values 1         Values 2         Values 3
===================== ================ ================ ================
Epochs                  100             100              100
Batch size              10              100              100
learning rate           0.1             0.01             0.005
Gibbs sampling steps    1               3                5
Momentum term           0.5             0.9              0.9
Weight decay            0.0001          0.0001           0.0001
===================== ================= ================ ================

Network structure: 1370, 500, 500, 1500, 7

Accuracy got never over 16%. Sometimes way worse. But the weights stay small which was a win for us.


Next try with almost the same parameters but this time with 31700 unlabeled data sets. The initialization was long and the
input vector got up to 7300. The program took just 3GB but after the first epoch the memory usage doubled. We expect that
the :meth:`np.shuffle` and the ne permutated image and label array are the reason why the memeory usage exploded. In previouse tests
wasn't this in issue. We expect that there had to be some kind of an bug.

Because of this we had to constrain the input vector. Every word which happens to occure to few or too much is cut out of the vector.

After this we ended up with 1636 in input vector size.