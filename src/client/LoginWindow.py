from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QMainWindow

from LoggedInWindow import LoggedInWidget
from LoggedInWindow import Sidebar

from sender import Sender
from receiver import Receiver
from authHandler import Auth

# NOTE:
# Custom LineEdit widget with shadow and custom design
class LoginLineEdit(QtWidgets.QLineEdit):
    def __init__(self):
        super(LoginLineEdit, self).__init__()
        
        # NOTE:
        # class configurations
        self.setStyleSheet( 'QLineEdit {\n'
                            '   background: rgb(73, 73, 73);\n'
                            '   color: white;\n'
                            '   border: 0px solid white;\n'
                            '   padding: 5px 10px;\n'
                            '   margin: 10px 0px 0px 0px;\n'
                            '}\n'
                            'QLineEdit:focus {\n'
                            '   border: 0px solid white;\n'
                            '}\n'
                            )
        self.setFont(QtGui.QFont('Arial', 12, 800))
        
        # NOTE:
        # setting drop shadow effect
        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(20, 20, 20))

        self.setGraphicsEffect(self.shadow)

        # NOTE:
        # setting sizing
        self.setFixedWidth(400)
        self.setFixedHeight(55)

# NOTE:
# Custom PushButton widget with shadow and custom design
class LoginButton(QPushButton):
    def __init__(self):
        super(LoginButton, self).__init__()

        # NOTE:
        # class variables
        self.text_color = "white"
        self.btn_back = "rgb(200, 100, 100)"
        self.btn_back_hover = "rgb(100, 50, 50)"
        self.btn_back_pressed = "rgb(50, 25, 25)"

        # NOTE:
        # class configurations
        self.setStyleSheet( 'QPushButton {\n'
                            '   background: rgb(200, 100, 100);\n'
                            '   color: white;\n'
                            '   border: 0px solid white;\n'
                            '}\n'
                            'QPushButton:hover {\n'
                            '   background: rgb(100, 50, 50);\n'
                            '}\n'
                            'QPushButton:pressed {\n'
                            '   background: rgb(50, 25, 25);\n'
                            '}\n')
        self.setFont(QtGui.QFont('Arial', 12, 800))
        
        # NOTE:
        # setting drop shadow effect
        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(20, 20, 20))

        self.setGraphicsEffect(self.shadow)

        # NOTE:
        # setting sizing
        self.setFixedWidth(180)
        self.setFixedHeight(45)
    
    def setColor(self, e):
        self.text_color = e
        self.setStyleSheet( 'QPushButton {\n'
                            '   background: ' + self.btn_back + ';\n'
                            '   color: ' + self.text_color + ';\n'
                            '   border: 0px solid white;\n'
                            '}\n'
                            'QPushButton:hover {\n'
                            '   background: ' + self.btn_back_hover + ';\n'
                            '}\n'
                            'QPushButton:pressed {\n'
                            '   background: ' + self.btn_back_pressed + ';\n'
                            '}\n')
    
    def setBackground(self, e1, e2, e3):
        self.btn_back = e1
        self.btn_back_hover = e2
        self.btn_back_pressed = e3

        self.setStyleSheet( 'QPushButton {\n'
                            '   background: ' + self.btn_back + ';\n'
                            '   color: ' + self.text_color + ';\n'
                            '   border: 0px solid white;\n'
                            '}\n'
                            'QPushButton:hover {\n'
                            '   background: ' + self.btn_back_hover + ';\n'
                            '}\n'
                            'QPushButton:pressed {\n'
                            '   background: ' + self.btn_back_pressed + ';\n'
                            '}\n')

# NOTE:
# Login page with LoginLineEdit and LoginButton instances
class LoginPage(QWidget):
    def __init__(self, parent):
        super(LoginPage, self).__init__()

        self.parent = parent

        # NOTE:
        # logo to be placed on top of login form
        logo = QtGui.QPixmap('../../assets/img/rendt_new_logo_square.png')
        self.logo = QLabel(self)
        self.logo.setPixmap(logo.scaled(
            200, 200, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))
        self.logo.setAlignment(QtCore.Qt.AlignCenter)

        # NOTE:
        # username field 
        self.emailField = LoginLineEdit()
        self.emailField.setPlaceholderText('email')

        # NOTE:
        # password field 
        self.passField = LoginLineEdit()
        self.passField.setPlaceholderText('password')
        self.passField.setEchoMode(QtWidgets.QLineEdit.Password)

        # NOTE:
        # Sign in button to log into the systen
        self.signInBtn = LoginButton()
        self.signInBtn.setText('Sign in')
        self.signInBtn.setBackground('rgb(173, 0, 223)', 'rgb(130, 0, 180)', 'rgb(86, 0, 111)')
        self.signInBtn.clicked.connect(self.goToLogin)

        # NOTE:
        # Sign up button to register to the system
        self.signUpBtn = LoginButton()
        self.signUpBtn.setText('Sign up')
        self.signUpBtn.setBackground('rgb(0, 200, 56)', 'rgb(0, 150, 42)', 'rgb(0, 100, 28)')
        self.signUpBtn.clicked.connect(self.goToRegister)

        # NOTE:
        # Layout and a widget to place buttons on the same row
        self.buttonsRow = QWidget()
        self.buttonsRow.setFixedWidth(600)
        self.buttonsRow.setFixedHeight(70)
        self.buttonsRowLayout = QHBoxLayout()
        self.buttonsRowLayout.addWidget(self.signInBtn, alignment = QtCore.Qt.AlignLeft)
        self.buttonsRowLayout.addWidget(self.signUpBtn, alignment = QtCore.Qt.AlignRight)
        self.buttonsRow.setLayout(self.buttonsRowLayout)
        self.buttonsRowLayout.setAlignment(QtCore.Qt.AlignJustify)
        self.buttonsRowLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsRowLayout.setSpacing(40)

        # NOTE:
        # forgot password label
        self.forgotPass = QLabel(self)
        self.forgotPass.setStyleSheet(  'QLabel {\n'
                                        '   color: rgb(200, 200, 200);\n'
                                        '   margin-right: 100px;\n'
                                        '}\n'
                                        'QLabel:hover {\n'
                                        '   color: rgb(150, 150, 150);\n'
                                        '}\n'
                                        'QLabel:pressed {\n'
                                        '   color: rgb(100, 100, 100);\n'
                                        '}\n')
        self.forgotPass.setText('Forgot password?')
        # self.forgotPass.setFixedWidth(400)
        self.forgotPass.setFont(QtGui.QFont('Arial', 12, 800))
        self.forgotPass.setAlignment(QtCore.Qt.AlignRight)
        self.forgotPass.mouseReleaseEvent = self.goToForgotPass

        # NOTE:
        # layout is vertical
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logo, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.emailField, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.passField, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.buttonsRow, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.forgotPass, alignment = QtCore.Qt.AlignRight)
        self.setLayout(self.layout)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)

    # NOTE:
    # function to go to register page
    def goToRegister(self):
        self.parent.registerPage = RegisterPage(self.parent)
        self.parent.setCentralWidget(self.parent.registerPage)
    
    # NOTE:
    # function to go to forgot password page
    def goToForgotPass(self, e):
        self.parent.forgotPassPage = ForgotPassPage(self.parent)
        self.parent.setCentralWidget(self.parent.forgotPassPage)
    
    # NOTE:
    # function to login to the application
    def goToLogin(self):
        authToken, username, user_type = None, None, None
        auth = Auth()

        email = self.emailField.text()
        email = email.strip()

        pswd = self.passField.text()
        pswd = pswd.strip()

        cred = auth.sign_in(email, pswd)

        if cred:
                authToken, username, user_type, leasing_status = cred

                if (leasing_status == 'a'):
                    leasing_status = 'idle'
                elif (leasing_status == 'u'):
                    leasing_status = 'not_leasing'
                elif (leasing_status == 'n'):
                    leasing_status = 'not_leasing'
                else:
                    leasing_status = 'not_leasing'

                self.parent.loggedInWidget = LoggedInWidget(self.parent)
                self.parent.loggedInWidget.setAuthToken(authToken)
                self.parent.loggedInWidget.lease_status = leasing_status
                self.parent.loggedInWidget.sidebar.selectPage(self.parent.loggedInWidget.sidebar.dashboard, 'Dashboard')
                self.parent.loggedInWidget.setAccount(username, email)
                self.parent.setCentralWidget(self.parent.loggedInWidget)
        
        # self.parent.loggedInWidget = LoggedInWidget()
        # self.parent.setCentralWidget(self.parent.loggedInWidget)

# NOTE:
# Register page with LoginLineEdit and LoginButton instances
class RegisterPage(QWidget):
    def __init__(self, parent):
        super(RegisterPage, self).__init__()

        self.parent = parent

        # NOTE:
        # logo to be placed on top of register form
        logo = QtGui.QPixmap('../../assets/img/rendt_new_logo_square.png')
        self.logo = QLabel(self)
        self.logo.setPixmap(logo.scaled(
            200, 200, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        
        # NOTE:
        # username field 
        self.userField = LoginLineEdit()
        self.userField.setPlaceholderText('username')

        # NOTE:
        # username field 
        self.emailField = LoginLineEdit()
        self.emailField.setPlaceholderText('email')

        # NOTE:
        # password field 
        self.passField = LoginLineEdit()
        self.passField.setPlaceholderText('password')
        self.passField.setEchoMode(QtWidgets.QLineEdit.Password)

        # NOTE:
        # Sign in button to log into the systen
        self.backBtn = LoginButton()
        self.backBtn.setText('Back')
        self.backBtn.setBackground('rgb(50, 50, 50)', 'rgb(70, 70, 70)', 'rgb(90, 90, 90)')
        self.backBtn.clicked.connect(self.goBack)

        # NOTE:
        # Sign up button to register to the system
        self.signUpBtn = LoginButton()
        self.signUpBtn.setText('Sign up')
        self.signUpBtn.setBackground('rgb(0, 200, 56)', 'rgb(0, 150, 42)', 'rgb(0, 100, 28)')
        self.signUpBtn.clicked.connect(self.signUp)

        # NOTE:
        # Layout and a widget to place buttons on the same row
        self.buttonsRow = QWidget()
        self.buttonsRow.setFixedWidth(600)
        self.buttonsRow.setFixedHeight(70)
        self.buttonsRowLayout = QHBoxLayout()
        self.buttonsRowLayout.addWidget(self.backBtn, alignment = QtCore.Qt.AlignLeft)
        self.buttonsRowLayout.addWidget(self.signUpBtn, alignment = QtCore.Qt.AlignRight)
        self.buttonsRow.setLayout(self.buttonsRowLayout)
        self.buttonsRowLayout.setAlignment(QtCore.Qt.AlignJustify)
        self.buttonsRowLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsRowLayout.setSpacing(40)

        # NOTE:
        # layout is vertical
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logo, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.userField, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.emailField, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.passField, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.buttonsRow, alignment = QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)
        self.layout.setAlignment(QtCore.Qt.AlignCenter) 
    
    # NOTE:
    # goBack function to go to the previous page when clicked
    def goBack(self):
        self.parent.loginPage = LoginPage(self.parent)
        self.parent.setCentralWidget(self.parent.loginPage)
    
    # NOTE:
    # signUp function to sign the user with the given credentials
    def signUp(self):
        authToken, usrname, user_type = None, None, None
        auth = Auth()

        username = self.userField.text()
        username = username.strip()

        email = self.emailField.text()
        email = email.strip()

        pswd = self.passField.text()
        pswd = pswd.strip()   

        cred = auth.sign_up(email, pswd, username)     
        if cred:
            authToken, usrname, user_type = cred

            cred = auth.sign_in(email, pswd)

            if cred:
                authToken, username, user_type, leasing_status = cred

                if (leasing_status == 'a'):
                    leasing_status = 'idle'
                elif (leasing_status == 'u'):
                    leasing_status = 'not_leasing'
                elif (leasing_status == 'n'):
                    leasing_status = 'not_leasing'
                else:
                    leasing_status = 'not_leasing'

                self.parent.loggedInWidget = LoggedInWidget(self.parent)
                self.parent.loggedInWidget.setAuthToken(authToken)
                self.parent.loggedInWidget.sidebar.selectPage(self.parent.loggedInWidget.sidebar.dashboard, 'Dashboard')
                self.parent.loggedInWidget.lease_status = leasing_status
                self.parent.loggedInWidget.setAccount(username, email)
                self.parent.setCentralWidget(self.parent.loggedInWidget)

# NOTE:
# Login page with LoginLineEdit and LoginButton instances
class ForgotPassPage(QWidget):
    def __init__(self, parent):
        super(ForgotPassPage, self).__init__()

        self.parent = parent

        # NOTE:
        # logo to be placed on top of forgot password form
        logo = QtGui.QPixmap('../../assets/img/rendt_new_logo_square.png')
        self.logo = QLabel(self)
        self.logo.setPixmap(logo.scaled(
            200, 200, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        
        # NOTE:
        # email field 
        self.emailField = LoginLineEdit()
        self.emailField.setPlaceholderText('email')

        # NOTE:
        # Send button to send email for forgotten passwords
        self.sendBtn = LoginButton()
        self.sendBtn.setText('Send')
        self.sendBtn.setBackground('rgb(2, 164, 158)', 'rgb(2, 123, 120)', 'rgb(0, 82, 79)')
        self.sendBtn.clicked.connect(self.goToForgotPassConfirmPage)

        # NOTE:
        # Sign in button to log into the systen
        self.backBtn = LoginButton()
        self.backBtn.setText('Back')
        self.backBtn.setBackground('rgb(50, 50, 50)', 'rgb(70, 70, 70)', 'rgb(90, 90, 90)')
        self.backBtn.clicked.connect(self.goBack)

        # NOTE:
        # Layout and a widget to place buttons on the same row
        self.buttonsRow = QWidget()
        self.buttonsRow.setFixedWidth(600)
        self.buttonsRow.setFixedHeight(70)
        self.buttonsRowLayout = QHBoxLayout()
        self.buttonsRowLayout.addWidget(self.backBtn, alignment = QtCore.Qt.AlignLeft)
        self.buttonsRowLayout.addWidget(self.sendBtn, alignment = QtCore.Qt.AlignRight)
        self.buttonsRow.setLayout(self.buttonsRowLayout)
        self.buttonsRowLayout.setAlignment(QtCore.Qt.AlignJustify)
        self.buttonsRowLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsRowLayout.setSpacing(40)

        # NOTE:
        # layout is vertical
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logo, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.emailField, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.buttonsRow, alignment = QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)

    # NOTE:
    # function to go to register page
    def goBack(self):
        self.parent.loginPage = LoginPage(self.parent)
        self.parent.setCentralWidget(self.parent.loginPage)
    
    # NOTE:
    # function to go to forgot password confirmation page
    def goToForgotPassConfirmPage(self):
        self.parent.forgotPassConfirmPage = ForgotPassConfirmPage(self.parent)
        self.parent.setCentralWidget(self.parent.forgotPassConfirmPage)

# NOTE:
# Login page with LoginLineEdit and LoginButton instances
class ForgotPassConfirmPage(QWidget):
    def __init__(self, parent):
        super(ForgotPassConfirmPage, self).__init__()

        self.parent = parent

        # NOTE:
        # logo to be placed on top of forgot password form
        logo = QtGui.QPixmap('../../assets/img/rendt_new_logo_square.png')
        self.logo = QLabel(self)
        self.logo.setPixmap(logo.scaled(
            200, 200, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        
        # NOTE:
        # email field 
        self.codeField = LoginLineEdit()
        self.codeField.setPlaceholderText('code')

        # NOTE:
        # Send button to send email for forgotten passwords
        self.confirmBtn = LoginButton()
        self.confirmBtn.setText('Confirm')
        self.confirmBtn.setBackground('rgb(2, 164, 158)', 'rgb(2, 123, 120)', 'rgb(0, 82, 79)')
        # self.sendBtn.clicked.connect(self.goToRegister)

        # NOTE:
        # Sign in button to log into the systen
        self.backBtn = LoginButton()
        self.backBtn.setText('Back')
        self.backBtn.setBackground('rgb(50, 50, 50)', 'rgb(70, 70, 70)', 'rgb(90, 90, 90)')
        self.backBtn.clicked.connect(self.goBack)

        # NOTE:
        # Layout and a widget to place buttons on the same row
        self.buttonsRow = QWidget()
        self.buttonsRow.setFixedWidth(600)
        self.buttonsRow.setFixedHeight(70)
        self.buttonsRowLayout = QHBoxLayout()
        self.buttonsRowLayout.addWidget(self.backBtn, alignment = QtCore.Qt.AlignLeft)
        self.buttonsRowLayout.addWidget(self.confirmBtn, alignment = QtCore.Qt.AlignRight)
        self.buttonsRow.setLayout(self.buttonsRowLayout)
        self.buttonsRowLayout.setAlignment(QtCore.Qt.AlignJustify)
        self.buttonsRowLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsRowLayout.setSpacing(40)

        # NOTE:
        # layout is vertical
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logo, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.codeField, alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.buttonsRow, alignment = QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)

    # NOTE:
    # function to go to register page
    def goBack(self):
        self.parent.forgotPassPage = ForgotPassPage(self.parent)
        self.parent.setCentralWidget(self.parent.forgotPassPage)

# NOTE:
# Login Window class to host all the login related pages
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()

        self.resize(1000, 950)
        self.setStyleSheet('background: rgb(47, 47, 47)')
        self.setWindowTitle('rendt')
        self.setWindowIcon(QtGui.QIcon(
            '../../assets/img/rendt_new_logo_square.png'))

        self.loginPage = LoginPage(self)
        self.registerPage = RegisterPage(self)
        self.forgotPassPage = ForgotPassPage(self)
        self.forgotPassConfirmPage = ForgotPassConfirmPage(self)
        self.loggedInWidget = LoggedInWidget(self)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.loginPage)
        self.layout.addWidget(self.registerPage)
        self.layout.addWidget(self.forgotPassPage)
        self.layout.addWidget(self.forgotPassConfirmPage)
        self.setLayout(self.layout)
        self.setCentralWidget(self.loginPage)
    
    def closeEvent(self, event):
        if (self.loggedInWidget.t1 is not None):
            self.loggedInWidget.t1.stop()
            self.loggedInWidget.t1.join()
            self.loggedInWidget.receiver.sign_out()

        self.close()

        event.accept() # let the window close