Why is Datapreparation necessary?
=================================


The machine learning network, which we used, requires a normalized vector, tp prevent the values from being too big or small.
The vector hasn't any length requirements, though its values have to be exclusively numerical.
The repository data of GitHub needs to be converted into numerical values to be useful. It is also the task of this module to
filter the data and use only the useful information.


The Github data
---------------
.. image:: singleValues.png

The first part of the GitHub data are mainly unique values, such as the repository id or the repository name.
 Except for the author name these data won't have much information, so we can ignore them.


.. image:: codeValues.png

The second part covers code-specific values, which are way more interesting. The language part is still irrelevant,
as it stores only information about code-based projects. The file and tree information however can be extracted and used for analyzing folder names or file extensions.

.. image:: repoValues.png

This is the most important part of our data. Here we can see everything, that is related to the repository itself,
such as its commits or issues. These will be core for analyzing the data.


All the data we want to analyze share one problem. All of them are text-based and not numerical values, which we need.
The textual values in the repositories therefore needs to be converted into numerical ones in order to fit the learning network.
This is the purpose of the module named data preparation. Data preparation gets object representations of git repositories
and returns numerical vectors which represent the textual values in an unique way.

How does the conversion work in general?
----------------------------------------
The conversion can cause many different problems. The most obvious way would be to assign an id to every word that is
used in any of the repositories. With this ids every word can be saved together with its neighbours, so this group of ids
would result in an context for the specific word. This solution would be extremely inefficient and also extremely inaccurate.
Either the words occur in many program documents, so they don't help us to identify the type or they are so specific
 that they don't occur often enough in the same context to come to an occlusion based on them.
