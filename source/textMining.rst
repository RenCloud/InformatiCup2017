First approach: Text Mining
===========================

We wanted instead to make use of the characteristics of decising words, which have an high impact in classifying repositories. These decisive words often dont need any context. Only the appearance of any of this words in an document can give us a hint on classifying the document. So we decided to only store one id for every word and dont store the context with it, as it would produce high additional costs while only giving low benefits.

Increasing performance
----------------------
In addition to only saving one id per word, we wanted to focus on increasing our efficency further. We did this by declaring a huge amount of words as unimportant. At first we cutted off all words with the least and the most frequency in our document sample. Expecially the words with high frquency rarely have impact on the classification. We ignored about 20 percent of the most frequent words and about .3 percent of the least frequent words. As a second we let our machine learning network learn to classify an repository using the rest of the word ids as elements for the output vector. After learning quite a while we could see which words influenced the outcome most, and – more important -  which influenced the outcome least. This words could be deleted to gain an massive increase in efficiency while only losing little accuracy.
