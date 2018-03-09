import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(250, 250, 500, 300)
        self.setWindowTitle("CAPTIONING")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))

        extractAction = QtGui.QAction("&GET TO THE CHOPPAH!!!", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)
        self.langtype='English'
        self.audtype='Audio'
        self.filename=None

        self.home()

    def home(self):
        btn = QtGui.QPushButton("Quit", self)
        btn.clicked.connect(self.close_application)
        btn.move(370,250)

        self.btnfile = QtGui.QPushButton("Select File",self)
        self.btnfile.move(250,45)
        self.btnfile.clicked.connect(self.getFile)
        self.btnfile.setVisible(False)

        self.btngo = QtGui.QPushButton("Go",self)
        self.btngo.move(50,250)
        self.btngo.clicked.connect(self.goSubmit)

        self.btnstop = QtGui.QPushButton("Stop",self)
        self.btnstop.move(210,250)
        self.btnstop.clicked.connect(self.stopSubmit)

        print(self.style().objectName())
        audioChoice = QtGui.QLabel("Language    :", self)
        audioChoice.move(20,20)
        audiocomboBox = QtGui.QComboBox(self)
        audiocomboBox.addItem("Record")
        audiocomboBox.addItem("Upload")
        audiocomboBox.addItem("System Audio")
        audiocomboBox.move(110, 20)
        audiocomboBox.activated[str].connect(self.aud_choice)

        languageChoice = QtGui.QLabel("Audio Type :", self)
        languageChoice.move(20,70)
        langcomboBox = QtGui.QComboBox(self)
        langcomboBox.addItem("English")
        langcomboBox.addItem("Hindi")
        langcomboBox.addItem("Tamil")
        langcomboBox.addItem("Telugu")
        langcomboBox.move(110,70)
        langcomboBox.activated[str].connect(self.lang_choice)

        self.textBox = QtGui.QTextEdit(self)
        self.textBox.move(20,120)
        self.textBox.resize(460,110)
        # self.textBox.setDisabled(True)

        self.pic = QtGui.QLabel(self)
        self.pic.move(380,12)
        self.pic.resize(100,100)
        self.pic.setPixmap(QtGui.QPixmap("Q107.png"))
        self.pic.show()

        self.process = QtCore.QProcess(self)
        self.process.readyRead.connect(self.dataReady)

        # self.process.started.connect(lambda: self.btngo.setEnabled(False))
        # self.process.finished.connect(lambda: self.btngo.setEnabled(True))

        self.show()

    def dataReady(self):
        cursor = self.textBox.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(str(self.process.readAll()))
        self.textBox.ensureCursorVisible()

    # def addText(self, query):
    #     self.textBox.append(" "+query)

    def lang_choice(self, text):
        self.langtype=text
        print 'Language:',text

    def aud_choice(self, text):
        self.audtype=text
        print 'Audio:',text
        self.visibility()

    def goSubmit(self):
        with open('data.py', 'w') as f:
            f.write('language = "{}"\n'.format(self.langtype))
            f.write('aud_type = "{}"\n'.format(self.audtype))
        self.process.start('python3',['gui.py'])

    def stopSubmit(self):
        return

    def getFile(self):
        self.filename=QtGui.QFileDialog.getOpenFileName()
        print(self.filename)

    def visibility(self):
        if(self.audtype=='Upload'):
            self.btnfile.setVisible(True)
        else:
            self.btnfile.setVisible(False)


    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Extract!',
                                            "Get into the chopper?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Exiting....")
            sys.exit()
        else:
            pass
