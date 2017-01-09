Get Started with Tensorflow
===========================

Installation
------------
The program mainly uses `Tensorflow <https://www.tensorflow.org/>`_ and `numpy <http://www.numpy.org/>`_ and python 3.5.

Tensoflow can be installed via pip install. Additional installation Methods can be found at
`Tensorflow.org <https://www.tensorflow.org/get_started/os_setup>`_. Tensorflow offers an additional version to run
your program on a GPU. The website offers a describtion on how to use
`NVIDIA GPUs <https://www.tensorflow.org/how_tos/using_gpu/>`_
, but this code is only programed and tested for CPUs.


Basic usage of Tensorflow
-------------------------

To get a better understanding of python we take a look at program example from `Tesorflow.org <https://www.tensorflow.org/get_started/>`_.

First Tensorflow and numpy have to be imported.::

    import tensorflow as tf
    import numpy as np

Then we create our input data and the desired output. These are saved as numpy arrays. Numpy arrays can be easyly converted
in to Tensorflow Variables.

Next we specify the Tensorflow variables we want to use. In this case we create one weight and one bias variable. For the
initial values of W and b we use helperfunction, which create a numpy array for us.::

    W = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
    b = tf.Variable(tf.zeros([1]))

Next we specify the computation Tensorflow should perform. But this listing of commands isn't executed yet. We are only
building a computation graph. Later on Tensorflow optimizes the graph and compiles it in a C language for maximum efficiency.::

    y = W * x_data + b

The variable y defines the prediction of the network. To correct the prediction we use an build in optimizer. Which minimizes our
error.::

    loss = tf.reduce_mean(tf.square(y - y_data))
    optimizer = tf.train.GradientDescentOptimizer(0.5)
    train = optimizer.minimize(loss)

Now that our computation graph is complete we let Tensorflow run it. First we initialize our Variables.::

    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)

The session is an abstract object which helps us managing our computations. With sess.run(init) the init node is run.
Within this session our variables are initialized.

In a simple for loop we now can run our training-graph.::

    for step in range(201):
        sess.run(train)
        if step % 20 == 0:
            print(step, sess.run(W), sess.run(b))

Like the sess.run(train) the sess.run(W) evaluates the W variable and returns a numpy array which represents the values saved in
W.
During the training the variables learn to fit the values W: [0.1], b: [0.3].

Further reading
---------------

For a more in depth tutorial about Tensorflow you can check out the mnist turial for `beginner <https://www.tensorflow.org/tutorials/mnist/beginners/>`_
and for `experts <https://www.tensorflow.org/tutorials/mnist/pros/>`_.

`Tensorflow Mechanics 101 <https://www.tensorflow.org/tutorials/mnist/tf/>`_ presents you additional features of Tensorflow.


Tensorboard
-----------
