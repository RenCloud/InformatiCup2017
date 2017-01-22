import json
import sys
import server

from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QFileDialog, QApplication)
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QWidget
from requests_oauthlib import OAuth2Session

from getJsonWithoAuth import getJson

# Credentials you get from registering a new application
client_id = 'a97b3ff30ea37904a570'
client_secret = 'aaf90eb8b87de2ca40c995f6ac55eec85f4c1170'

# OAuth endpoints given in the GitHub API documentation
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
objectwidth = 25


class Gui(QMainWindow):
    def __init__(self):
        """
            init ui
        """
        super().__init__()

        # create a Tab Layout
        self.tabs = QTabWidget(self)
        self.initui()

    def initui(self):
        """
            place object on window and set there geometry and reaction
        """

        # create a Status bar at the bottom of the window
        self.statusBar()

        # set tab size and position
        self.tabs.setGeometry(0, 0, 500, 380)

        # add 3 tabs to the tab layout
        tab1 = QWidget()
        tab1.setStatusTip('Set Classify Option and start it')
        self.tabs.addTab(tab1, 'Classify')

        tab2 = QWidget()
        tab2.setStatusTip('Solution of Classify')
        self.tabs.addTab(tab2, 'Solution')

        tab3 = QWidget()
        tab3.setStatusTip('Training option and start training')
        self.tabs.addTab(tab3, 'Training')

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

        # same like above
        self.bfiledialog = QPushButton('Pick File', tab1)
        self.bfiledialog.setStatusTip('Pick File with Repositorys Links')
        self.bfiledialog.resize(self.bfiledialog.sizeHint())
        self.bfiledialog.setGeometry(370, 50, 80, objectwidth)
        self.bfiledialog.clicked.connect(self.showdialog)

        # create a 'textField'
        self.lepath = QLineEdit(tab1)
        self.lepath.setGeometry(50, 50, 300, objectwidth)
        self.lepath.setStatusTip('Path to Repository Link List File')

        # create another button to classify repositorys
        self.btag = QPushButton('Classify Repositorys', tab1)
        self.btag.setStatusTip('Classify Repositorys from File')
        self.btag.resize(self.btag.sizeHint())
        self.btag.setGeometry(50, 90, 400, objectwidth)
        self.btag.clicked.connect(self.btagclicked)

        # add an TextField for Trainings Data
        self.letrainingpath = QLineEdit(tab3)
        self.letrainingpath.setGeometry(50, 80, 300, objectwidth)
        self.letrainingpath.setStatusTip('Set Trainings Data')

        # another button to set Path
        self.bshowTrain = QPushButton('Select Files', tab3)
        self.bshowTrain.setGeometry(360, 80, 75, objectwidth)
        self.bshowTrain.setStatusTip('Set Trainings Data')
        self.bshowTrain.clicked.connect(self.bshowtrainclicked)

        # create an table view
        self.view = QTableView(tab2)  # declare table view
        self.view.setGeometry(0, 0, 495, 250)
        self.model = QStandardItemModel()  # declare model
        self.view.setModel(self.model)  # assign model to table view

        # create the header of the table
        item = QStandardItem('SolutionTable')
        self.model.setHorizontalHeaderLabels(['Link', 'Classsifiy'])
        # auto scroll
        self.view.setAutoScroll(True)
        # and a scroll bar when it has to mutch data
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # create buttons to login in github
        self.blogging = QPushButton('Login to Github', tab1)
        self.blogging.setStatusTip('Login to Github for more features and private repository acces')
        self.blogging.resize(self.blogging.sizeHint())
        self.blogging.setGeometry(50, 130, 400, objectwidth)
        self.blogging.clicked.connect(self.bloggingclicked)

        # create label
        self.lurl = QLabel(tab1)
        self.lurl.setGeometry(50, 150, 400, objectwidth)

        # create githuboAuthSession
        self.github = OAuth2Session(client_id)

        # create label
        self.lback = QLabel(tab1)
        self.lback.setGeometry(50, 170, 400, objectwidth)
        # hide label
        self.lback.hide()

        # create TextField
        self.leback = QLineEdit(tab1)
        self.leback.setGeometry(50, 190, 400, objectwidth)
        self.leback.hide()

        # hiden button
        self.bpaste = QPushButton('Login', tab1)
        self.bpaste.setStatusTip('Get Login Token')
        self.bpaste.resize(self.bpaste.sizeHint())
        self.bpaste.setGeometry(50, 220, 400, objectwidth)
        self.bpaste.clicked.connect(self.bpasteclicked)
        self.bpaste.hide()

        # Create two Check boxes for training
        self.cbt = QCheckBox('with Validation Set', tab3)
        self.cbt.setGeometry(50, 20, 150, objectwidth)

        # own repositorys?
        self.cbown = QCheckBox('Add own repositorys', tab1)
        self.cbown.setGeometry(50, 220, 150, objectwidth)
        self.cbown.hide()
        self.cbown.setStatusTip('Add Own Repositorys automaticly to the list')

        # training create 6 textfield and 6 buttons
        self.letraingdir1 = QLineEdit(tab3)
        self.letraingdir1.setGeometry(50, 110, 300, objectwidth)
        self.letraingdir1.setStatusTip('Network main dir')

        self.btraindir1 = QPushButton('Set Dir', tab3)
        self.btraindir1.setStatusTip('Set Dir')
        self.btraindir1.resize(self.btraindir1.sizeHint())
        self.btraindir1.setGeometry(370, 110, 80, objectwidth)
        self.btraindir1.clicked.connect(self.btraindir1clicked)
        self.btraindir1.setStatusTip('Network main dir')

        self.letraingdir2 = QLineEdit(tab3)
        self.letraingdir2.setGeometry(50, 140, 300, objectwidth)
        self.letraingdir2.setStatusTip("Network sub dir")

        self.btraindir2 = QPushButton('Set Dir', tab3)
        self.btraindir2.setStatusTip('Set Dir')
        self.btraindir2.resize(self.btraindir2.sizeHint())
        self.btraindir2.setGeometry(370, 140, 80, objectwidth)
        self.btraindir2.clicked.connect(self.btraindir2clicked)
        self.btraindir2.setStatusTip("Network sub dir")

        self.letrainfile1 = QLineEdit(tab3)
        self.letrainfile1.setGeometry(50, 170, 300, objectwidth)
        self.letrainfile1.setStatusTip("Validation Set")

        self.btrainfile1 = QPushButton('Set Files', tab3)
        self.btrainfile1.setStatusTip('Set Files')
        self.btrainfile1.resize(self.btrainfile1.sizeHint())
        self.btrainfile1.setGeometry(370, 170, 80, objectwidth)
        self.btrainfile1.clicked.connect(self.btrainfile1clicked)
        self.btrainfile1.setStatusTip("Validation Set")

        self.letrainfile2 = QLineEdit(tab3)
        self.letrainfile2.setGeometry(50, 200, 300, objectwidth)
        self.letrainfile2.setStatusTip("Validation set classification")

        self.btrainfile2 = QPushButton('Set Files', tab3)
        self.btrainfile2.setStatusTip('Set Files')
        self.btrainfile2.resize(self.btrainfile2.sizeHint())
        self.btrainfile2.setGeometry(370, 200, 80, objectwidth)
        self.btrainfile2.clicked.connect(self.btrainfile2clicked)
        self.btrainfile2.setStatusTip("Validation set classification")

        self.letrainfile3 = QLineEdit(tab3)
        self.letrainfile3.setGeometry(50, 230, 300, objectwidth)
        self.letrainfile3.setStatusTip("Supervised train set")

        self.btrainfile3 = QPushButton('Set Files', tab3)
        self.btrainfile3.setStatusTip('Set Files')
        self.btrainfile3.resize(self.btrainfile3.sizeHint())
        self.btrainfile3.setGeometry(370, 230, 80, objectwidth)
        self.btrainfile3.clicked.connect(self.btrainfile3clicked)
        self.btrainfile3.setStatusTip("Supervised train set")

        self.letrainfile4 = QLineEdit(tab3)
        self.letrainfile4.setGeometry(50, 260, 300, objectwidth)
        self.letrainfile4.setStatusTip("Supervised train set classification")

        self.btrainfile4 = QPushButton('Set Files', tab3)
        self.btrainfile4.setStatusTip('Set Files')
        self.btrainfile4.resize(self.btrainfile4.sizeHint())
        self.btrainfile4.setGeometry(370, 260, 80, objectwidth)
        self.btrainfile4.clicked.connect(self.btrainfile4clicked)
        self.btrainfile4.setStatusTip("Supervised train set classification")

        # set geometry of main window
        self.setGeometry(300, 300, 500, 400)
        self.setMinimumSize(500, 400)
        self.show()
        self.setMaximumSize(9680, 400)

        # set title of main window
        self.setWindowTitle('Repository Tagger')
        # self.setFixedSize(500,300)
        # show the main window


    def closeEvent(self, event):
        """
            What happens when the user hits the close button
        :param event: close button click
        """

        # show a Close Dialog
        reply = QMessageBox.question(self, 'Exit',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        # check if user will quit or not
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def btrainingclicked(self):
        """
            training button was clicked and training will start recently
        """
        # start different modes when checkboxes are checked

        if self.cbt.isChecked():
            server.training(self.files, valid=True, vsD=self.trainfile1, vsR=self.trainfile2, svtD=self.trainfile3, svtR=self.trainfile4, main_dir=self.trainingdir1, sub_dir=self.trainingdir2)
        else:
            server.training(self.files, valid=False)


    def showdialog(self):
        """
            user wants to pick a file so we open the file picker for him
        """

        # start filepicker at '/home' place
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        # set textfiel text with filepath
        self.lepath.setText(fname[0])


    def bshowtrainclicked(self):
        """
            user wants to pick fileS so we open the dir picker for him
        """

        # start filepicker at '/home' place
        # fname = QFileDialog.getExistingDirectory(self, 'Select Directory', '/home')  # set textfiel text with filepath

        name = QFileDialog.getOpenFileNames(self, 'Select Files')
        nameString = ''
        for i in name[0]:
            nameString += i + ';'
        self.letrainingpath.setText(nameString)
        self.files = name[0]


    def btagclicked(self):
        """
            User wants to tag repositorys so the wish will done by the neural network recently
        """
        # load when he is login and want his repositorys added his repository and added them
        self.tabs.setCurrentIndex(1)
        app.processEvents()
        with open(self.lepath.text(), "r") as myfile:
            data = myfile.readlines()
            if self.cbown.isChecked():
                r = self.github.get('https://api.github.com/user/repos')
                if r.ok:
                    jsonstring = json.loads(r.text or r.content)
                    for ownrepos in jsonstring:
                        data.append(ownrepos['html_url'])

        for repositorys in data:
            repositorys = repositorys.replace('\n', '')
            item = QStandardItem(repositorys)
            self.model.appendRow(item)
            itemRow = item.row()
            indexOfColumn1 = self.model.index(itemRow, 1)

            if len(repositorys) != 0:
                keineahnung = getJson(repositorys, self.github)
                cat = server.classify(keineahnung)
                print(cat)
            # where cat stay the value should stand and than it should work
            self.model.setData(indexOfColumn1, cat, 0)
            app.processEvents()

        self.view.resizeColumnsToContents()
        self.data = data


    def bloggingclicked(self):
        """
            User choose to log in (github) for more features and more repository tagging

        """
        # show login fields
        self.bpaste.show()
        self.leback.show()
        self.lback.setText('Please Copy Callback Url')
        self.lback.show()
        # Redirect user to GitHub for authorization
        authorization_url, state = self.github.authorization_url(authorization_base_url)

        QDesktopServices.openUrl((QUrl(authorization_url)))
        print(authorization_url)


    def bpasteclicked(self):
        """
            user has paste the callbacklink(or not) in the field so we hopefully have a functional oAuth token
        :return: self
        """
        url = self.leback.text()
        # add a s so we have https hotfix for request_oAuthlib becouse it's make it only with https
        firstpart = url[0:4]
        secondpart = url[4:len(url)]
        completeurl = firstpart + 's' + secondpart
        self.github.fetch_token(token_url, client_secret=client_secret,
                                authorization_response=completeurl)
        # hide login button so user not try to relogin and an exception is create
        self.bpaste.hide()
        self.cbown.show()


    def resizeEvent(self, resizeEvent):
        """
         window size has change change the size of the objects too
        """

        width = self.width()


        scale = width / 500

        # tab 1
        startx = scale * 20 + 30
        temp = width - 2 * startx
        size = temp - (width - startx - (scale * 95 + 65) + 20)
        size2 = width - startx - (scale * 95 + 65)
        size3 = width - (scale * 95 + 65) + 20
        self.tabs.resize(width, self.height() - 20)
        self.lepath.setGeometry(startx, 50, size2, objectwidth)
        self.bfiledialog.setGeometry(size3, 50, size, objectwidth)
        self.btag.setGeometry(startx, 90, temp, objectwidth)
        self.blogging.setGeometry(startx, 130, temp, objectwidth)
        self.lurl.setGeometry(startx, 150, temp, objectwidth)
        self.lback.setGeometry(startx, 170, temp, objectwidth)
        self.leback.setGeometry(startx, 190, temp, objectwidth)
        self.bpaste.setGeometry(startx, 220, temp, objectwidth)
        self.cbown.setGeometry(startx, 220, temp, objectwidth)

        # tab 2
        self.view.setGeometry(0, 0, width - 5, self.height() - 50)

        # tab 3
        self.bshowTrain.setGeometry(size3, 80, size, objectwidth)
        self.cbt.setGeometry(startx, 20, 150, objectwidth)
        self.btraining.setGeometry(startx, 50, size, objectwidth)
        self.letrainingpath.setGeometry(startx, 80, size2, objectwidth)

        self.letraingdir1.setGeometry(startx, 110, size2, objectwidth)
        self.letraingdir2.setGeometry(startx, 140, size2, objectwidth)
        self.btraindir1.setGeometry(size3, 110, size, objectwidth)
        self.btraindir2.setGeometry(size3, 140, size, objectwidth)

        self.letrainfile1.setGeometry(startx, 170, size2, objectwidth)
        self.letrainfile2.setGeometry(startx, 200, size2, objectwidth)
        self.letrainfile3.setGeometry(startx, 230, size2, objectwidth)
        self.letrainfile4.setGeometry(startx, 260, size2, objectwidth)
        self.btrainfile1.setGeometry(size3, 170, size, objectwidth)
        self.btrainfile2.setGeometry(size3, 200, size, objectwidth)
        self.btrainfile3.setGeometry(size3, 230, size, objectwidth)
        self.btrainfile4.setGeometry(size3, 260, size, objectwidth)


    def btraindir1clicked(self):
        """
        Select an dir
        """


        # start filepicker at '/home' place


        fname = QFileDialog.getExistingDirectory(self, 'Select Directory', '/home')  # set textfiel text with filepath
        self.letraingdir1.setText(fname)
        self.trainingdir1 = fname


    def btraindir2clicked(self):
        """
        Select an dir
        """


        # start filepicker at '/home' place


        fname = QFileDialog.getExistingDirectory(self, 'Select Directory', '/home')  # set textfiel text with filepath
        self.letraingdir2.setText(fname)
        self.trainingdir2 = fname


    def btrainfile1clicked(self):
        """
        Select multiple files
        """


        name = QFileDialog.getOpenFileNames(self, 'Select Files')
        nameString = ''
        for i in name[0]:
            nameString += i + ';'
        self.letrainfile1.setText(nameString)
        self.trainfile1 = name[0]


    def btrainfile2clicked(self):
        """
       Select multiple files
       """


        name = QFileDialog.getOpenFileNames(self, 'Select Files')
        nameString = ''
        for i in name[0]:
            nameString += i + ';'
        self.letrainfile2.setText(nameString)
        self.trainfile2 = name[0]


    def btrainfile3clicked(self):
        """
        Select multiple files
        """


        name = QFileDialog.getOpenFileNames(self, 'Select Files')
        nameString = ''
        for i in name[0]:
            nameString += i + ';'
        self.letrainfile3.setText(nameString)
        self.trainfile3 = name[0]


    def btrainfile4clicked(self):
        """
       Select multiple files
       """


        name = QFileDialog.getOpenFileNames(self, 'Select Files')
        nameString = ''
        for i in name[0]:
            nameString += i + ';'
        self.letrainfile4.setText(nameString)
        self.trainfile4 = name[0]

if __name__ == '__main__':
    """
    Entry point of the application create the gui
    """

    app = QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())
