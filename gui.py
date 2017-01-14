import json
import sys


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
from PyQt5.QtWidgets import QScrollBar
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QWidget
from requests_oauthlib import OAuth2Session

from getJsonWithoAuth import getJson2

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

        self.initui()

    def initui(self):
        """
            place object on window and set there geometry and reaction
        """

        # create a Status bar at the bottom of the window
        self.statusBar()
        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(0, 0, 500, 280)
        tab1 = QWidget()
        self.tabs.addTab(tab1, 'Classify')
        tab1.setStatusTip('Set Classify Option and start it')
        tab2 = QWidget()
        self.tabs.addTab(tab2, 'Solution')
        tab2.setStatusTip('Solution of Classify')
        tab3 = QWidget()
        self.tabs.addTab(tab3, 'Training')
        tab3.setStatusTip('Training option and start training')

        # create a button
        btraining = QPushButton('Training', tab3)
        # when the cursor is move above the button show this text on the status bar
        btraining.setStatusTip('Start Training Mode')
        # resize button
        btraining.resize(btraining.sizeHint())
        # set his geometry ( xposition,yposition,xsize,ysize)
        btraining.setGeometry(50, 50, 75, 25)
        # what happens when the button is clicked
        btraining.clicked.connect(self.btrainingclicked)

        # same like above
        bfiledialog = QPushButton('Pick File', tab1)
        bfiledialog.setStatusTip('Pick File with Repositorys Links')
        bfiledialog.resize(bfiledialog.sizeHint())
        bfiledialog.setGeometry(370, 50, 75, 25)
        bfiledialog.clicked.connect(self.showdialog)

        # create a 'textField'
        self.lepath = QLineEdit(tab1)
        self.lepath.setGeometry(50, 50, 300, 25)
        self.lepath.setStatusTip('Path to Repository Link List File')

        btag = QPushButton('Tag Repositorys', tab1)
        btag.setStatusTip('Tag Repositorys from File')
        btag.resize(btag.sizeHint())
        btag.setGeometry(50, 90, 395, 25)
        btag.clicked.connect(self.btagclicked)

        self.letrainingpath = QLineEdit(tab3)
        self.letrainingpath.setGeometry(50, 80, 300, 25)
        self.letrainingpath.setStatusTip('Set Trainings Path')

        bshowTrain = QPushButton('Set path', tab3)
        bshowTrain.setGeometry(360, 80, 75, 25)
        bshowTrain.setStatusTip('Set Trainings Path')
        bshowTrain.clicked.connect(self.bshowtrainclicked)

        self.view = QTableView(tab2)  # declare table view
        self.view.setGeometry(0, 0, 495, 250)
        self.model = QStandardItemModel()  # declare model
        self.view.setModel(self.model)  # assign model to table view
        item = QStandardItem('SolutionTable')
        self.model.setHorizontalHeaderLabels(['Link', 'Classsifiy'])
        self.view.setAutoScroll(True)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # create buttons
        blogging = QPushButton('Login to Github', tab1)
        blogging.setStatusTip('Login to Github for more features and private repository acces')
        blogging.resize(blogging.sizeHint())
        blogging.setGeometry(50, 130, 395, 25)
        blogging.clicked.connect(self.bloggingclicked)

        # create label
        self.lurl = QLabel(tab1)
        self.lurl.setGeometry(50, 150, 395, 25)

        # create githuboAuthSession
        self.github = OAuth2Session(client_id)

        # create label
        self.lback = QLabel(tab1)
        self.lback.setGeometry(50, 170, 395, 25)
        # hide label
        self.lback.hide()

        # create TextField
        self.leback = QLineEdit(tab1)
        self.leback.setGeometry(50, 190, 395, 25)
        self.leback.hide()

        # hiden button
        self.bpaste = QPushButton('Login', tab1)
        self.bpaste.setStatusTip('Get Login Token')
        self.bpaste.resize(self.bpaste.sizeHint())
        self.bpaste.setGeometry(50, 220, 395, 25)
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
        # set title of main window
        self.setWindowTitle('Repository Tagger')
        # show the main window
        self.show()

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
            print('New Dataset')

        if self.cbt.isChecked():
            print('Validation')
        else:
            print('Standart')

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
            nameString += i+';'
        self.letrainingpath.setText(nameString)
        self.files = name[0]



    def btagclicked(self):
        """
            User wants to tag repositorys so the wish will done by the neural network recently
        """
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
                keineahnung = getJson2(repositorys, self.github)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
