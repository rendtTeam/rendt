import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QMainWindow

from LoginWindow import LoginWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.loginPage.emailField.setText('cenk.er98@hotmail.com')
    window.loginPage.passField.setText('270898Cee')
    window.loginPage.goToLogin()
    window.show()
    sys.exit(app.exec_())