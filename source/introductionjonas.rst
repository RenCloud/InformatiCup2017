Get Started Request and PyQt5
=============================

Installation
------------
The Gui and the Data Fetch (the python part, we also have a ASP.Net C# version of it) use `Requests: HTTP for Humans <http://docs.python-requests.org/en/master/>`_ for fetching the Gihub API data with requests_oAuthlib, `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/intro>`_
for the Graphical Interface and python 3.5 as language.

Both can installed via pip: pip install requests/requests_oauthlib/PyQt5.


Basic usage of Requests/Requests_oAtuhLib
-----------------------------------------

Both libarys are very easy to use and make with small kind of code manny tasks.

To import Requests and make HTTP Request (which we need to do GitHub API request to fetch data) we need first ::

    import requests  # for the Standart HTTP Requests
    from requests_oauthlib import OAuth2Session # for the OAuth lib which we need later for OAuth 2 support 

To create a basic request ex. to get a webpage ::
    
    r = requests.get('https://api.github.com/events')

The server response, the whole like headers, content and more, is within the r object.

To view the content this line is all what you need ::

    print(r.text)

For the githubapi we get a JSON string back we can easily make an python object from it with the standart json lib within python ::

    # don't forget to import json
    jsonobject = json.loads(r.text or r.content)

To run in less problems while doing github requests a simple if construction helps ;;

    if r.ok: # is ok when request is ok -> when you hit ratelimit it's not ok
        print(r.text)

The Requests Lib can make mutch more like Post requests, working with Vert Verification and more which you can read `here <http://docs.python-requests.org/en/master/user/quickstart/>`_ and `here <http://docs.python-requests.org/en/master/user/advanced/>`_.

For the OAuth know we use the Requests_oAtuhLib we import at the begin.
For Github we have a client_id and a client_secret ::

    # Credentials you get from registering a new application
    client_id = 'Your Client ID'
    client_secret = 'Your Client Secret'

You get this `here <https://github.com/settings/applications/new>`_.
Also we need the URL, 2 of them ::

    # OAuth endpoints given in the GitHub API documentation
    authorization_base_url = 'https://github.com/login/oauth/authorize'
    token_url = 'https://github.com/login/oauth/access_token'

Now we have nearly all what we need ::

     github = OAuth2Session(client_id)
     # Redirect user to GitHub for authorization
     authorization_url, state = github.authorization_url(authorization_base_url)
     print ('Please go here and authorize,', authorization_url)
     # Get the authorization verifier code from the callback url
     redirect_response = raw_input('Paste the full redirect URL here:')
     # Fetch the access token
     github.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

With the github object you can make request with oauth.
Simple make the same like above only with github and not with requests ::

    r = github.get('https://api.github.com/user')

For more look `here <http://requests-oauthlib.readthedocs.io/en/latest/index.html>`_.


Basic use of PyQt5
------------------

So for PyQt it's not so easy to make a basic view.
Within the project we need 13 Imports from PyQt for different objects like Buttons, TextFields and more.
Here we only show a basic window with a button and a tooltip.

For this we need as import ::

    import sys
    from PyQt5.QtWidgets import (QWidget, QToolTip, 
         QPushButton, QApplication)
    from PyQt5.QtGui import QFont  

That's alot for such a bit but we need all of them. 
Next we create a main for our window ::

    if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

Like you see we start an Example() wich we write now ::

    class Example(QWidget):
        
        def __init__(self):
            super().__init__()
            
            self.initUI()

This is the basic init structure for a QWidget.
The only part which is missing 'initUI' ::           
            
   def initUI(self):
        
        QToolTip.setFont(QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)       
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')    
        self.show()

May the line are self desciptive i say one two words to them.

At the beginn QToolTip.setFont is easy -> it sets the font of the Window and of the parts of the window, buttons and so on.
self.setToolTip creats a small box under the cursur when it's over the window.
Same with btn.setToolTip.

The last line is important -> self.show() without this line you want see the window and wait and nothing happen.
When all of the code is correct and you make all things correct you see something like that 

.. image ::tooltips.png

For more and more detailed you may look `here <http://zetcode.com/gui/pyqt5/>`_ for a good basic of PyQt5.
