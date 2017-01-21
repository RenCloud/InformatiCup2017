Fetch data and GUI mechanism
============================

Basic Structure
---------------

The GUI and the data fetching are devided into two file: :file:`getJsonwithoauth` and :file:`Gui`.



*********************************************************

Diesen Teil habe ich rausgenommen weil er hier nicht hin passt. Man kann ihn  viel besser in dem Resultsfile verwenden.

But before we have the python part to fetch data and to get the train data the code in C# within GetData directory is used.
With the help of the offical Octokit.net Api wrapper and an basic ASP.Net Local Server we fetch data of 31.700 id's from github (from 1 up to ~110.000).
Why only 31k in this big range? Only public repositorys are within the 31k.
Also a second nearly the same code is used as a new page to fetch the trainingsdata with given solution.

Then the C# project is deprecaded, becouse the wrapper has to net.core support at the moment.
So the application is only useable on windows but we want an cross-platform applcation.

***********************************************************


Fetch Data
----------

To fetch the data we have decided befour what we need: readme, file typ, issues, comments, commits, author login and a few more we choose later do not use them.
For almost every information was an extra request necessary. So the requested directorys look as followed: ::

   /repos/:owner/:repo/git/trees/:sha?recursive=1       # to get file data
   /repos/:owner/:repo/issues                           # to get issue data
   /repositories                                        # to get ID of public repositorys
   /repos/:owner/:repo/languages                        # to get the main language of an repository
   /repos/:owner/:repo/comments                         # to get the commit comments
   /repos/:owner/:repo/commits                          # to get the commits

A call to the GitHub API can be seen as a standard HTML request. The API handles the input and responds to the user with a JSON string.
The API has some advanced features, because it is possible to use PUT, POST and Delete.

When you aren't registered you can only request 60 times per hour. If you are above this limit you don't get any responds back
from the GitHub API. To get more you have to use Basic Authentication or use oAtuh which we would recommend.


*********************************

Das ist nicht wirklich was hier nich stehen sollte. Es ist gut das du einmal das Thema noch genauer erläuterst. Aber
was in diesem Kapitel eher geklärt werden sollte ist, was du für einen Programmaufbau hast. Zum Beispiel was ist deine Schnittstelle
, was erwartet sie für Argumente und was gibt sie zurück. Wie sie das tut hast du ja bereits mit den Bibliotheken erläutert und wer
es genauer wissen will soll sich deinen Code ansehen.

Präsentier vill noch ein paar Codestücke aus deinem Code. Wenn er zu viel und zu komplex wird dann nimmst du alles unnötige raus

und schreibst stattdessen:

# ...
oder
# Hier würde die Verbindung zum server stehen
oder
# initialisierung der Variablen

Dann machst du die Prüfer direkt mit deinem Code vertraut und sie können sich besser zurecht finden und können deine Gedankengänge
besser nachvollziehen.

Beschränke dich auf das wesentlich und schreib nicht zu viel :-P


Das was da unten noch in diesem unterkapitel steht wieder holt nur das was du schon erzählt hast. Ich glaube nicht das das noch darin verbleiben sollte.

***********************************

OAuth2 is an Authorization Flow for webapplication (and other ). It's make it easy to control which application is connected.
Every application gets an client id and secret which this an application is registert at the server. 
When a user use it the application contact the server with his id and secret. Than the user have to log in. Than the application gets an token from the server.
This token is the OAuth2 token which is used to validate that is this application and this user.
Thats only a very basic overview for the github oAuth2 implementation not every use id and secret or other parts. 
To read more about this technic: `OAuth2 <https://oauth.net/2/>`_.

************************************

GUI
---

The GUI is build with PyQt5. PyQt5 is based on Qt which is a cross-plattform libary in C++.
It is accessible with many high-level APIs for modern desktop and mobile system development.
PyQt5 is a comprehensive set of Python bindings for Qt v5. Not all parts are completly implements but 35 are. Enough to build our functioning GUI.
Qt has powerfull features to make nice graphical interfaces which can run on different platforms.
More Information about `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/download5>`_.

**************************************
Hier nochmal wie deine Schnittstellen und Teile deines Codes besprechen (s.o.).

**************************************
