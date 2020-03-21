import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QFrame

import receiver

class OutputFrame(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setStyleSheet("QWidget{\n"
                           "    background: rgb(150, 150, 150);\n"
                           "    border: 1px solid rgb(150, 150, 150);\n"
                            "    color: white;\n"
                            "}\n"
                            "QLabel{\n"
                            "    color: white;\n"
                            "}\n")
        self.setFixedHeight(121)
        self.container = parent
        self.form = QtWidgets.QFormLayout()
        self.groupBox = QtWidgets.QGroupBox('')
        self.files = []
    
    def receiveFiles(self):
        self.container.receiver.receiveFromServer()
        self.container.showReceiverWindow()
        self.container.outputLabel.setText('sender_job.py')
        

class WaitingWindow(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(WaitingWindow, self).__init__(parent)
        self.waitingLabel = QtWidgets.QLabel(self)
        self.waitingLabel.setStyleSheet('color: white')
        self.waitingLabel.setGeometry(QtCore.QRect(135, 100, 144, 17))
        self.waitingLabel.setText('Waiting...')
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.waitingLabel.setFont(font)
        self.waitingLabel.setObjectName("waitingLabel")
        self.waitingLabel.adjustSize()

class ReceiverWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Rendt Receiver Demo')
        self.setWindowIcon(QtGui.QIcon('../../assets/img/rendt_new_logo_square.png'))
        self.resize(421, 283)
        self.setStyleSheet("QPushButton {\n"
                                "    background: rgb(232, 232, 232);\n"
                                "    border: 1px solid rgb(227, 227, 227);\n"
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

        # Setting up the 'Received Files' label
        self.label = QLabel(self)
        self.label.setText('Received Output')
        self.label.setGeometry(QtCore.QRect(30, 20, 210, 43))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")
        self.label.adjustSize()

        # Setting up output frame
        self.outputFrame = OutputFrame(self)
        self.outputFrame.setGeometry(QtCore.QRect(30, 70, 361, 121))

        # Setting up output label
        self.outputLabel = QLabel(self.outputFrame)
        self.outputLabel.setStyleSheet('color: white')
        
        font = QtGui.QFont()
        font.setFamily('Arial')
        font.setPointSize(12)

        self.outputLabel.setFont(font)

        # Adding the 'Accept' button and configuring it
        self.acceptBtn = QPushButton(self)
        self.acceptBtn.setGeometry(QtCore.QRect(320, 200, 71, 31))
        self.acceptBtn.setText('Accept')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.acceptBtn.setFont(font)
        self.acceptBtn.setStyleSheet("color: white;")
        self.acceptBtn.setObjectName("acceptBtn")

        # Setting up Waiting Screen
        self.waitingWindow = WaitingWindow(self)

        # Adding everything into the layout
        self.layout.addWidget(self.waitingWindow)
        self.layout.addWidget(self.acceptBtn)
        self.layout.addWidget(self.outputFrame)
        self.layout.addWidget(self.label)

        # Creating an instance of Receiver class
        self.receiver = receiver.Receiver()
        self.acceptBtn.clicked.connect(self.execFile)

        # Hiding the unnecessary parts
        self.acceptBtn.hide()
        self.label.hide()
        self.outputFrame.hide()
        self.outputFrame.receiveFiles()
    
    def showReceiverWindow(self):
        self.acceptBtn.show()
        self.label.show()
        self.outputFrame.show()
        self.waitingWindow.hide()
    
    def execFile(self):
        self.receiver.execute()

if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)

    window = ReceiverWindow()
    window.show()

    sys.exit(app.exec_())