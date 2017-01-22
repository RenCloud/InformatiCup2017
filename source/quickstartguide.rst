

Quickstart Guide
================

In our quickstart guide we briefly describe how our program can be used.
For further information read our :doc:`documentation <index>`.

Table of content:

#. :ref:`Requirements <req>`
#. :ref:`Start the program <start>`
#. :ref:`Train a network <train>`
#. :ref:`Classify a repository <classify>`

.. _req:

Requirements
------------

#. numpy
#. tensorflow
#. gensim
#. PyQt5
#. requests_oauthlib
#. requests

.. _start:

Start the program
-----------------

With our console navigate into our project directory.
Then start the userinterface with the following command:

::

    python3 gui.py


.. _train:

Use the program to train a neural network
-----------------------------------------

When you started the program a GUI will show.
Click on the tab training. Then select the appropriate files and directories to run the training.

Pick the listed files and directories in the same order as shown here:

#. Unclassified training data: (Choose multiple file) Every File in the data/json directory.
#. Main directory of the network: Take a directory of your choice.
#. Sub directory of the network: Take a directory of your choice.
#. Validationset data: Select the file validationData.json.
#. Validation data labels: Select the file validationDataLabels.json.
#. Supervised trainset data: Select every file in tagged/data.
#. Supervised trainset labels: Select every file in tagged/labels.


.. _classify:

Use the program to classify a repository of your choice
-------------------------------------------------------

If you want to classify a repository start the program follow these steps.

#. Create a file with all repository URLs you want to classify. For each repository use just one line.

#. Click the button 'login to GitHub'.

#. The browser will open GitHub automatically. Log in.

#. The URL in your browser will change. Copy the new URL.

#. Click the 'login' button of our GUI.

#. Then click the button 'classify repositories'

#. Wait till the program finishes working then see the results in the results tab.