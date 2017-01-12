import sys

from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QFileDialog, QApplication)
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
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

        # create a button
        btraining = QPushButton('Training', self)
        # when the cursor is move above the button show this text on the status bar
        btraining.setStatusTip('Start Training Mode')
        # resize button
        btraining.resize(btraining.sizeHint())
        # set his geometry ( xposition,yposition,xsize,ysize)
        btraining.setGeometry(50, 50, 75, 25)
        # what happens when the button is clicked
        btraining.clicked.connect(self.btrainingclicked)

        # same like above
        bfiledialog = QPushButton('Pick File', self)
        bfiledialog.setStatusTip('Pick File with Repositorys Links')
        bfiledialog.resize(bfiledialog.sizeHint())
        bfiledialog.setGeometry(370, 50, 75, 25)
        bfiledialog.clicked.connect(self.showdialog)

        # create a 'textField'
        self.lepath = QLineEdit(self)
        self.lepath.setGeometry(150, 50, 200, 25)
        self.lepath.setStatusTip('Path to Repository Link List File')

        btag = QPushButton('Tag Repositorys', self)
        btag.setStatusTip('Tag Repositorys from File')
        btag.resize(btag.sizeHint())
        btag.setGeometry(50, 90, 395, 25)
        btag.clicked.connect(self.btagclicked)

        # create buttons
        blogging = QPushButton('Login to Github', self)
        blogging.setStatusTip('Login to Github for more features and private repository acces')
        blogging.resize(blogging.sizeHint())
        blogging.setGeometry(50, 130, 395, 25)
        blogging.clicked.connect(self.bloggingclicked)

        # create label
        self.lurl = QLabel(self)
        self.lurl.setGeometry(50, 150, 395, 25)

        # create githuboAuthSession
        self.github = OAuth2Session(client_id)

        # create label
        self.lback = QLabel(self)
        self.lback.setGeometry(50, 170, 395, 25)
        # hide label
        self.lback.hide()

        # create TextField
        self.leback = QLineEdit(self)
        self.leback.setGeometry(50, 190, 395, 25)
        self.leback.hide()

        # hiden button
        self.bpaste = QPushButton('Login', self)
        self.bpaste.setStatusTip('Get Login Token')
        self.bpaste.resize(self.bpaste.sizeHint())
        self.bpaste.setGeometry(50, 220, 395, 25)
        self.bpaste.clicked.connect(self.bpasteclicked)
        self.bpaste.hide()

        # Create two Check boxes for training
        self.cbt = QCheckBox('with Validation Set', self)
        self.cbt.setGeometry(50, 20, 150, 25)
        self.cb = QCheckBox('new Read of Dataset', self)
        self.cb.setGeometry(50, 5, 150, 25)

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

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                # set textfiel text with filepath
                self.lepath.setText(fname[0])

    def btagclicked(self):
        """
            User wants to tag repositorys so the wish will done by the neural network recently
        """

        with open(self.lepath.text(), "r") as myfile:
            data = myfile.readlines()

        for blabala in data:
            blabala = blabala.replace('\n', '')
            print(blabala)
            if len(blabala) == 0:
                keineahnung = getJson2(blabala, self.github)

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

        # QDesktopServices.openUrl((QUrl(authorization_url)))
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
