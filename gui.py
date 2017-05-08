"""
A GUI for updating the RePEc file

This is my first use of PyQt5

I heavily consulted the following tutorial:
http://zetcode.com/gui/pyqt5/
as well as this post on QDialogs:
http://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo

author: Colin Williams
last edited: April. 2017
"""

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
    QLabel, QLineEdit, QTextEdit, QGridLayout, QDateEdit,
    QSpinBox, QDialog, QDialogButtonBox)
from PyQt5.QtCore import QCoreApplication
from collections import deque
from papers import addNewEntry, genHTML

# TODO: test on linux
# DONE: connect paper input to main window
# DONE: generate HTML
# DONE: implement 'submit changes' button
# TODO: implement 'Williams Author' button

###############################################################
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.paperDetails = [] # keep track of information needed to generate html
        self.authors = [] # keep track of each author of the paper
    def initUI(self):

        # BUTTONS
        addAuthorButton = QPushButton('Add Author', self)
        addPaperButton = QPushButton('Add Paper', self)
        submitButton = QPushButton('Submit Changes', self)
        addAuthorButton.clicked.connect(self.add_author)
        addPaperButton.clicked.connect(self.add_paper)
        submitButton.clicked.connect(self.submit_changes)

        # HTML
        self.htmlEdit = QLineEdit()

        # RePEc ENTRY
        self.entryEdit = QTextEdit()

        # LAYOUT
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(addAuthorButton, 0, 0)
        grid.addWidget(addPaperButton, 0, 1)
        grid.addWidget(submitButton, 0, 2)
        grid.addWidget(self.htmlEdit, 1, 0, 1, 3)
        grid.addWidget(self.entryEdit, 2, 0, 2, 3)
        self.setLayout(grid)

        self.resize(400, 400)
        self.setWindowTitle("Update RePEc File")

        self.show()

    def add_author(self):
        authEntry, authorName, ok = Author.getAuthorInfo()
        if ok:
            for line in authEntry:
                self.entryEdit.append(line)
            self.authors.append(authorName)

    def add_paper(self):
        paper, paperHtml, ok = Paper.getPaperInfo()
        if ok:
            for line in paper:
                self.entryEdit.append(line)
            self.paperDetails = paperHtml

    def submit_changes(self):
        data = self.entryEdit.toPlainText()
        addNewEntry(data)
        htmlString = genHTML(self.paperDetails, self.authors)
        self.htmlEdit.setText(htmlString)

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

        info.append('Author-Name: ' + self.getFullName())
        info.append('Author-X-Name-First: ' + self.fNameEdit.text())
        info.append('Author-X-Name-Last: ' + self.lNameEdit.text())
        info.append('Author-Person: ' + self.codeEdit.text())
        info.append('Author-Workplace-Name: ' + self.workplaceEdit.text())
        info.append('Author-Workplace-Homepage: ' + self.homepageEdit.text())
        return info

    def getFullName(self):
        # Build up the full name
        fullName = self.fNameEdit.text() + " "
        if self.mNameEdit.text():
            fullName += (self.mNameEdit.text() + ". ")
        fullName += self.lNameEdit.text()
        return fullName

    @staticmethod
    def getAuthorInfo(parent = None):
        dialog = Author(parent)
        result = dialog.exec_()
        info = dialog.authorInfo()
        authorName = dialog.getFullName()
        return (info, authorName, result == QDialog.Accepted)

###############################################################
class Paper(QDialog):

    def __init__(self, parent=None):
        super(Paper, self).__init__(parent)

        self.initUI()
    def initUI(self):
        # Labels
        #year = QLabel('Year:')
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
        #self.yearEdit = QSpinBox(self)
        self.titleEdit = QLineEdit()
        self.classEdit = QLineEdit()
        self.keywordsEdit = QLineEdit()
        self.lengthEdit = QSpinBox(self)
        self.numberEdit = QSpinBox(self)
        self.createdEdit = QDateEdit()
        self.urlTitleEdit = QLineEdit("http://web.williams.edu/Economics/wp/")
        self.abstractEdit = QTextEdit()

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # Layout
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(title, 1, 0)
        grid.addWidget(self.titleEdit, 1, 1, 1, 2)
        grid.addWidget(classification, 2, 0)
        grid.addWidget(self.classEdit, 2, 1, 1, 2)
        grid.addWidget(keywords, 3, 0)
        grid.addWidget(self.keywordsEdit, 3, 1, 1, 2)
        grid.addWidget(length, 4, 0)
        grid.addWidget(self.lengthEdit, 4, 1, 1, 2)
        grid.addWidget(pages, 4, 3)
        grid.addWidget(number, 5, 0)
        grid.addWidget(self.numberEdit, 5, 1, 1, 2)
        grid.addWidget(created, 6, 0)
        grid.addWidget(self.createdEdit, 6, 1, 1, 2)
        grid.addWidget(urlTitle, 7, 0)
        grid.addWidget(self.urlTitleEdit, 7, 1, 1, 2)
        grid.addWidget(abstract, 8, 0)
        grid.addWidget(self.abstractEdit, 8, 1, 1, 2)
        grid.addWidget(buttons, 9, 1, 9, 2)
        self.setLayout(grid)

        # Focus and tab order
        title.setFocus(True)
        self.setTabOrder(self.keywordsEdit, self.lengthEdit)
        self.setTabOrder(self.lengthEdit, self.numberEdit)
        self.setTabOrder(self.createdEdit, self.urlTitleEdit)

        #self.setGeometry(300, 300, 300, 220)
        self.resize(450, 500)
        self.setWindowTitle('Enter Paper Information')

    def paperInfo(self):
        info = deque()
        info.append("Title: " + self.titleEdit.text())
        info.append("Abstract: " + self.abstractEdit.toPlainText())
        info.append("Classification-JEL: " + self.classEdit.text())
        info.append("Keywords: " + self.keywordsEdit.text())
        info.append("Length: " + str(self.lengthEdit.value()) + " pages")

        num = self.numberEdit.value()
        if num < 10:
            strNum = "0" + str(num) # The paper number should be two digits
        else:
            strNum = str(num)

        info.append("Number: 2017-" + strNum) # TODO: fix year
        info.append("Note: ")
        info.append("Creation-date: " + str(self.createdEdit.date().toString('yyyy-MM')))
        info.append("Revision-date: ")
        info.append("Price: Free")
        info.append("Publication-Status: ")
        info.append("File-URL: " + self.urlTitleEdit.text())
        info.append("File-Format: Application/PDF")
        info.append("File-Function: Full text")
        info.append("Handle: RePEc:wil:wileco:2017-" + strNum) #TODO: fix year

        return info

    # get the fields relevant to making the html entry
    def htmlInfo(self):
        paperHtml = []

        # TODO: this code is duplicated in 'paperInfo' and is ugly
        num = self.numberEdit.value()
        if num < 10:
            strNum = "0" + str(num) # The paper number should be two digits
        else:
            strNum = str(num)
        paperHtml.append(strNum)
        paperHtml.append(self.urlTitleEdit.text())
        paperHtml.append(self.titleEdit.text())

        return paperHtml

    @staticmethod
    def getPaperInfo(parent = None):
        dialog = Paper(parent)
        result = dialog.exec_()
        info = dialog.paperInfo()
        html = dialog.htmlInfo()
        return (info, html, result == QDialog.Accepted)

###############################################################
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
