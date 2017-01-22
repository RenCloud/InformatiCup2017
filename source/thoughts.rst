What could be used furthermore?
===============================
Length of arrays
----------------

*************************************

Because of text mining not working properly, we wanted to filter some values which can be converted much easier into numerical
representations. While searching for such values, the length of some array-based values seemed to be useful in order to analyze
the repository. In our repository data the commits, comments, files/folders and issues consist of arrays, which length we
can extract and easily convert to the needed input vector for the learning network. We only had to normalize (number between 0 and 1)
them by the length dividing the maximum length(which is 1000 per array, larger arrays would be truncated).

**************************************************

Hier hast du doch noch nicht die neusten Entwicklungen eingebaut oder? Wir haben das dann doch mit den mit file normalisieren sein lassen?!

Hier wäre es cool wenn du noch die Idee mit den gefilterten Wörter die 1000 mal vorkommen und nur in 70% der repos enthalten sind benutzt.
Und noch die gleiche liste mit den Dateiendungen. Um noch ein paar alternativen und versuche aufzuzeigen.

**************************************************


Conclusion
----------
With this approach we increased our accuracy up to 30%, which is 150% of the text-mining accuracy.
Increasing the accuracy any further won't be possible without using much more computing power.
With enough performance you can store and analyze the textual values better, which should be the
main part in this analysis. Only storing single words isn't enough, you have to analyze the context, too.
Having some side values (here the length of arrays) is helpful too, but they cannot classify repositories with enough precision.

*********************************************************

Sag hier vill noch was man an zusätzlichen informationen genau gebraucht hätte.
Auch zum Beispiel: Was wäre wenn wir mehr werte in dem JSON string gehabt hätten.
Hätte man vill leere directorys filtern sollen.
Vill was für tools gibt es um diesen Kontext in die Codierung mit einbaut auch wenn das vill unbegrenzt viel speicher gebraucht hätte.


**********************************************************
