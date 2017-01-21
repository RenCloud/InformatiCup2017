Fetch data and GUI mechanism
============================

Basic Structure
---------------

To handle such a complexe task we split the project in three parts. Every one of use got one of them.
    #. Data Fetching, GUI and handling of the GitHub API
    #. Datapreparation
    #. Neural Networks ( The learning part)

The Data Fetching and Gui part has mostly two files: Gui and getJsonwithoauth.
Like the name saying gui is in gui and the fetch part in getJsonwithoauth.

But before we have the python part to fetch data and to get the train data the code in C# within GetData directory is used.
With the help of the offical Octokit.net Api wrapper and an basic ASP.Net Local Server we fetch data of 31.700 id's from github (from 1 up to ~110.000).
Why only 31k in this big range? Only public repositorys are within the 31k. 
Also a second nearly the same code is used as a new page to fetch the trainingsdata with given solution.

Then the C# project is deprecaded, becouse the wrapper has to net.core support at the moment.
So the application is only useable on windows but we want an cross-platform applcation.


Fetch Data
----------

To fetch the data we have decided befour what we need: readme, file typ, issues, comments, commits, author login and a few more we choose later do not use them.
A bit mad is that nearly each data part needs an own API requests. 
So we must do requests on ::

   /repos/:owner/:repo/git/trees/:sha?recursive=1       # to get file data
   /repos/:owner/:repo/issues                           # to get issue data
   /repositories                                        # to get ID of public repositorys
   /repos/:owner/:repo/languages                        # to get the main language of an repository
   /repos/:owner/:repo/comments                         # to get the commit comments
   /repos/:owner/:repo/commits                          # to get the commits

But what is an request? The Github API is and standart request API. You send a get to the specified point of the api and get back the data in JSON format.
But also Post, Put and Delete message are possible.

When you use it normal ex. with ure browser u have 60 request within 1 hour. When you make more you get no data back.
To get more you have to use Basic Authentication, this is not so great, or use oAtuh which is a lot better.

OAuth2 is an Authorization Flow for webapplication (and other ). It's make it easy to control which application is connected.
Every application gets an client id and secret which this an application is registert at the server. 
When a user use it the application contact the server with his id and secret. Than the user have to log in. Than the application gets an token from the server.
This token is the OAuth2 token which is used to validate that is this application and this user.
Thats only a very basic overview for the github oAuth2 implementation not every use id and secret or other parts. 
To read more about this technic: `OAuth2 <https://oauth.net/2/>`_.


GUI
---

The gui is build up with PyQt5. PyQt5 work on Qt which is an cross-plattform libary in C++ that implement high-level APIs for accessing many aspects of modern desktop and mobile systems.
PyQt5 is a comprehensive set of Python bindings for Qt v5. Not all parts are completly implements but more than 35 are implemented.
Qt have powerfull features to make nice graficall interfaces which run on different platforms. 
More Information about `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/download5>`_.
