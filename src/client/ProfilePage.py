from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QMainWindow

import LoginWindow

class CustomShadow(QtWidgets.QGraphicsDropShadowEffect):
    def __init__(self):
        super(CustomShadow, self).__init__()

        self.setBlurRadius(30)
        self.setXOffset(0)
        self.setYOffset(0)
        self.setColor(QtGui.QColor(30, 30, 30))

class ProfilePage(QWidget):
    def __init__(self, parent):
        super(ProfilePage, self).__init__()

        self.parent = parent

        self.current_theme = self.parent.current_theme
        self.current_font = self.parent.current_font
        self.current_sf = self.parent.current_sf
    
        self.shadow = CustomShadow()
        self.shadow1 = CustomShadow()
        self.shadow2 = CustomShadow()

        self.profileLabel = QLabel(self)
        self.profileLabel.setText('Profile')
        self.profileLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 48), 400))
        self.profileLabel.adjustSize()
        self.profileLabel.setStyleSheet(   'background: transparent;\n'
                                            'color: white;\n'
                                            'border: 0px solid black;\n'
                                            'margin-top: 50px;\n'
                                            'font-weight: bold;\n')
        self.profileLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.profileLabel.setGraphicsEffect(self.shadow)

        self.accountsLabel = QLabel(self)
        self.accountsLabel.setText('Account')
        self.accountsLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 30), 400))
        self.accountsLabel.adjustSize()
        self.accountsLabel.setStyleSheet(   'background: transparent;\n'
                                            'color: white;\n'
                                            'border: 0px solid black;\n'
                                            'font-weight: bold;\n')
        self.accountsLabel.setAlignment(QtCore.Qt.AlignHCenter)

        self.accountsRow = QWidget(self)
        self.accountsRow.setStyleSheet( 'background: rgb(124, 124, 124);\n'
                                        'border: 0px solid white;\n')
        
        self.accountsRowLayout = QVBoxLayout()
        self.accountsRowLayout.addWidget(self.accountsLabel)
        self.accountsRowLayout.setContentsMargins(20, 20, 20, 20)
        self.accountsRowLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.accountsRow.setLayout(self.accountsRowLayout)

        self.unameLabel = QLabel(self)
        self.unameLabel.setText('username: ')
        self.unameLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 24), 400))
        self.unameLabel.adjustSize()
        self.unameLabel.setStyleSheet(  'background: transparent;\n'
                                        'color: white;\n'
                                        'border: 0px solid black;\n'
                                        'font-weight: bold;\n')
        self.unameLabel.setAlignment(QtCore.Qt.AlignVCenter)

        self.unameVal = QLabel(self)
        self.unameVal.setText(self.parent.account)
        self.unameVal.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 24), 400))
        self.unameVal.adjustSize()
        self.unameVal.setStyleSheet(  'background: transparent;\n'
                                        'color: rgb(255, 241, 118);\n'
                                        'border: 0px solid black;\n'
                                        'font-weight: bold;\n')
        self.unameVal.setAlignment(QtCore.Qt.AlignVCenter)

        self.accountRow = QWidget(self)
        self.accountRow.setStyleSheet('background: transparent;\n'
                                    'border: 0px solid white;\n')
        
        self.accountRowLayout = QHBoxLayout()
        self.accountRowLayout.addWidget(self.unameLabel, alignment = QtCore.Qt.AlignRight)
        self.accountRowLayout.addWidget(self.unameVal, alignment = QtCore.Qt.AlignLeft)
        self.accountRowLayout.setSpacing(10)
        self.accountRowLayout.setContentsMargins(0, 0, 0, 0)
        self.accountRowLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.accountRow.setLayout(self.accountRowLayout)



        self.emailLabel = QLabel(self)
        self.emailLabel.setText('email: ')
        self.emailLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 24), 400))
        self.emailLabel.adjustSize()
        self.emailLabel.setStyleSheet(  'background: transparent;\n'
                                        'color: white;\n'
                                        'border: 0px solid black;\n'
                                        'font-weight: bold;\n')
        self.emailLabel.setAlignment(QtCore.Qt.AlignVCenter)

        self.emailVal = QLabel(self)
        self.emailVal.setText(self.parent.accountEmail)
        self.emailVal.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 24), 400))
        self.emailVal.adjustSize()
        self.emailVal.setStyleSheet(  'background: transparent;\n'
                                        'color: rgb(255, 241, 118);\n'
                                        'border: 0px solid black;\n'
                                        'font-weight: bold;\n')
        self.emailVal.setAlignment(QtCore.Qt.AlignVCenter)

        self.emailRow = QWidget(self)
        self.emailRow.setStyleSheet('background: transparent;\n'
                                    'border: 0px solid white;\n')
        
        self.emailRowLayout = QHBoxLayout()
        self.emailRowLayout.addWidget(self.emailLabel, alignment = QtCore.Qt.AlignRight)
        self.emailRowLayout.addWidget(self.emailVal, alignment = QtCore.Qt.AlignLeft)
        self.emailRowLayout.setSpacing(10)
        self.emailRowLayout.setContentsMargins(0, 0, 0, 0)
        self.emailRowLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.emailRow.setLayout(self.emailRowLayout)

        self.logOutBtn = QPushButton
        self.logOutBtn = QPushButton(self)
        self.logOutBtn.setStyleSheet('QPushButton {\n'
                                     '   background: rgb(246, 49, 49);\n'
                                     '   color: white;\n'
                                     '   border: 0px solid black;\n'
                                     '   margin: 20px;\n'
                                     '}\n'
                                     'QPushButton:hover {\n'
                                     '   background: rgb(200, 39, 39);\n'
                                     '}\n'
                                     'QPushButton:pressed {\n'
                                     '   background: rgb(123, 25, 25);\n'
                                     '}\n')
        self.logOutBtn.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 18), 400))
        self.logOutBtn.setText('Log Out')
        self.logOutBtn.setFixedHeight(95)
        self.logOutBtn.setFixedWidth(205)
        self.logOutBtn.setGraphicsEffect(self.shadow2)
        self.logOutBtn.clicked.connect(self.logOut)

        self.box = QWidget(self)

        self.boxLayout = QVBoxLayout()
        self.boxLayout.addWidget(self.accountsRow)
        self.boxLayout.addWidget(self.accountRow)
        self.boxLayout.addWidget(self.emailRow)
        self.boxLayout.addWidget(self.logOutBtn, alignment = QtCore.Qt.AlignCenter)
        self.boxLayout.setAlignment(QtCore.Qt.AlignTop)
        self.boxLayout.setContentsMargins(0, 0, 0, 0)
        self.boxLayout.setSpacing(20)
        self.box.setLayout(self.boxLayout)
        self.box.setGraphicsEffect(self.shadow1)
        self.box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.box.setMaximumWidth(1200)
        self.box.setMinimumWidth(1000)

        layout = QVBoxLayout()
        layout.addWidget(self.profileLabel, alignment = QtCore.Qt.AlignHCenter)
        layout.addWidget(self.box, alignment = QtCore.Qt.AlignHCenter)
        layout.setContentsMargins(50, 0, 50, 50)
        layout.setSpacing(30)
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.widget = QWidget(self)
        self.widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.widget.setLayout(layout)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.widget)
        self.layout.setAlignment(QtCore.Qt.AlignHCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        if (self.current_theme == 'Dark'):
            self.darkTheme()
        elif (self.current_theme == 'Light'):
            self.lightTheme()
        else:
            self.classicTheme()

    def logOut(self, e):
        self.parent.t1.stop()
        self.parent.t1.join()
    
        self.parent.receiver.sign_out()

        self.hide()
        self.parent.hide()
        self.parent.parent.close()
        loginWindow = LoginWindow.LoginWindow()
        loginWindow.show()
        

    def darkTheme(self):
        self.widget.setStyleSheet(  'background: rgb(69, 69, 69);\n'
                                    'color: white;\n'
                                    'border: 0px solid white;\n')
        self.box.setStyleSheet('background: rgb(71, 71, 71);\n')
        self.accountsRow.setStyleSheet(     'background: rgb(124, 124, 124);\n'
                                            'border: 0px solid white;\n')

    def lightTheme(self):
        self.widget.setStyleSheet(  'background: rgb(204, 204, 204);\n'
                                    'color: white;\n'
                                    'border: 0px solid black;\n')
        self.box.setStyleSheet('background: rgb(140, 140, 140);\n')
        self.accountsRow.setStyleSheet(     'background: rgb(100, 100, 100);\n'
                                            'border: 0px solid white;\n')

    def classicTheme(self):
        self.widget.setStyleSheet(  'background: rgb(0, 23, 37);\n'
                                    'color: white;\n'
                                    'border: 0px solid white;\n')
        self.box.setStyleSheet('background: rgba(255, 255, 255, 0.1);\n')
        self.accountsRow.setStyleSheet(     'background: rgba(255, 255, 255, 0.2);\n'
                                            'border: 0px solid white;\n')