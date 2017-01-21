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

Accuracy got never over 16%. Sometimes way worse. But the weights stay small which was a win for us.
The choice of Opitmizer and learning rate for the finetuning part didn't had any effect on the testresults.


Next try with almost the same parameters but this time with 31700 unlabeled data sets. The initialization was long and the
input vector got up to 7300. The program took just 3GB but after the first epoch the memory usage doubled. We expect that
the :meth:`np.random.shuffle` and the ne permutated image and label array are the reason why the memeory usage exploded. In previouse tests
wasn't this in issue. We expect that there had to be some kind of an bug.

Because of this we had to constrain the input vector. Every word which happens to occure to few or too much is cut out of the vector.

After this we ended up with 1636 in input vector size. The hyperparameters for the third test were as followed:


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

We tested all possible optimizers netstructures and hyperparameters and came to the conclusion that single words aren't
usefull for a classification problem if they are used without a context.

So we tried a new short input vector. Which encoded the following things:
#. Number of files in the repository
#. Number of commits
#. Number of open issues
#. Number of closed issues
#. Number of closed issues
#. Number of Users how left a comment
#. Number of Users how commited something

Every of these parameters was normalized relativly to the number of ... in the whole data set.
But we observed that the network couldn't even learn a small dataset. To prove this we let the network train with our
supervised dataset and test every epoch how many of them it could classify correctly.
We never did crack the 21% accuracy rate. That's why we reconstructed the vector again this time we made the value relative
to the other values in the repository. Because we expected that all of the given parameters are also kind of dependent how
big the repository is.
New vector:
#. Number of Files / the number of maximal possible files
#. Number of comments / Number of commits
#. Number of open issues / number of closed issues
#. Number of authors / number of files
#. Number of users who commited / number of files

But still the network couldn't even find a relatively good solution for all our 300 trainsets.

New kind of Weight decay in rbms to controll the jumping weight growth
