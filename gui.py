"""
A GUI for updating the RePEc file

This is my first use of PyQt

I heavily consulted the following tutorial:
http://zetcode.com/gui/pyqt5/
as well as this post on dialogs:
http://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo

author: Colin Williams
last edited: April. 2017
"""

import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
    QPushButton, QDesktopWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QDateEdit, QSpinBox, QDialog, QDialogButtonBox)
from PyQt5.QtCore import QCoreApplication

from collections import deque

# TODO: link to papers.py
# TODO: test on linux

###############################################################
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):

        # BUTTONS
        addAuthorButton = QPushButton('Add Author', self)
        addPaperButton = QPushButton('Add Paper', self)
        submitButton = QPushButton('Submit Changes', self)
        addAuthorButton.clicked.connect(self.add_author)
        addPaperButton.clicked.connect(self.add_paper)
        submitButton.clicked.connect(self.submit_changes)

        # RePEc ENTRY
        self.entryEdit = QTextEdit()

        # LAYOUT
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(addAuthorButton, 0, 0)
        grid.addWidget(addPaperButton, 0, 1)
        grid.addWidget(submitButton, 0, 2)
        grid.addWidget(self.entryEdit, 1, 0, 1, 3)
        self.setLayout(grid)

        self.resize(400, 400)
        self.setWindowTitle("Update RePEc File")

        self.show()

    def add_author(self):
        auth, ok = Author.getAuthorInfo()
        if ok:
            for line in auth:
                self.entryEdit.append(line)

    def add_paper(self):
        paper, ok = Paper.getPaperInfo()

    def submit_changes(self):
        pass

###############################################################
class Author(QDialog):

    def __init__(self, parent = None):
        super(Author, self).__init__(parent)
        self.initUI()
    def initUI(self):
        # Labels
        fName = QLabel("First Name: ")
        mName = QLabel("Middle Initial: ")
        lName = QLabel("Last Name: ")
        authorCode = QLabel("RePEc code: ")
        workplace = QLabel("Workplace: ")
        homepage = QLabel("Homepage: ")

        # Edits
        self.fNameEdit = QLineEdit()
        self.mNameEdit = QLineEdit()
        self.lNameEdit = QLineEdit()
        self.codeEdit = QLineEdit()
        self.workplaceEdit = QLineEdit()
        self.homepageEdit = QLineEdit()

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        williamsButton = QPushButton('Williams Author', self)

        # Listeners
        williamsButton.clicked.connect(self.on_WilliamsButton_clicked)

        # Layout
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(lName, 1, 0)
        grid.addWidget(self.lNameEdit, 1, 1)
        grid.addWidget(williamsButton, 1, 2)
        grid.addWidget(fName, 2, 0)
        grid.addWidget(self.fNameEdit, 2, 1)
        grid.addWidget(mName, 3, 0)
        grid.addWidget(self.mNameEdit, 3, 1)
        grid.addWidget(authorCode, 4, 0)
        grid.addWidget(self.codeEdit, 4, 1)
        grid.addWidget(workplace, 5, 0)
        grid.addWidget(self.workplaceEdit, 5, 1)
        grid.addWidget(homepage, 6, 0)
        grid.addWidget(self.homepageEdit, 6, 1)
        grid.addWidget(buttons, 7, 0)
        self.setLayout(grid)

        # Focus and tab order
        self.lNameEdit.setFocus(True)
        self.resize(400, 400)
        self.setWindowTitle('Author')

    def on_WilliamsButton_clicked(self):
        pass

    def authorInfo(self):
        info = deque()

        # Build up the full name
        fullName = self.fNameEdit.text() + " "
        if self.mNameEdit.text():
            fullName += (self.mNameEdit.text() + ". ")
        fullName += self.lNameEdit.text()

        info.append('Author-Name: ' + fullName)
        info.append('Author-X-Name-First: ' + self.fNameEdit.text())
        info.append('Author-X-Name-Last: ' + self.lNameEdit.text())
        info.append('Author-Person: ' + self.codeEdit.text())
        info.append('Author-Workplace-Name: ' + self.workplaceEdit.text())
        info.append('Author-Workplace-Homepage: ' + self.homepageEdit.text())
        #info.append() #AUTHOR LAST NAME TO BUILD FILE URL
        return info

    @staticmethod
    def getAuthorInfo(parent = None):
        dialog = Author(parent)
        result = dialog.exec_()
        info = dialog.authorInfo()
        return (info, result == QDialog.Accepted)

###############################################################
class Paper(QDialog):

    def __init__(self, parent=None):
        super(Paper, self).__init__(parent)

        self.initUI()
    def initUI(self):
        # Labels
        title = QLabel('Paper Title:')
        abstract = QLabel('Abstract:')
        classification = QLabel('JEL-classification:')
        keywords = QLabel('Keywords:')
        length = QLabel('Length:')
        pages = QLabel(' pages')
        number = QLabel('Number:')
        created = QLabel('Date Created:')
        urlTitle = QLabel('URL Title:')

        # Edits
        titleEdit = QLineEdit()
        classEdit = QLineEdit()
        keywordsEdit = QLineEdit()
        lengthEdit = QSpinBox(self)
        numberEdit = QSpinBox(self)
        createdEdit = QDateEdit()
        urlTitleEdit = QLineEdit("http://web.williams.edu/Economics/wp/")
        abstractEdit = QTextEdit()

        # Buttons
        quitButton = QPushButton('Quit', self)
        submitButton = QPushButton('Submit', self)

        # Listeners
        quitButton.clicked.connect(QCoreApplication.instance().quit)

        # Layout
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1, 1, 2)
        grid.addWidget(classification, 2, 0)
        grid.addWidget(classEdit, 2, 1, 1, 2)
        grid.addWidget(keywords, 3, 0)
        grid.addWidget(keywordsEdit, 3, 1, 1, 2)
        grid.addWidget(length, 4, 0)
        grid.addWidget(lengthEdit, 4, 1, 1, 2)
        grid.addWidget(pages, 4, 3)
        grid.addWidget(number, 5, 0)
        grid.addWidget(numberEdit, 5, 1, 1, 2)
        grid.addWidget(created, 6, 0)
        grid.addWidget(createdEdit, 6, 1, 1, 2)
        grid.addWidget(urlTitle, 7, 0)
        grid.addWidget(urlTitleEdit, 7, 1, 1, 2)
        grid.addWidget(abstract, 8, 0)
        grid.addWidget(abstractEdit, 8, 1, 1, 2)
        grid.addWidget(submitButton, 9, 1)
        grid.addWidget(quitButton, 9, 2)
        self.setLayout(grid)

        # Focus and tab order
        title.setFocus(True)
        self.setTabOrder(keywordsEdit, lengthEdit)
        self.setTabOrder(lengthEdit, numberEdit)
        self.setTabOrder(createdEdit, urlTitleEdit)

        #self.setGeometry(300, 300, 300, 220)
        self.resize(450, 500)
        self.center()
        self.setWindowTitle('Paper')

    def paperInfo(self):
        info = []
        return info

    @staticmethod
    def getPaperInfo(parent = None):
        dialog = Paper(parent)
        result = dialog.exec_()
        info = dialog.paperInfo()
        return (info, result == QDialog.Accepted)

        #self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

###############################################################
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
