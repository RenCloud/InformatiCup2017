Results
=======

In this section we will describe the development of our GUI and the changes we made to the datafetching process.




Userinterface
-------------

**********************************

Was möchtest du in dieser Sektion genau machen.
Ist das eine Beschreibung des Fensters oder willst du die Fortschritt bei der Entwicklung des Fensters beschreiben?

Ich wäre dafür du gehts einmal über die Änderungen drüber die du mit der Zeit gemach hast und warum

***********************************



The Gui run threw different size steps.
First we have a on Tab gui with a few buttons and an textfield for path selecting

.. image :: firstgui.png

The Gui need a bit more fency and function so it get tabs. 3 of them a table and a login posibility in github

.. image :: secondgui.png

May the user whants a bigger gui so know he can make it a bit bigger

.. image :: thirdgui.png

So at the end the user have 3 tabs: 1 to pick a file and clasify the repositorys within the file and have the posibility to login in github and add his own repositorys,
2 is the solution tab on that the solution will present,
and 3 tab the trainings tab to start training with different parameters.
Also the gui is possible to grow in the width.

Fetch data
----------
The Fetch Results first was a valid but failure json file which was not usable for us. 
Also small errors like 403 response or other and 404 files have killed the script.
After generate a part of the json without the help of json.dumps we have a valid useable json file.
And failure response are excepted or other handled.
What on least? It's only fetch up to 100 commits, issue, comments becouse of the api request only send back 100.
The traindata contains up to 1000 so this should be the same.
With the header response which contains the maximum number of sites the script gains the feature to get up to 1000 commits...


******************************************

But before we have the python part to fetch data and to get the train data the code in C# within GetData directory is used.
With the help of the offical Octokit.net Api wrapper and an basic ASP.Net Local Server we fetch data of 31.700 id's from github (from 1 up to ~110.000).
Why only 31k in this big range? Only public repositorys are within the 31k.
Also a second nearly the same code is used as a new page to fetch the trainingsdata with given solution.

Then the C# project is deprecaded, becouse the wrapper has to net.core support at the moment.
So the application is only useable on windows but we want an cross-platform applcation.


Vill kannst du diesen Block da noch einbauen und noch mit hinschreiben das man ja mehrere Anfragen brauchte um alle benötigten Daten zu bekommen.
Vill kannst du noch was zur automatisierung des datafetch Prozesses sagen, denn du hast das ja alles per hand gemacht also das programm regelmäßig gestartet
und durchlaufen lassen?!


*********************************************

