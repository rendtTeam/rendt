import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget

import sender
import receiver


class TaskFinishedWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel(self)
        label.setText('Task finished successfully')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)

        label.setFont(font)
        label.adjustSize()

        self.label = label
        self.label.setGeometry(QtCore.QRect(135, 100, 144, 17))

        self.layout = layout
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


class ReceivedWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel(self)
        label.setText('Files successfully received')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)

        label.setFont(font)
        label.adjustSize()

        self.label = label
        self.label.setGeometry(QtCore.QRect(135, 100, 144, 17))

        self.layout = layout
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


class WaitingWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WaitingWindow, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout()
        
        self.waitingLabel = QtWidgets.QLabel(self)
        self.waitingLabel.setStyleSheet('color: white')
        self.waitingLabel.setGeometry(QtCore.QRect(135, 100, 144, 17))
        self.waitingLabel.setText('Waiting...')

        self.backBtn = QPushButton(self)
        self.backBtn.setGeometry(QtCore.QRect(0, 0, 20, 20))
        self.backBtn.setText('<')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.clicked.connect(parent.goBack)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.waitingLabel.setFont(font)
        self.waitingLabel.setObjectName("waitingLabel")
        self.waitingLabel.adjustSize()

        self.layout.addWidget(self.backBtn)
        self.layout.addWidget(self.waitingLabel)

    def filesReceivedWindow(self):
        self.receivedWindow = ReceivedWindow()
        self.waitingLabel.hide()
        self.layout.addWidget(self.receivedWindow)


class ReceiverWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.container = parent
        self.started = False
    
    def startWindow(self):
        self.started = True
        self.container.setWindowTitle('Rendt Receiver Demo')
        self.setWindowIcon(QtGui.QIcon(
            '../../assets/img/rendt_new_logo_square.png'))
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setStyleSheet("QPushButton {\n"
                           "    background: rgb(232, 232, 232);\n"
                           "    border: 1px solid rgb(227, 227, 227);\n"
                           "    color: white;\n"
                           "}\n"
                           "\n"
                           "QPushButton:hover {\n"
                           "    background: rgb(200, 200, 200);\n"
                           "}\n"
                           "\n"
                           "QPushButton:pressed {\n"
                           "    background: rgb(150, 150, 150);\n"
                           "}\n"
                           "\n"
                           "QWidget {\n"
                           "    background: rgb(120, 120, 120);\n"
                           "}\n"
                           "\n"
                           "")

        # Setting up the layout
        self.layout = QVBoxLayout()

        # Adding back button
        self.backBtn = QPushButton(self)
        self.backBtn.setGeometry(QtCore.QRect(0, 0, 20, 20))
        self.backBtn.setText('<')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.clicked.connect(self.goBack)
        self.backBtn.hide()

        # Setting up Waiting Screen
        self.waitingWindow = WaitingWindow(self)

        # Setting up Received Window
        self.receivedWindow = ReceivedWindow()
        self.receivedWindow.hide()

        # Setting up Task Finished Window
        self.taskFinishedWindow = TaskFinishedWindow()
        self.taskFinishedWindow.hide()

        # Adding everything into the layout
        self.layout.addWidget(self.backBtn)
        self.layout.addWidget(self.waitingWindow)
        self.layout.addWidget(self.receivedWindow)
        self.layout.addWidget(self.taskFinishedWindow)

        self.setLayout(self.layout)

        # self.receiveAndExecute()

    def receiveAndExecute(self):
        self.receiver = receiver.Receiver()

        # Show received message
        self.waitingWindow.hide()
        self.receivedWindow.show()

        # Show execution finished
        self.receiver.execute()
        self.receivedWindow.hide()
        self.taskFinishedWindow.show()
    
    def goBack(self):
        self.hideWindow()
        self.container.resetUi()
    
    def hideWindow(self):
        self.waitingWindow.hide()
        self.receivedWindow.hide()
        self.taskFinishedWindow.hide()
        self.backBtn.hide()

    def showWindow(self):
        self.container.setWindowTitle('Rendt Receiver Demo')
        self.waitingWindow.show()


class FileButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.file_src = ''

    def setFileSource(self, e):
        self.file_src = e

    def getFileSource(self):
        return self.file_src


class ScrollFrame(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.form = QtWidgets.QFormLayout()
        self.setFixedHeight(121)
        self.container = parent
        self.groupBox = QtWidgets.QGroupBox('')
        self.files = []

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
            print('Accepted')
        else:
            e.ignore()
            print('Ignored')
        self.setStyleSheet("background: rgb(30, 136, 229);\n"
                           "border: 1px solid rgb(25, 118, 210);\n"
                           "color: white")

    def dragLeaveEvent(self, e):
        self.setStyleSheet("background: rgb(150, 150, 150);\n"
                           "border: 1px solid rgb(150, 150, 150);\n"
                           "color: white")

    def dropEvent(self, e):
        self.setStyleSheet("QScrollArea{\n"
                           "    color: white;\n"
                           "}\n"
                           "QLabel{\n"
                           "    color: white;\n"
                           "}\n"
                           "QPushButton {\n"
                           "    background: rgb(232, 232, 232);\n"
                           "    color: white;\n"
                           "    border: 1px solid rgb(227, 227, 227);\n"
                           "}\n"
                           "\n"
                           "QPushButton:hover {\n"
                           "    background: rgb(255,0,0);\n"
                           "    border: 1px solid rgb(255,0,0);\n"
                           "}\n"
                           "\n"
                           "QPushButton:pressed {\n"
                           "    background: rgb(182,0,0);\n"
                           "    border: 1px solid rgb(182,0,0);\n"
                           "}\n"
                           "\n"
                           "QWidget {\n"
                           "    background: rgb(120, 120, 120);\n"
                           "}\n"
                           "\n"
                           "")
        if (self.form.rowCount() == 0):
            self.container.switchLabel(False)

        for url in e.mimeData().urls():
            f, file_src = str(url.toString()).split('///')
            file_dir, file_name = os.path.split(file_src)

            print(file_src)
            label = QLabel(file_name)
            btn = FileButton('Remove')

            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)

            label.setFont(font)
            label.setFixedWidth(270)
            btn.setFont(font)
            btn.setFixedWidth(50)
            btn.setFixedHeight(20)

            btn.setFileSource(str(file_src))

            btn.clicked.connect(self.clickedRemove)

            self.form.addRow(label, btn)

        self.groupBox.setLayout(self.form)
        self.setWidget(self.groupBox)

    def clickedRemove(self):
        self.form.removeRow(self.sender())

        if (self.form.rowCount() == 0):
            self.container.switchLabel(True)

    def uploadFiles(self):
        for i in range(self.form.rowCount() * 2):
            if (i % 2):
                self.files.append(self.form.itemAt(i).widget().getFileSource())

        for f in self.files:
            print(f'File: {f}')
            self.container.sender.sendToServer(f)
        data = ''
        with open('received_output.txt') as f:
            for i, l in enumerate(f):
                self.container.outputFrame.addLine(l)

        self.container.loadingWindow.hide()
        self.container.outputFrame.show()
        self.container.outputDetailsLabel.show()


class OutputFrame(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.form = QtWidgets.QFormLayout()
        self.setFixedHeight(121)
        self.container = parent
        self.groupBox = QtWidgets.QGroupBox('')
        self.files = []

    def addLine(self, e):
        label = QLabel(e)
        label.setStyleSheet('color: white')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        label.setFont(font)
        label.setFixedHeight(14)
        label.adjustSize()

        self.form.addRow(label)
        self.groupBox.setLayout(self.form)
        self.setWidget(self.groupBox)


class LoadingWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LoadingWindow, self).__init__(parent)
        self.loadingLabel = QtWidgets.QLabel(self)
        self.loadingLabel.setStyleSheet('color: white')
        self.loadingLabel.setGeometry(QtCore.QRect(135, 100, 144, 17))
        self.loadingLabel.setText('Loading...')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.loadingLabel.setFont(font)
        self.loadingLabel.setObjectName("loadingLabel")
        self.loadingLabel.adjustSize()


class UploadFinishedWindow(QWidget):
    def __init__(self):
        super().__init__()

    def startWindow(self):
        self.layout = QVBoxLayout()

        self.label = QLabel(self)
        self.label.setText('Files uploaded successfully')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)

        self.label.setFont(font)
        self.label.adjustSize()
        self.label.setGeometry(QtCore.QRect(135, 100, 144, 30))

        self.downloadId = QLabel(self)
        self.downloadId.setText('Job ID: ')
        self.downloadId.setFont(QtGui.QFont('Arial', 20))
        self.downloadId.setGeometry(QtCore.QRect(150, 130, 144, 22))
        self.downloadId.adjustSize()
        # TODO: Set self.downloadId text to the Job ID received from server

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.downloadId)
        self.setLayout(self.layout)


class DownloadWindow(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.container = parent
        self.layout = QVBoxLayout()
        self.setStyleSheet('color: white')

        self.label = QLabel(self)
        self.label.setText('Download executed files with Job ID')
        self.label.setFont(QtGui.QFont('Arial', 20))
        self.label.setGeometry(QtCore.QRect(50, 60, 20, 22))
        self.label.adjustSize()

        self.jobIdLabel = QLabel(self)
        self.jobIdLabel.setText('Job ID: ')
        self.jobIdLabel.setFont(QtGui.QFont('Arial', 14))
        self.jobIdLabel.setGeometry(QtCore.QRect(50, 100, 20, 16))
        self.jobIdLabel.adjustSize()

        self.jobId = QtWidgets.QLineEdit(self)
        self.jobId.setFont(QtGui.QFont('Arial', 14))
        self.jobId.setStyleSheet(   'background: white;\n'
                                    'border: 1px solid transparent;\n'
                                    'color: black;\n')
        self.jobId.setGeometry(QtCore.QRect(100, 100, 100, 16))

        self.sendBtn = QPushButton(self)
        self.sendBtn.setText('Send')
        self.sendBtn.setFont(QtGui.QFont('Arial', 12))
        self.sendBtn.setStyleSheet( "QPushButton:hover {\n"
                                    "    background: rgb(200, 200, 200);\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:pressed {\n"
                                    "    background: rgb(150, 150, 150);\n"
                                    "}\n"
                                    "QPushButton {\n"
                                    "   background: transparent;\n"
                                    "   border: 1px solid rgb(227, 227, 227);\n"
                                    "   color: white;\n}\n")
        self.sendBtn.setGeometry(QtCore.QRect(202, 100, 50, 16))

        # Adding back button
        self.backBtn = QPushButton(self)
        self.backBtn.setGeometry(QtCore.QRect(0, 0, 20, 20))
        self.backBtn.setText('<')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.clicked.connect(self.container.goBack)

        # Adding download files button
        self.uploadBtn = QPushButton(self)
        self.uploadBtn.setText('Upload')
        self.uploadBtn.setFont(QtGui.QFont('Arial', 12))
        self.uploadBtn.setGeometry(22, 0, 50, 20)
        self.uploadBtn.clicked.connect(self.startUploadWindow)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.jobIdLabel)
        self.layout.addWidget(self.jobId)
        self.layout.addWidget(self.sendBtn)
        self.layout.addWidget(self.backBtn)
        self.layout.addWidget(self.uploadBtn)

        # self.setLayout(self.layout)

    def startUploadWindow(self):
        self.destroy()
        self.container.resetUi()

class SenderWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.container = parent
        self.started = False

    def startWindow(self):
        self.started = True
        self.container.setWindowTitle('Rendt Sender Demo')
        self.setWindowIcon(QtGui.QIcon(
            '../../assets/img/rendt_new_logo_square.png'))
        # self.resize(600, 300)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setStyleSheet("QPushButton {\n"
                           "    background: rgb(232, 232, 232);\n"
                           "    border: 1px solid rgb(227, 227, 227);\n"
                           "    color: white;\n"
                           "}\n"
                           "\n"
                           "QPushButton:hover {\n"
                           "    background: rgb(200, 200, 200);\n"
                           "}\n"
                           "\n"
                           "QPushButton:pressed {\n"
                           "    background: rgb(150, 150, 150);\n"
                           "}\n"
                           "\n"
                           "QWidget {\n"
                           "    background: rgb(120, 120, 120);\n"
                           "}\n"
                           "\n"
                           "")

        # Setting up the layout
        self.layout = QVBoxLayout()

        # Adding back button
        self.backBtn = QPushButton(self)
        self.backBtn.setGeometry(QtCore.QRect(0, 0, 20, 20))
        self.backBtn.setText('<')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.clicked.connect(self.goBack)

        # Adding download files button
        self.downloadBtn = QPushButton(self)
        self.downloadBtn.setText('Download')
        self.downloadBtn.setFont(QtGui.QFont('Arial', 12))
        self.downloadBtn.setGeometry(22, 0, 70, 20)
        self.downloadBtn.clicked.connect(self.startDownloadWindow)

        # Setting up the label and configuring it
        self.label = QLabel(self)
        self.label.setText('Drag & Drop')
        self.label.setGeometry(QtCore.QRect(30, 20, 210, 43))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")

        # Adding Scroll Frame where the Dragging and Dropping will happen
        self.scroll = ScrollFrame(self)
        self.scroll.setGeometry(QtCore.QRect(30, 70, 361, 121))
        self.scroll.setStyleSheet("background: rgb(150, 150, 150);\n"
                                  "border: 1px solid rgb(150, 150, 150);\n")
        self.scroll.setWidgetResizable(True)

        # Adding Download Window
        self.downloadWindow = DownloadWindow(self)
        self.downloadWindow.hide()

        # Setting up the label inside the frame and configuring it
        self.uploadLabel = QLabel(self.scroll)
        self.uploadLabel.setStyleSheet('color: white')
        self.uploadLabel.setGeometry(QtCore.QRect(100, 50, 144, 17))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)

        self.uploadLabel.setFont(font)
        self.uploadLabel.setObjectName("uploadLabel")
        self.uploadLabel.setText('Drag & Drop files here')
        self.uploadLabel.adjustSize()

        # Adding the 'Upload' button and configuring it
        self.uploadBtn = QPushButton(self)
        self.uploadBtn.setGeometry(QtCore.QRect(320, 200, 71, 31))
        self.uploadBtn.setText('Upload')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.uploadBtn.setFont(font)
        self.uploadBtn.setStyleSheet("color: white;")
        self.uploadBtn.setObjectName("uploadBtn")
        self.uploadBtn.clicked.connect(self.startLoadingWindow)

        # Setting up Loading Screen
        self.loadingWindow = LoadingWindow(self)
        self.loadingWindow.hide()

        # Adding Output Details Label
        self.outputDetailsLabel = QLabel(self)
        self.outputDetailsLabel.setText('Received Output')
        self.outputDetailsLabel.setGeometry(QtCore.QRect(30, 20, 210, 43))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.outputDetailsLabel.setFont(font)
        self.outputDetailsLabel.setStyleSheet("color: white;")
        self.outputDetailsLabel.adjustSize()
        self.outputDetailsLabel.hide()

        # Adding Ouput Frame
        self.outputFrame = OutputFrame(self)
        self.outputFrame.setGeometry(QtCore.QRect(30, 70, 361, 121))
        self.outputFrame.setStyleSheet("background: rgb(150, 150, 150);\n"
                                       "border: 1px solid rgb(150, 150, 150);\n")
        self.outputFrame.setWidgetResizable(True)
        self.outputFrame.hide()

        # Adding Upload Finished Window
        self.uploadFinishedWindow = UploadFinishedWindow()
        self.uploadFinishedWindow.hide()

        # Adding everything into the layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.uploadLabel)
        self.layout.addWidget(self.uploadBtn)
        self.layout.addWidget(self.loadingWindow)
        self.layout.addWidget(self.outputDetailsLabel)
        self.layout.addWidget(self.outputFrame)
        self.layout.addWidget(self.uploadFinishedWindow)
        self.layout.addWidget(self.backBtn)
        self.layout.addWidget(self.downloadWindow)

        # Creating Sender class instance
        self.sender = sender.Sender()
    
    def startDownloadWindow(self):
        self.label.hide()
        self.scroll.hide()
        self.uploadLabel.hide()
        self.uploadBtn.hide()
        self.backBtn.hide()
        self.downloadBtn.hide()
        self.downloadWindow.show()

    def startLoadingWindow(self):
        self.label.hide()
        self.scroll.hide()
        self.uploadLabel.hide()
        self.uploadBtn.hide()
        self.loadingWindow.show()
        self.startUploadFinishedWindow()

    def startUploadFinishedWindow(self):
        self.scroll.uploadFiles()
        self.loadingWindow().hide()
        self.uploadFinishedWindow()

    def switchLabel(self, flag):
        if (flag):
            self.uploadLabel.show()
        else:
            self.uploadLabel.hide()
    
    def goBack(self):
        self.container.resetUi()
    
    def resetUi(self):
        self.downloadWindow.hide()
        self.label.show()
        self.scroll.show()
        self.uploadLabel.show()
        self.uploadBtn.show()
        self.backBtn.show()
        self.downloadBtn.show()
    
    def hideWindow(self):
        self.label.hide()
        self.scroll.hide()
        self.uploadLabel.hide()
        self.uploadBtn.hide()
        self.backBtn.hide()
        self.downloadBtn.hide()
        self.downloadWindow.hide()
        self.uploadFinishedWindow.hide()
        self.loadingWindow.hide()
        self.outputDetailsLabel.hide()
        self.outputFrame.hide()
    
    def showWindow(self):
        self.container.setWindowTitle('Rendt Sender Demo')
        self.label.show()
        self.scroll.show()
        self.uploadLabel.show()
        self.uploadBtn.show()
        self.backBtn.show()
        self.downloadBtn.show()


class RenterButton(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.container = parent
        self.layout = QVBoxLayout()
        self.setStyleSheet('QWidget {\nbackground: transparent;\n'
                           'border: 1px solid white;\n'
                           'border-radius: 10px;\n'
                           'color: white;\n}\n'
                           'QWidget:hover {\n'
                           'background: rgba(100, 100, 100, 0.3)\n}\n'
                           'QWidget:clicked {\n'
                           'background: rgba(50, 50, 50, 0.3)\n}\n')

        self.label = QLabel(self)
        self.label.setText('rent')
        self.label.setFont(QtGui.QFont('Arial', 36))
        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.adjustSize()

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setMouseTracking(True)
        self.clicked = self.container.startSenderWindow

    def mousePressEvent(self, e):
        self.clicked()
    
    def changeClickedEvent(self, e):
        self.clicked = e


class LeaserButton(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.container = parent
        self.layout = QVBoxLayout()
        self.setStyleSheet('QWidget {\nbackground: transparent;\n'
                           'border: 1px solid white;\n'
                           'border-radius: 10px;\n'
                           'color: white;\n}\n'
                           'QWidget:hover {\n'
                           'background: rgba(100, 100, 100, 0.3)\n}\n'
                           'QWidget:clicked {\n'
                           'background: rgba(50, 50, 50, 0.3)\n}\n')

        self.label = QLabel(self)
        self.label.setText('lease')
        self.label.setFont(QtGui.QFont('Arial', 36))
        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.adjustSize()

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setMouseTracking(True)
        self.clicked = self.container.startReceiverWindow

    def mousePressEvent(self, e):
        self.clicked()

    def changeClickedEvent(self, e):
        self.clicked = e

class RenterLeiserWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon(
            '../../assets/img/rendt_new_logo_square.png'))
        self.setWindowTitle('rendt')

        self.resize(440, 283)
        self.setStyleSheet('background: rgb(120, 120, 120);\n'
                           'color: white;\n')

        self.layout = QtWidgets.QHBoxLayout()
        self.senderButton = RenterButton(self)
        self.receiverButton = LeaserButton(self)

        self.senderWindow = SenderWindow(self)
        self.receiverWindow = ReceiverWindow(self)

        self.senderWindow.hide()
        self.receiverWindow.hide()

        self.layout.addWidget(self.senderButton)
        self.layout.addWidget(self.receiverButton)
        self.layout.addWidget(self.senderWindow)
        self.layout.addWidget(self.receiverWindow)
        self.setLayout(self.layout)

    def startSenderWindow(self):
        self.senderButton.hide()
        self.receiverButton.hide()
        self.senderWindow.startWindow()
        self.senderWindow.show()
    
    def startReceiverWindow(self):
        self.senderButton.hide()
        self.receiverButton.hide()
        self.receiverWindow.startWindow()
        self.receiverWindow.show()
    
    def showSenderWindow(self):
        self.senderButton.hide()
        self.receiverButton.hide()
        self.senderWindow.showWindow()
        self.senderWindow.show()
    
    def showReceiverWindow(self):
        self.senderButton.hide()
        self.receiverButton.hide()
        self.receiverWindow.showWindow()
        self.receiverWindow.show()

    def resetUi(self):
        self.setWindowTitle('rendt')
        self.senderButton.show()
        self.receiverButton.show()
        self.senderWindow.hide()
        self.receiverWindow.hide()

        if (self.senderWindow.started):
            self.senderWindow.hideWindow()
            self.senderButton.changeClickedEvent(self.showSenderWindow)
        
        if (self.receiverWindow.started):
            self.receiverWindow.hideWindow()
            self.receiverButton.changeClickedEvent(self.showReceiverWindow)

if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)

    window = RenterLeiserWindow()
    window.show()

    sys.exit(app.exec_())
