.. Gi-Projekt documentation master file, created by
   sphinx-quickstart on Wed Jan  4 15:24:15 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome To Our Documentation Page
=================================

The task was to write a software which can automatically classify a GitHub repository in one of the seven following classes:

#. Development
#. Homework
#. Education
#. Documentation
#. Websites
#. Data
#. Other

Further information about the contest can be found on `informaticup.gi.de <http://informaticup.gi.de/fileadmin/redaktion/InformatiCup2017.pdf>`_
or `github <https://informaticup.github.io/InformatiCup2017/>`_.

The task could be solved in many different ways. We decided to use Deep Neural Network. It is complex but a capable problem solver
for task with much available data. That is also their biggest weakness: They need many datasets to work properly.

Because there doesn't exist any labeled data on this task we decided to start with unsupervised training. We stacked multiple
so called restricted Boltzmann machines on top of each other and performed greedy layer wise training.

After this we can train the so build network with our hand-classified dataset.
As values for our input vector we used the comments, commits, open issues, closed issues, users who commented and users who commited.
Our unlabeled trainingset has a size of 31700 and the labeled dataset 308.

We decided to divide the project into three main modules. Every module has its specific task.
The :ref:`first module <first-label>` handles the user input and manages the data download and was also used to download our datasets.
The :ref:`second module <second-label>` extracts the information out of the raw data. The :ref:`third modul <third_label>` uses it to train the model und hands the
results back to the userinterface.

The documentation is divided into these three modules. Each Section explains one section.

.. _first-label:

Userinterface and data management
---------------------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   introductionjonas
   explanationjonas
   resultsjonas
   CodeJonas


.. _second-label:

Datapreparation
---------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   why
   textMining
   efficency
   thoughts

.. _third_label:

Training and predictions
------------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   explanation
   results
   code



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
