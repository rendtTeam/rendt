import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QMainWindow

import LoginWindow

def init():
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_DisableHighDpiScaling, True)
    window = LoginWindow.LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    init()