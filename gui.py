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


class Example(QMainWindow):
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
        self.tabs.setGeometry(0, 0, 500, 280)

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
        self.btraining.setGeometry(50, 50, 75, 25)
        # what happens when the button is clicked
        self.btraining.clicked.connect(self.btrainingclicked)

        # same like above
        self.bfiledialog = QPushButton('Pick File', tab1)
        self.bfiledialog.setStatusTip('Pick File with Repositorys Links')
        self.bfiledialog.resize(self.bfiledialog.sizeHint())
        self.bfiledialog.setGeometry(370, 50, 80, 25)
        self.bfiledialog.clicked.connect(self.showdialog)

        # create a 'textField'
        self.lepath = QLineEdit(tab1)
        self.lepath.setGeometry(50, 50, 300, 25)
        self.lepath.setStatusTip('Path to Repository Link List File')

        # create another button to classify repositorys
        self.btag = QPushButton('Classify Repositorys', tab1)
        self.btag.setStatusTip('Classify Repositorys from File')
        self.btag.resize(self.btag.sizeHint())
        self.btag.setGeometry(50, 90, 400, 25)
        self.btag.clicked.connect(self.btagclicked)

        # add an TextField for Trainings Data
        self.letrainingpath = QLineEdit(tab3)
        self.letrainingpath.setGeometry(50, 80, 300, 25)
        self.letrainingpath.setStatusTip('Set Trainings Data')

        # another button to set Path
        self.bshowTrain = QPushButton('Select Files', tab3)
        self.bshowTrain.setGeometry(360, 80, 75, 25)
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
        self.blogging.setGeometry(50, 130, 400, 25)
        self.blogging.clicked.connect(self.bloggingclicked)

        # create label
        self.lurl = QLabel(tab1)
        self.lurl.setGeometry(50, 150, 400, 25)

        # create githuboAuthSession
        self.github = OAuth2Session(client_id)

        # create label
        self.lback = QLabel(tab1)
        self.lback.setGeometry(50, 170, 400, 25)
        # hide label
        self.lback.hide()

        # create TextField
        self.leback = QLineEdit(tab1)
        self.leback.setGeometry(50, 190, 400, 25)
        self.leback.hide()

        # hiden button
        self.bpaste = QPushButton('Login', tab1)
        self.bpaste.setStatusTip('Get Login Token')
        self.bpaste.resize(self.bpaste.sizeHint())
        self.bpaste.setGeometry(50, 220, 400, 25)
        self.bpaste.clicked.connect(self.bpasteclicked)
        self.bpaste.hide()

        # Create two Check boxes for training
        self.cbt = QCheckBox('with Validation Set', tab3)
        self.cbt.setGeometry(50, 20, 150, 25)

        self.cb = QCheckBox('new Read of Dataset', tab3)
        self.cb.setGeometry(50, 5, 150, 25)

        # own repositorys?
        self.cbown = QCheckBox('Add own repositorys', tab1)
        self.cbown.setGeometry(50, 220, 150, 25)
        self.cbown.hide()
        self.cbown.setStatusTip('Add Own Repositorys automaticly to the list')

        # set geometry of main window
        self.setGeometry(300, 300, 500, 300)
        self.setMinimumSize(500, 300)
        self.show()
        self.setMaximumSize(9680,300)

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
        if self.cb.isChecked():
            print("New DataSet")
            #server.training([], True, False)
            return

        if self.cbt.isChecked():
            print('Validation')
            server.training(self.files, False, True, [], [], [], [])
        else:
            print('Standard')
            server.training(self.files, False, False)

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
            self.model.setData(indexOfColumn1, 'not Classifed yet', 0)
            app.processEvents()

            if len(repositorys) != 0:
                keineahnung = getJson(repositorys, self.github)
                cat = server.classify(keineahnung)
                print(cat)
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
            user has pastethe callbacklink(or not) in the field so we hopefully have a functional oAuth token
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
        # tab 1
        temp = self.width() - 2 * ((self.width() / 500) * 20 + 30)
        self.tabs.resize(self.width(), self.height() - 20)
        self.lepath.setGeometry((self.width() / 500) * 20 + 30, 50, self.width() - ((self.width() / 500) * 20 + 30)-((self.width()/500)*95+65), 25)
        self.bfiledialog.setGeometry(self.width() -((self.width()/500)*95+65)+20, 50,temp-(self.width() - ((self.width() / 500) * 20 + 30)-((self.width()/500)*95+65)+20) , 25)
        self.btag.setGeometry((self.width() / 500) * 20 + 30, 90, temp, 25)
        self.blogging.setGeometry(((self.width() / 500)) * 20 + 30, 130, temp, 25)
        self.lurl.setGeometry((self.width() / 500) * 20 + 30, 150,temp, 25 )
        self.lback.setGeometry((self.width() / 500) * 20 + 30, 170,temp, 25 )
        self.leback.setGeometry((self.width() / 500) * 20 + 30, 190,temp, 25 )
        self.bpaste.setGeometry((self.width() / 500) * 20 + 30, 220,temp, 25 )
        self.cbown.setGeometry((self.width() / 500) * 20 + 30, 220,temp, 25 )

        # tab 2
        self.view.setGeometry(0,0,self.width()-5, self.height()-50)

        # tab 3
        self.bshowTrain.setGeometry(self.width() -((self.width()/500)*95+65)+20, 80,temp-(self.width() - ((self.width() / 500) * 20 + 30)-((self.width()/500)*95+65)+20) , 25)
        self.cb.setGeometry((self.width() / 500) * 20 + 30, 5,150,25)
        self.cbt.setGeometry((self.width() / 500) * 20 + 30, 20,150,25)
        self.btraining.setGeometry((self.width() / 500) * 20 + 30, 50,temp-(self.width() - ((self.width() / 500) * 20 + 30)-((self.width()/500)*95+65)+20),25 )
        self.letrainingpath.setGeometry((self.width() / 500) * 20 + 30, 80, self.width() - ((self.width() / 500) * 20 + 30)-((self.width()/500)*95+65), 25)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
