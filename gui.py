"""
A GUI for updating the RePEc file

This is my first use of PyQt

I heavily consulted the following tutorial:
http://zetcode.com/gui/pyqt5/

author: Colin Williams
last edited: Jan. 2016
"""

import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
    QPushButton, QDesktopWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QDateEdit, QSpinBox, )

#from PyQt5.QtGui import QIcon, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QCoreApplication

# TODO: link menus together
# TODO: link to papers.py
# TODO: test on linux

class numAuthors(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        prompt = QLabel("How many authors?")
        num = QSpinBox(self)

        self.dialog = Authors()

        # Buttons
        submitButton = QPushButton('Submit', self)
        quitButton = QPushButton('Quit', self)

        # Listeners
        quitButton.clicked.connect(QCoreApplication.instance().quit)
        submitButton.clicked.connect(self.on_submitButton_clicked)

        # Layout
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(prompt, 1, 0)
        grid.addWidget(num, 1, 1)

        grid.addWidget(submitButton, 2, 0)
        grid.addWidget(quitButton, 2, 1)

        self.setLayout(grid)

        self.resize(280, 150)
        self.center()
        self.setWindowTitle('Number of Authors')

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_submitButton_clicked(self):
        self.dialog.show()

class Authors(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # Labels
        fName = QLabel("First Name: ")
        mName = QLabel("Middle Initial: ")
        lName = QLabel("Last Name: ")
        # TODO: RePEc code
        workplace = QLabel("Workplace: ")
        homepage = QLabel("Homepage: ")

        # Edits
        fNameEdit = QLineEdit()
        mNameEdit = QLineEdit()
        lNameEdit = QLineEdit()
        workplaceEdit = QLineEdit()
        homepageEdit = QLineEdit()

        # Buttons
        williamsButton = QPushButton('Williams Author', self)
        submitButton = QPushButton('Submit', self)
        quitButton = QPushButton('Quit', self)


        # Listeners
        quitButton.clicked.connect(QCoreApplication.instance().quit)

        # Layout
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(lName, 1, 0)
        grid.addWidget(lNameEdit, 1, 1)
        grid.addWidget(williamsButton, 1, 2)

        grid.addWidget(fName, 2, 0)
        grid.addWidget(fNameEdit, 2, 1)

        grid.addWidget(mName, 3, 0)
        grid.addWidget(mNameEdit, 3, 1)

        grid.addWidget(workplace, 4, 0)
        grid.addWidget(workplaceEdit, 4, 1)

        grid.addWidget(homepage, 5, 0)
        grid.addWidget(homepageEdit, 5, 1)

        grid.addWidget(submitButton, 6, 0)
        grid.addWidget(quitButton, 6, 1)

        self.setLayout(grid)

        # Focus and tab order
        lNameEdit.setFocus(True)


        self.resize(400, 400)
        self.center()
        self.setWindowTitle('Author') #TODO: add author number

        #self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class Paper(QWidget):

    def __init__(self):
        super().__init__()

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

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    app = QApplication(sys.argv)
    #paper = Paper()
    num = numAuthors()
    #auth = Authors()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
