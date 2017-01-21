Results
=======

Result here described is of the Gui and fetch part only.

So what we want as gui is a simple to use interface with the needed functionality, but for the moment not overloaded.
The fetch part has to create valid JSON files and request them with oAuth.


Gui
---
The Gui run throw different size steps.
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

