from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QMainWindow

class TestPage(QWidget):
    def __init__(self):
        super(TestPage, self).__init__()

        self.r = 100
        self.g = 100
        self.b = 100
        self.isMax = False
        self.isMin = True
        c = 0

        # self.resize(800, 600)
        self.setStyleSheet('background: rgb(' + str(self.r) + ', ' + str(self.g) + ', ' + str(self.b) + ');')
        label = QLabel(self)
        label.setFont(QtGui.QFont('Arial', 96, 10000))
        label.setStyleSheet('color: white')
        label.setText('Executing')
        label.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        
        timer = QtCore.QTimer(
            self, 
            interval=1, 
            timeout=self.changeColor
        )

        timer.start()

    @QtCore.pyqtSlot()
    def changeColor(self):
        if (not self.isMax):
            if (self.r < 255):
                self.r += 1
            elif (self.g < 255):
                self.g += 1
            elif (self.b < 255):
                self.b += 1
            else:
                self.isMax = True
                self.isMin = False

        if (not self.isMin):
            if (self.r > 0):
                self.r -= 1
            elif (self.g > 0):
                self.g -= 1
            elif (self.b > 0):
                self.b -= 1
            else:
                self.isMax = False
                self.isMin = True
        self.setStyleSheet('background: rgb(' + str(self.r) + ', ' + str(self.g) + ', ' + str(self.b) + ');')