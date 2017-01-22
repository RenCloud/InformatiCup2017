First approach: Text Mining
===========================

When we first started the project we tried to find the information needed to classify a repository. As a human we would
just look at the readme or the description file to get an idea what this repository is all about.

That's why our first approach was to convert the readme and description file into one vector which the network then would use to learn.

To thin out the amount of words to save we tried to find decisive words, which have an high impact in classifying repositories.
These decisive words often don't need any context. Only the appearance of any of this words in a document can give us a hint on
classification of the document. So we decided to only store one id for every word and don't store the context with it, as it would
produce high additional costs while only giving low benefits.

Gensim
------
To keep track of all these decisive words, we used the Python library "Gensim". Gensim can be installed using pip install and provides an interace for storing words of documents with their frquency in documents as well as the documents itself. It is designed for searching for similarities in multiple documents, which could maybe be used in our project too.

We started with storing values in Gensims "Dictionary". This is mapping between words an their unique ids with an extra storage for the  frequency of this words. To create a large dictionary, we iterated over our trainingset of repository data and stored at first every word we found. After this was done we started filtering out words that cant be useful for classifying repositories based on their frequency in our repositories. This increased our performance by an huge amount. Prior to deleting we had an list of ~40000 unique words. After cutting off both extremes we had ~1600 left.

Increasing performance
----------------------
In addition to only saving one id per word, we wanted to focus on increasing our efficency further.
Words, which are in nearly every repository as well as words, which are in only few of our about 30.000 repositories, wont give us any information about the repository. Gensims dictionary offers an method for filtering both extremes. We decided to delete every word that is found in under 30 repositories(0.1% of our trainingset) or in above 70%(21.000) of our repositories.
As a second we let our machine learning network learn to classify an repository using the rest of the word ids as elements
for the output vector. After learning quite a while we could see which words influenced the outcome most, and – more important -
which influenced the outcome least. This words could be deleted to gain an massive increase in efficiency while only losing little accuracy.


Is Text Mining good for identifying repositories?
-------------------------------------------------
while testing this vector, our peak accuration of the learning network was only about 15% at most. So we decided to
focus more on the few numeric values existing in the data. Because we only got arrays of texts in the data,
the only numeric values we could get were the lengths of this arrays. While testing with a few values we already got
an improvement of accuracy to 20%. This isnt really great at all, but showed us, that we can get an tendency based off text mining.
But to increase our accuracy further, another approach was necessary.
