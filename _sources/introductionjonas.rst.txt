Get Started: Request and PyQt5
==============================

Installation
------------

The userinterface is built with `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/intro>`_.
We use `Requests: HTTP for Humans <http://docs.python-requests.org/en/master/>`_ and requests_oAuthlib to fetch the required data
from GitHub.
The requirements for this part of the project are easily installed via pip:
::

    pip install requests

::

    pip install requests_oauthlib

::

    pip install PyQt5


Basic: Requests and Requests_oAtuhLib
-------------------------------------

Both libraries are very easy to use. We will show you some examples on how to use them so you have a better understanding of our code.

First we import the needed modules as followed: ::

    import requests  # for the Standart HTTP Requests
    from requests_oauthlib import OAuth2Session # for the OAuth lib which we need later for OAuth 2 support
    import json

To send a basic webpage request we use the :meth:`get` function.::
    
    r = requests.get('https://api.GitHub.com/events')

The sever responds is now saved in our r variable.

To view its content we use the python :meth:`print` functionality::

    print(r.text)

From the GitHub API we get a JSON string back. We can easily convert the responds into a JSON string. ::

    jsonobject = json.loads(r.text or r.content)

To get fewer problems while handling GitHub requests a simple if-construction helps. ::

    if r.ok: # is ok when request is ok -> when you hit ratelimit it's not ok
        print(r.text)

The :mod:`request` can be used for more advanced tasks. The links for more information are
`here <http://docs.python-requests.org/en/master/user/quickstart/>`_ and `here <http://docs.python-requests.org/en/master/user/advanced/>`_.

The next step is to use the :mod:`OAuth2Session`.
First we create two variables which hold our userinformation. ::

    # Credentials you get from registering a new application
    client_id = 'Your Client ID'
    client_secret = 'Your Client Secret'

If you want to register your own application follow this link `here <https://GitHub.com/settings/applications/new>`_.
Let's create some more variables with needed information::

    # OAuth endpoints given in the GitHub API documentation
    authorization_base_url = 'https://GitHub.com/login/oauth/authorize'
    token_url = 'https://GitHub.com/login/oauth/access_token'

Now we have nearly all what we need ::

     GitHub = OAuth2Session(client_id)
     # Redirect user to GitHub for authorization
     authorization_url, state = GitHub.authorization_url(authorization_base_url)
     print ('Please go here and authorize,', authorization_url)
     # Get the authorization verifier code from the callback url
     redirect_response = raw_input('Paste the full redirect URL here:')
     # Fetch the access token
     GitHub.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

With the GitHub object you can do request with oauth.
Simple do the same as you did before only this time with the GitHub object instead of :meth:`requests` ::

    r = GitHub.get('https://api.GitHub.com/user')

For more look `here <http://requests-oauthlib.readthedocs.io/en/latest/index.html>`_.


Basics: PyQt5
-------------

Within the project we need 13 imports from PyQt for different objects like Buttons, TextFields and more.
In this section we give you nice insight into the methods we used in our code.
Here we only show a basic window with a button and a tooltip.

Our imports are: ::

    import sys
    from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
    from PyQt5.QtGui import QFont  

Next we create a main for our window: ::

    if __name__ == '__main__':
    
        app = QApplication(sys.argv)
        ex = Example()
        sys.exit(app.exec_())

The variable is our class which we use to create our window.
That's what the class will look like::

    class Example(QWidget):
        
        def __init__(self):
            super().__init__()
            
            self.initUI()

This is the basic init structure for a QWidget.
The only part which is missing is 'initUI'.
Lets's implement it:
::

    def initUI(self):
        # set the font for buttons, texts and the window
        QToolTip.setFont(QFont('SansSerif', 10))

        # Creates the tooltip for our window
        self.setToolTip('This is a <b>QWidget</b> widget')

        # creates a button
        btn = QPushButton('Button', self)

        # Creates the tooltip for our button
        btn.setToolTip('This is a <b>QPushButton</b> widget')

        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')

        # this call is needed otherwise the window won't show up
        self.show()



Our Program now looks like this:

.. image:: tooltips.png

For more details you may look `here <http://zetcode.com/gui/pyqt5/>`_ for a good basic tutorial about PyQt5.
