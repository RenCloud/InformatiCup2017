Fetch data and GUI mechanism
============================

Basic Structure
---------------

The GUI and the data fetching are divided into two file: :file:`getJsonwithoauth` and :file:`Gui`.



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

To call the the api nearly every time the same routine is done:
::

    # request the api here we call the tree api to get the git data 
    r = github.get('https://api.github.com/repos/' + owner + '/' + repos + '/git/trees/master?recursive=1')
    # if request ok
    if r.ok:
        # create object from JSON response this part is different in some points
        # because not overall we use the given json structure
        repoItemTree = json.loads(r.text or r.content)
    # is there a problem than only get data from repository ( it's may an empty one)
    else:
        r = github.get('https://api.github.com/repos/' + owner + '/' + repos)
        if r.ok:
        # see here is an empty one
            return json.dumps(json.loads(r.text or r.context))
        else:
        # somethins is wrong
            return None

The routine for commits, issue and comments is a big greater. It needs to add Pagination or something that do the same task.
::

     if r.ok:
        # CommitJson -> Object
        # get up to 1000 commits with the header that comes back from github api
        stringcommiter = ''
        try:
             # get header / try to get him ( when it's only 1 page this header wont exist
            headers = r.headers['link']
            # split header data in smaller parts
            test = headers.split(',')
            # get page part of an smaller part ( smaler part is nearly a link and from the end of the link i want the
            #  number)
            startIndex = test[1].find('&page=')
            # get the last to chars -> if we have 2-9 whe cut it
            # if we have 10-99 -> 10-99
            # if the number bigger we have 130 or something -> 13 so 13x the last number is not interestet
            # we can do this becouse we want only 10 and very number bigger 99 will give us 10 or an bigger number than
            end = test[1][startIndex + 6:startIndex + 6 + 2]
            if end[1] == '>':
                end = end[0]
            if int(end) < 10:
                # do the standart routine with changing link 'end' times
                repoItemCommits = json.loads(r.text or r.content)
                for i in range(2, int(end) + 1):
                    r = github.get(
                        'https://api.github.com/repos/' + owner + '/' + repos + '/commits?per_page=100&page=' + str(i))
                    repoItemCommits += json.loads(r.text or r.content)
            else:
                # when the size is bigger than 10 do it 10 times
                # ... standart routine like above 
        except:
            # when the header 'link' is not there it's only one page so we need no 
            # pagination and we can run standart routine without loop
            # ...


Commit it there a extra special case. At this point the json is create complete by hand.
::

     for i in repoItemCommits:
                    author = i['author']['login']
                    commiter = i['committer']['login']
                    stringcommiter += '{"author_login": "' + author + '","committer_login": "' + commiter + '"},'

The other parts use 
::

     infoJson = json.dumps(repoInfo)

But they need little changes.
Treedata was cut a part of the json and change the word tree to repository.
The other get her type presentation in front of the json like 
::

    commit -> '"commits":['+ stringcommits + ']'

At the end all json strings are combined in one big string
::

     finalReposItem = '[{' + infoJson + ',' + treeJson + ',' + readmeJson + ',' + languageJson + ',' + commitsJson + ',' + commentsJson + ',' + issueJson + '}]'


*********************************

Das ist nicht wirklich das was hier stehen sollte. Es ist gut das du einmal das Thema noch genauer erläuterst. Aber
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


Das was da unten noch in diesem unterkapitel steht wiederholt nur das, was du schon erzählt hast. Ich glaube nicht, dass das noch darin verbleiben sollte.

***********************************
Soll dieser Teil auch raus?
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
PyQt5 is a comprehensive set of Python bindings for Qt v5. Not all parts are completely implemented but 35 are. Enough to build our functioning GUI.
Qt has powerful features to make nice graphical interfaces which can run on different platforms.
More Information about `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/download5>`_.

Within our code we need not mutch of them, but often the same parts.
The interface is build with buttons, textfield(LineEdits), filepicker and a tableview.
::

    # objectwidth = 25
    # create a button on tab3
            self.btraining = QPushButton('Training', tab3)
            # when the cursor is move above the button show this text on the status bar
            self.btraining.setStatusTip('Start Training Mode')
            # resize button
            self.btraining.resize(self.btraining.sizeHint())
            # set his geometry ( xposition,yposition,xsize,ysize)
            self.btraining.setGeometry(50, 50, 75, objectwidth)
            # what happens when the button is clicked
            self.btraining.clicked.connect(self.btrainingclicked)

Like this button every button is create.
The Code for a LineEdit is a bit shorter.
::

       # create a 'textField'
        self.lepath = QLineEdit(tab1)
        # set his position and size
        self.lepath.setGeometry(50, 50, 300, objectwidth)
        # Whats happen when the cursur is moved over the LineEdit
        self.lepath.setStatusTip('Path to Repository Link List File')

The TableView is a bit complicated, but have not so mutch lines.
::

     # create an table view on tab2
        self.view = QTableView(tab2)  # declare table view
        self.view.setGeometry(0, 0, 495, 250) # set his position and size
        self.model = QStandardItemModel()  # declare model
        self.view.setModel(self.model)  # assign model to table view
         # create the header of the table
        item = QStandardItem('SolutionTable')
        # set header to the view
        self.model.setHorizontalHeaderLabels(['Link', 'Classsifiy'])
        # auto scroll
        self.view.setAutoScroll(True)
        # and a scroll bar when it has to mutch data
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # to set new data know we need
        # create new data
        item = QStandardItem(repositorys)
        # new row
        self.model.appendRow(item)
        itemRow = item.row()
        indexOfColumn1 = self.model.index(itemRow, 1)
        # add new data
        self.model.setData(indexOfColumn1, cat, 0)

To create the filepicker after a button is clicked a simple class can used.
::

      def showdialog(self):
        """
            user wants to pick a file so we open the file picker for him
        """

        # start filepicker at '/home' place
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

For the directory picker or the selected file picker only a small change is made.
::

    # for the directory
    fname = QFileDialog.getExistingDirectory(self, 'Select Directory', '/home')

    # for slected files ( multiple files)
    name = QFileDialog.getOpenFileNames(self, 'Select Files')
        nameString = ''
        for file in name[0]:
            print(file)
            





