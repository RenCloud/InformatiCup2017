Interfaces
==========

Data preparation
----------------
Besides gensim, we only used one python script for all kind of tasks. This was possible, because of all of them have huge similarities. ::

  def prep(file, training = 0):
  ...
  return json_out_raw_arr

This script gets two parameters. A file containing an json representation of the repository data. And an mode which seperates the different usages of this script. There are four differnet modes:
- 0: Produces vectors to train or learning network by given files
- 1: Adds the current file to all Text Mining dictionaries
- 2: Prepares an vector for classifiying
- 3: Tries to remove as many unnecessary values in the dictionaries as possible

In mode 0 and 2 the script returns a vector, which will be used in our vector.
In mode 1 and 3 the script do not have to return anything.

To control all of this modes and retrieve or send values to adjacent modules, we had to write a short script handling everything.

Server
------
Our server script provides two different methods, that can be run using the gui.
At first: The training::

  def training(data, newDataset = False, valid = True, svtD=None, svtR = None, vsD = None, vsR = None)

The parameters are

data
  training data without prior classification
valid
  Are control values given?
svtD
  json files of training data with prior classification
svtR
  classification of svtD
vsD
  json files of an control set
vsR
  clasification of control set

The gui only takes (multiple) files as input and dynamically generates the parameter values

As second: Classification::
  def classify(json_str)

This method only gets the data of the chosen url as json, forms it into an vector and classifys it. The classification is being return as an 7-tuple to the gui.


The server also provides an console edition of the gui for manual testing. For using it, just uncomment the bottom section of the server file.
Not all functions might be supported.
