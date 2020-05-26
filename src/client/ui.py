import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QMainWindow

from LoginWindow import LoginWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.loginPage.emailField.setText('zxyctn@gmail.com')
    window.loginPage.passField.setText('123456')
    window.loginPage.goToLogin()
    window.show()
    sys.exit(app.exec_())