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

class SettingsPage(QWidget):
    def __init__(self, parent):
        super(SettingsPage, self).__init__()

        self.parent = parent

        self.current_theme = self.parent.current_theme
        self.current_font = self.parent.current_font
        self.current_sf = self.parent.current_sf
    
        self.shadow = CustomShadow()
        self.shadow1 = CustomShadow()
        self.shadow2 = CustomShadow()

        self.settingsLabel = QLabel(self)
        self.settingsLabel.setText('Settings')
        self.settingsLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 48), 400))
        self.settingsLabel.adjustSize()
        self.settingsLabel.setStyleSheet(   'background: transparent;\n'
                                            'color: white;\n'
                                            'border: 0px solid black;\n'
                                            'margin-top: 50px;\n'
                                            'font-weight: bold;\n')
        self.settingsLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.settingsLabel.setGraphicsEffect(self.shadow)

        self.customLabel = QLabel(self)
        self.customLabel.setText('Customization')
        self.customLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 30), 400))
        self.customLabel.adjustSize()
        self.customLabel.setStyleSheet(   'background: transparent;\n'
                                            'color: white;\n'
                                            'border: 0px solid black;\n'
                                            'font-weight: bold;\n')
        self.customLabel.setAlignment(QtCore.Qt.AlignHCenter)

        self.customRow = QWidget(self)
        
        self.customRowLayout = QVBoxLayout()
        self.customRowLayout.addWidget(self.customLabel)
        self.customRowLayout.setContentsMargins(20, 20, 20, 20)
        self.customRowLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.customRow.setLayout(self.customRowLayout)

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

        self.themeLabel = QLabel(self)
        self.themeLabel.setText('Theme')
        self.themeLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 24), 400))
        self.themeLabel.adjustSize()
        self.themeLabel.setStyleSheet(  'background: transparent;\n'
                                        'color: white;\n'
                                        'border: 0px solid black;\n'
                                        'font-weight: bold;\n')
        self.themeLabel.setAlignment(QtCore.Qt.AlignVCenter)

        self.themeDropdown = QtWidgets.QComboBox(self)
        self.themeDropdown.setStyleSheet(   'background: rgb(124, 124, 124);\n'
                                            'color: white;\n'
                                            'border: 0px solid white;\n'
                                            'padding-left: 10px;\n')
        self.themeDropdown.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 18), 400))
        self.themeDropdown.setFixedHeight(50)
        self.themeDropdown.setFixedWidth(200)
        self.themeDropdown.addItem('Dark')
        self.themeDropdown.addItem('Light')
        self.themeDropdown.addItem('Classic')
        self.themeDropdown.currentTextChanged.connect(self.changeTheme)

        self.themeRow = QWidget(self)
        self.themeRow.setStyleSheet('background: transparent;\n'
                                    'border: 0px solid white;\n')
        
        self.themeRowLayout = QHBoxLayout()
        self.themeRowLayout.addWidget(self.themeLabel, alignment = QtCore.Qt.AlignRight)
        self.themeRowLayout.addWidget(self.themeDropdown, alignment = QtCore.Qt.AlignLeft)
        self.themeRowLayout.setSpacing(10)
        self.themeRowLayout.setContentsMargins(0, 0, 0, 0)
        self.themeRowLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.themeRow.setLayout(self.themeRowLayout)

        self.fontLabel = QLabel(self)
        self.fontLabel.setText('Font')
        self.fontLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 24), 400))
        self.fontLabel.adjustSize()
        self.fontLabel.setStyleSheet(  'background: transparent;\n'
                                        'color: white;\n'
                                        'border: 0px solid black;\n'
                                        'font-weight: bold;\n')
        self.fontLabel.setAlignment(QtCore.Qt.AlignVCenter)

        self.fontDropdown = QtWidgets.QComboBox(self)
        self.fontDropdown.setStyleSheet('background: rgb(124, 124, 124);\n'
                                        'color: white;\n'
                                        'border: 0px solid white;\n'
                                        'padding-left: 10px;\n')
        self.fontDropdown.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 18), 400))
        self.fontDropdown.setFixedHeight(50)
        self.fontDropdown.setFixedWidth(200)
        self.fontDropdown.addItem('Arial')
        self.fontDropdown.addItem('Calibri')
        self.fontDropdown.addItem('Cambria')
        self.fontDropdown.addItem('Comic Sans MS')
        self.fontDropdown.addItem('Impact')
        self.fontDropdown.addItem('Times New Roman')
        self.fontDropdown.currentTextChanged.connect(self.changeFont)

        self.fontRow = QWidget(self)
        self.fontRow.setStyleSheet( 'background: transparent;\n'
                                    'border: 0px solid white;\n')
        
        self.fontRowLayout = QHBoxLayout()
        self.fontRowLayout.addWidget(self.fontLabel, alignment = QtCore.Qt.AlignRight)
        self.fontRowLayout.addWidget(self.fontDropdown, alignment = QtCore.Qt.AlignLeft)
        self.fontRowLayout.setSpacing(10)
        self.fontRowLayout.setContentsMargins(0, 0, 0, 0)
        self.fontRowLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.fontRow.setLayout(self.fontRowLayout)


        self.sfLabel = QLabel(self)
        self.sfLabel.setText('Scaling')
        self.sfLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 24), 400))
        self.sfLabel.adjustSize()
        self.sfLabel.setStyleSheet(  'background: transparent;\n'
                                        'color: white;\n'
                                        'border: 0px solid black;\n'
                                        'font-weight: bold;\n')
        self.sfLabel.setAlignment(QtCore.Qt.AlignVCenter)

        self.sfDropdown = QtWidgets.QComboBox(self)
        self.sfDropdown.setStyleSheet('background: rgb(124, 124, 124);\n'
                                        'color: white;\n'
                                        'border: 0px solid white;\n'
                                        'padding-left: 10px;\n')
        self.sfDropdown.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 18), 400))
        self.sfDropdown.setFixedHeight(50)
        self.sfDropdown.setFixedWidth(200)
        self.sfDropdown.addItem('100%')
        self.sfDropdown.addItem('125%')
        self.sfDropdown.addItem('150%')
        self.sfDropdown.addItem('200%')
        self.sfDropdown.currentTextChanged.connect(self.changeSf)

        self.sfRow = QWidget(self)
        self.sfRow.setStyleSheet( 'background: transparent;\n'
                                    'border: 0px solid white;\n')
        
        self.sfRowLayout = QHBoxLayout()
        self.sfRowLayout.addWidget(self.sfLabel, alignment = QtCore.Qt.AlignRight)
        self.sfRowLayout.addWidget(self.sfDropdown, alignment = QtCore.Qt.AlignLeft)
        self.sfRowLayout.setSpacing(10)
        self.sfRowLayout.setContentsMargins(0, 0, 0, 0)
        self.sfRowLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.sfRow.setLayout(self.sfRowLayout)


        self.accountLabel = QLabel(self)
        self.accountLabel.setText('account')
        self.accountLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 18), 400))
        self.accountLabel.adjustSize()
        self.accountLabel.setStyleSheet('background: transparent;\n'
                                        'color: white;\n'
                                        'border: 0px solid black;\n'
                                        'font-weight: bold;\n')
        self.accountLabel.setAlignment(QtCore.Qt.AlignVCenter)

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

        self.accountRow = QWidget(self)
        self.accountRow.setStyleSheet(  'background: transparent;\n'
                                        'border: 0px solid white;\n')
        
        self.accountRowLayout = QHBoxLayout()
        self.accountRowLayout.addWidget(self.accountLabel, alignment = QtCore.Qt.AlignRight)
        self.accountRowLayout.addWidget(self.logOutBtn, alignment = QtCore.Qt.AlignLeft)
        self.accountRowLayout.setSpacing(10)
        self.accountRowLayout.setContentsMargins(0, 0, 0, 0)
        self.accountRowLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.accountRow.setLayout(self.accountRowLayout)

        self.box = QWidget(self)

        self.boxLayout = QVBoxLayout()
        self.boxLayout.addWidget(self.customRow)
        self.boxLayout.addWidget(self.themeRow)
        self.boxLayout.addWidget(self.fontRow)
        self.boxLayout.addWidget(self.sfRow)
        self.boxLayout.addWidget(self.accountsRow)
        self.boxLayout.addWidget(self.accountRow)
        self.boxLayout.setAlignment(QtCore.Qt.AlignTop)
        self.boxLayout.setContentsMargins(0, 0, 0, 0)
        self.boxLayout.setSpacing(20)
        self.box.setLayout(self.boxLayout)
        self.box.setGraphicsEffect(self.shadow1)
        self.box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.box.setMaximumWidth(1200)
        self.box.setMinimumWidth(1000)

        layout = QVBoxLayout()
        layout.addWidget(self.settingsLabel, alignment = QtCore.Qt.AlignHCenter)
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

    def setCurrentSettings(self, theme, font, sf):
        self.themeDropdown.setCurrentText(theme)
        self.fontDropdown.setCurrentText(font)
        if (sf == 1):
            self.sfDropdown.setCurrentText('100%')
        elif (sf == 1.25):
            self.sfDropdown.setCurrentText('125%')
        elif (sf == 1.5):
            self.sfDropdown.setCurrentText('150%')
        else:
            self.sfDropdown.setCurrentText('200%')

    def changeTheme(self, e):
        self.parent.current_theme = self.themeDropdown.currentText()
        self.current_theme = self.parent.current_theme
        
        if (self.current_theme == 'Dark'):
            self.darkTheme()
            self.parent.darkTheme()
        elif (self.current_theme == 'Light'):
            self.lightTheme()
            self.parent.lightTheme()
        else:
            self.classicTheme()
            self.parent.classicTheme()
    
    def changeSf(self, e):
        if (self.sfDropdown.currentText() == '100%'):
            self.parent.current_sf = 1
        elif (self.sfDropdown.currentText() == '125%'):
            self.parent.current_sf = 1.25
        elif (self.sfDropdown.currentText() == '150%'):
            self.parent.current_sf = 1.5
        else:
            self.parent.current_sf = 2
        
        self.current_sf = self.parent.current_sf
        
        self.changeFont(0)

    def changeFont(self, e):
        self.parent.current_font = self.fontDropdown.currentText()
        self.current_font = self.parent.current_font

        self.logOutBtn.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 18), 400))
        self.accountLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 18), 400))
        self.fontDropdown.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 18), 400))     
        self.fontLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 24), 400))
        self.themeDropdown.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 18), 400))
        self.themeLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 24), 400))
        self.accountsLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 30), 400))
        self.customLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 30), 400))
        self.settingsLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 48), 400))
        self.sfDropdown.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 18), 400))
        self.sfLabel.setFont(QtGui.QFont(self.current_font, int(self.current_sf * 24), 400))

        self.parent.sidebar.changeFont()

    def darkTheme(self):
        self.widget.setStyleSheet(  'background: rgb(69, 69, 69);\n'
                                    'color: white;\n'
                                    'border: 0px solid white;\n')
        self.box.setStyleSheet('background: rgb(71, 71, 71);\n')
        self.customRow.setStyleSheet(   'background: rgb(124, 124, 124);\n'
                                        'border: 0px solid white;\n')
        self.accountsRow.setStyleSheet(     'background: rgb(124, 124, 124);\n'
                                            'border: 0px solid white;\n')

    def lightTheme(self):
        self.widget.setStyleSheet(  'background: rgb(204, 204, 204);\n'
                                    'color: white;\n'
                                    'border: 0px solid black;\n')
        self.box.setStyleSheet('background: rgb(140, 140, 140);\n')
        self.customRow.setStyleSheet(   'background: rgb(100, 100, 100);\n'
                                        'border: 0px solid white;\n')
        self.accountsRow.setStyleSheet(     'background: rgb(100, 100, 100);\n'
                                            'border: 0px solid white;\n')
        self.themeDropdown.setStyleSheet(   'background: rgb(100, 100, 100);\n'
                                            'color: white;\n'
                                            'border: 0px solid white;\n'
                                            'padding-left: 10px;\n')
        self.fontDropdown.setStyleSheet('background: rgb(100, 100, 100);\n'
                                        'color: white;\n'
                                        'border: 0px solid white;\n'
                                        'padding-left: 10px;\n')
        self.sfDropdown.setStyleSheet('background: rgb(100, 100, 100);\n'
                                        'color: white;\n'
                                        'border: 0px solid white;\n'
                                        'padding-left: 10px;\n')

    def classicTheme(self):
        self.widget.setStyleSheet(  'background: rgb(0, 23, 37);\n'
                                    'color: white;\n'
                                    'border: 0px solid white;\n')
        self.box.setStyleSheet('background: rgba(255, 255, 255, 0.1);\n')
        self.customRow.setStyleSheet(   'background: rgba(255, 255, 255, 0.2);\n'
                                        'border: 0px solid white;\n')
        self.accountsRow.setStyleSheet(     'background: rgba(255, 255, 255, 0.2);\n'
                                            'border: 0px solid white;\n')
        self.themeDropdown.setStyleSheet(   'background: rgba(255, 255, 255, 0.2);\n'
                                            'color: white;\n'
                                            'border: 0px solid white;\n'
                                            'padding-left: 10px;\n')
        self.fontDropdown.setStyleSheet('background: rgba(255, 255, 255, 0.2);\n'
                                        'color: white;\n'
                                        'border: 0px solid white;\n'
                                        'padding-left: 10px;\n')
        self.sfDropdown.setStyleSheet('background: rgba(255, 255, 255, 0.2);\n'
                                        'color: white;\n'
                                        'border: 0px solid white;\n'
                                        'padding-left: 10px;\n')