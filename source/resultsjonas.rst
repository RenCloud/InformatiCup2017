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



The graphical interface change with the development and rise to a good looking basic interface.
At the begin the interface should have basic control. This means you can start an training without option, select an file with Github repository links, and start the classify process.
Because of the smaller size of the button and to show the user more information 2 option were possible: tooltip and statusbar. 
For our application we decided statusbar is the better option.
Also to get more control over the training, 2 checkboxes were added.

.. image :: firstgui.png

The login button came with the OAuth2 feature. This was a must to get enough request for more than one or two repositorys.
Problem here, after the classify there was no more place to show the solution.
To get more place and make a seperation between Classify, Solution and Training tabs was the choosen thing.
This also create the possibility to add the function that the user can add his own repositorys after login and make a table for the solution.
At this time the login function get the feature to open the loginlink direct within the browser so the user must not copy and open it on his own.

.. image :: secondgui.png

This interface look mutch times better than the first, has more function, but get not mutch complexity.
Now a bit optimation and better looking is the task.
At the moment the Solution tab must open by the user and this is only after the full classify task possible.
To make this better the tab is automcaticly choosen at the begin of the classify process.
Thats is a bit better, but because of singlethread application the interface/table is only refresht after the process.
Only the explicity call to refresh the window, after a new item is added, was here a help to make a responable application.



.. image :: thirdgui.png

The most user wants an interface which is resize able. 
Our is have this possibility not at the moment.
To get at least a resize able interface when the user is change the width, every position and size of an control object(button, textfield,...) is calculated every time new when the size change.
At the and the training tab get more features. Now you can/you have to choose 2 directorys and 5 file/s so the output path and trainings data and more can specified.

Fetch data
----------

The Fetch part is also run throw different steps.
Started had it with the c# application which use Octokit.Net as API wrapper to do the calls and create Json trainingfiles.
This project is within the 'GetData' directory.
At the beginning, this means after the point a workable example with the wrapper was found and a basic ASP.Net/c# server application is written,
the application has one task.
The task was:

1. Check state -> this means which is the id of the last fetched data ? or do we start new ? 1 - xxxx...
2. Have we an id list of public repositorys after this id ? 
2.1 When not make an HTTP Request ( without the Wrapper, because this function was a bug... so it fetch all data and make uncount able requests) to the API and get an list of public repositorys id's
3. Load the data we need from different parts of the API -> 6 different API endpoints were called to get all data some of them multiple to get more data
4. create a json document from the data

One run throw these steps mean we have 100 id's and data to these.
A neural network need alot more of them.
And to get this amount of data it need hours of time.
5000 api calls is possible when your application is connected with OAuth2.
A set of 100 id's need around 600-700 requests.
This means 700 id's and ~4200-4900 request within an hour it can fire.

At the end we fetch 31.7k id's( from 1 up to ~110.000 so nearly every 3 is an public and not deleted repository).
To get this amount it need a minimum of 46 hours.
Also around 15 clicks per run(700id's) -> 690 clicks within the server application.
Why this? Because it is a local server it has to start nearly every hour new, login in Github and than fetch 700 id's.
For this it needs around 20 minutes and every few minutes a new click was need to start a new fetch process(100 id's).

Later it gains a new feature. At the moment it only can take this list with 100 id's to fetch data.
The new added feature makes the possibility to create a list with id's by hand and fetch data from them.
This feature is used to get the trainingsdata with given solution.

Then the C# project become deprecaded, becouse the wrapper has no net.core support at the moment.
So the application is only useable on windows, but we want an cross-platform applcation.

To get this part more to the rest of the rest of the project and the cross-platform feature 
it was rewritten in python.
For python at the moment is there no given officel api wrapper.
Only unofficel wrapper. Problem of these? There are not very nice to use and very short described.
When you have less knowings about python and read a 2 line sample of an libary you don't know how this will work.
Than a more easyer and with the possibility of OAuth2 solution with 'Requests' was found.

With this libary it is easy and understandable to get data from the Request API.
So know it was possible to rewrite the fetch part into pure python.
The Fetch Results first was a valid, but failure json file which was not usable for us. 
Because the pregenerated json from the c# project was a bit different.
To make not big changes on the dataprepered part with lot of work the json create routine was changed.
Befour it use the standart json.dumps function within python and create with smaller peaces of json a big one.
This is a valid json, but not one we want.
So a part is created by hand with for loop and string building.
At the end a part json ist sill created over python json and must modify after that or is create befour by hand.

Then small errors like 403 response or other and 404 files have killed the script.
These errors create not initialized varibles or wrong initialized.
With if and try functionality and preinitializion tis problem was going.

What on least? It's only fetch up to 100 commits, issue, comments, because of the api request only send 100 in one message back.
The traindata wich was generated befour has the possibility of 1000 of them.
With a wrapper like the Octokit.net it is easy to get the 1000, because of implemented Pagination feature.
The normal requests return header contains an 'next' filed ('link' is the field, but it contains next and last page links).
These field is used for Pagination.
To get more as 100 commits a basic Pagination up to 10 sites are implemented.


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

