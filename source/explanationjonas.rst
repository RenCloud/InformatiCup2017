Fetch data and GUI mechanism
============================

Basic Structure
---------------

The GUI and the data fetching are divided into two file: :file:`getJsonwithoauth` and :file:`Gui`.


Fetch Data
----------

To fetch the data we have decided in a first step what we need: readme, file typ, issues, comments, commits, author login and a few more.
For almost every information an extra request was necessary. So the requested directories look as followed: ::

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

OAuth2 is an Authorization Flow for webapplication (and other ). It's make it easy to control which application is connected.
Every application gets an client id and secret which this an application is registert at the server. 
When a user use it the application contact the server with his id and secret. Than the user have to log in. Than the application gets an token from the server.
This token is the OAuth2 token which is used to validate that is this application and this user.
Thats only a very basic overview for the github oAuth2 implementation not every use id and secret or other parts. 
To read more about this technic: `OAuth2 <https://oauth.net/2/>`_.


GUI
---

The GUI is build with PyQt5. PyQt5 is based on Qt which is a cross-plattform libary in C++.
It is accessible with many high-level APIs for modern desktop and mobile system development.
PyQt5 is a comprehensive set of Python bindings for Qt v5. Not all parts are completely implemented but 35 are. Enough to build our functioning GUI.
Qt has powerful features to make nice graphical interfaces which can run on different platforms.
More Information about `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/download5>`_.

