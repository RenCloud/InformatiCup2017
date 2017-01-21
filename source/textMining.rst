First approach: Text Mining
===========================

When we first started the project we tried to find the information needed to classifiy a repository. As a human we would
just look at the readme or the description file to get an idea what this repository is all about.

That's why our first approach was to convert the readme and description file into one vector which the network then would learn.

To thin out the amount of words to save we tried to find decising words, which have an high impact in classifying repositories.
These decisive words often don't need any context. Only the appearance of any of this words in an document can give us a hint on
classifying the document. So we decided to only store one id for every word and don't store the context with it, as it would
produce high additional costs while only giving low benefits.

Increasing performance
----------------------
In addition to only saving one id per word, we wanted to focus on increasing our efficency further.
We did this by declaring a huge amount of words as unimportant. At first we cutted off all words with the least
and the most frequency in our document sample. Expecially the words with high frquency rarely have impact on the classification.
We ignored about 20 percent of the most frequent words and about .3 percent of the least frequent words.
As a second we let our machine learning network learn to classify an repository using the rest of the word ids as elements
for the output vector. After learning quite a while we could see which words influenced the outcome most, and – more important -
which influenced the outcome least. This words could be deleted to gain an massive increase in efficiency while only losing little accuracy.


*************************************************

Es wäre gut wenn du noch beschreibst wie du dises Textmining performst und was du für bibliotheken benutzt
vill gibst du noch einen kurzen ausgewählten Einblick in deinen Code das die Prüfer sich besser zurecht finden
Gut wäre auch wenn du die Schnittstellen deine Software erläuterst und begründest warum die so gewählt worden ist von dir

Ich und Jonas haben auch noch kurz unsere Bibliotheken vogestellt die wir verwendet haben

Vill kannst du dich an unserem Aufbau orientieren, dann sind wir einheitlichen :-).

**************************************************