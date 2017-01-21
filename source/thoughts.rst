What could be used furthermore?
===============================
Length of arrays
----------------
Because of text mining not working properly, we wanted to filter some values which can be converted much easier into numerical representations. While searching for such values, the length of some array-based values seemed to be useful in order to analyze the repository. In our repository data the commits, comments, files/folders ans issues consists of array, which length we can extract and easily convert to the needed input vector for the learning network. We only had to normalize(number between 0 and 1) them by the length dividing the maximum length(which is 1000 per array, larger arrays would be truncated).

Conclusion
----------
With this approach we increased our accuracy up to 30%, which is 150% of the text-mining accuracy. Increasing the accuracy any further wont be possible without using much more computing power. With enough performance you can store and analyze the textual values better, which should be the main part in this analyzation. Only storing single words isnt enough, you have to analyze the context to. Having some side values(here the length of arrays)is being helpful too, but they cannot classify repositories wiht enough precision.
