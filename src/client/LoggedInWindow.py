from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QMainWindow

from RentPage import RentPage
from LeasePage import LeasePage
from DashboardPage import DashboardPage

from sender import Sender
from receiver import Receiver

# NOTE: 
# A page for testing GUI and layouts
from TestPage import TestPage

# NOTE:
# class for Sidebar elements/members
class SidebarElement(QWidget):
    def __init__(self, parent):
        super(SidebarElement, self).__init__()

        # NOTE:
        # parent variable to get necessary configs
        self.parent = parent

        # NOTE:
        # class variables
        self.text_color = ""
        self.page_title = ""
        self.page_font = parent.current_font
        self.page = ""
        self.isSelected = False

        # NOTE:
        # setting text color for the element depending on the theme
        if (parent.current_theme == 'Light'):
            self.text_color = 'white'
        else:
            self.text_color = 'white'

        # NOTE:
        # class widgets
        self.pageLabel = QLabel(self)
        self.pageIcon = QLabel(self)

        # NOTE:
        # class configurations
        self.setStyleSheet('background: rgba(255, 255, 255, 0.1);\n'
                           'border: 0px solid black;\n'
                           'color: white;\n')

        # NOTE:
        # layout is Horizontal
        layout = QHBoxLayout()
        layout.addWidget(self.pageIcon, alignment = QtCore.Qt.AlignVCenter)
        layout.addWidget(self.pageLabel, alignment = QtCore.Qt.AlignLeft)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # NOTE:
        # Widget to include both icon and label
        widget = QWidget()
        widget.setLayout(layout)
        widget.setFixedWidth(200)
        widget.setFixedHeight(70)

        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor('rgba(0, 0, 0, 0.2)'))

        # self.setGraphicsEffect(self.shadow)
        widget.setGraphicsEffect(self.shadow)

        # NOTE:
        # Layout of the class
        self.layout = QHBoxLayout()
        self.layout.addWidget(widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # NOTE:
        # Enabling MouseTracking to listen to hovers
        self.setMouseTracking(True)

    # NOTE:
    # getter function to get element text
    def getText(self):
        return self.page_title

    # NOTE:
    # setter function for element icon
    def setIcon(self, e):
        icon = QtGui.QPixmap(e)
        self.pageIcon.setPixmap(icon.scaled(
            25, 25, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))
        self.pageIcon.setStyleSheet('background: transparent;\n'
                                    'border: 0px solid white;\n'
                                    'margin: 0px 0px 0px 0px;\n'
                                    'padding: 20px;')
        self.pageIcon.adjustSize()
        self.pageIcon.setAlignment(QtCore.Qt.AlignLeft)
        self.pageIcon.setFixedWidth(70)

    # NOTE:
    # setter function for element label and window title
    def setLabel(self, e):
        self.page_title = e
        self.pageLabel.setText(e)
        self.pageLabel.setFont(QtGui.QFont(self.parent.current_font, 10, 800))
        self.pageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.pageLabel.adjustSize()
        # self.pageLabel.hide()
        self.unSelectPage()

    # NOTE:
    # setter function to set the associated page with the sidebar element
    def setPage(self, e):
        self.page = e

    # NOTE:
    # changing label style when page is selected
    def selectPage(self):
        self.pageLabel.setStyleSheet('QLabel {\n'
                                     '   border: 0px solid white;\n'
                                     '   background: rgba(0, 0, 0, 0);\n'
                                     '   color: white;\n'
                                     '}\n'
                                     'QLabel:hover {\n'
                                     '   color: white;\n'
                                     '}\n'
                                     'QLabel:pressed {\n'
                                     '   color: rgba(0, 0, 0, 0.1);\n'
                                     '}\n')
        self.isSelected = True

    # NOTE:
    # reverting label style back to original
    def unSelectPage(self):
        self.pageLabel.setStyleSheet('QLabel {\n'
                                     '   border: 0px solid white;\n'
                                     '   background: rgba(0, 0, 0, 0);\n'
                                     '   color: rgba(255, 255, 255, 0.6);\n'
                                     '}\n'
                                     'QLabel:hover {\n'
                                     '   color: ' + self.text_color + ';\n'
                                     '}\n'
                                     'QLabel:clicked {\n'
                                     '   color: rgba(0, 0, 0, 0.2);\n'
                                     '}\n')
        self.isSelected = False

    # NOTE:
    # clickListener to change the page
    def mouseReleaseEvent(self, e):
        self.parent.selectPage(self, self.page)

# NOTE:
# Sidebar class containing SidebarElement instances
class Sidebar(QWidget):
    def __init__(self, parent):
        super(Sidebar, self).__init__()

        # NOTE:
        # Minimized sidebar width
        self.setFixedWidth(70)

        # NOTE:
        # parent variable to get necessary configs
        self.parent = parent

        # NOTE:
        # class state variables
        self.current_page = ""
        self.current_font = self.parent.current_font
        self.current_theme = self.parent.current_theme
        self.elements = []

        # NOTE:
        # class configurations
        self.setMouseTracking(True)
        self.setStyleSheet('background: rgba(0, 0, 0, 0.3);\n'
                           'border: 0px solid white;\n'
                           'color: white;\n')

        # NOTE:
        # Sidebar elements
        self.dashboard = SidebarElement(self)
        self.dashboard.setIcon('../../assets/img/rendt_new_logo_square.png')
        self.dashboard.setLabel('Dashboard')
        self.dashboard.setPage(self.parent.dashboardPage)

        self.profile = SidebarElement(self)
        self.profile.setIcon('../../assets/img/profile_w.png')
        self.profile.setLabel('Profile')
        # self.profile.setPage(self.parent.profilePage)

        self.rent = SidebarElement(self)
        self.rent.setIcon('../../assets/img/cloud_w_no_border.png')
        self.rent.setLabel('Rent')
        self.rent.setPage(self.parent.rentPage)

        self.lease = SidebarElement(self)
        self.lease.setIcon('../../assets/img/cpu_w_no_border.png')
        self.lease.setLabel('Lease')
        self.lease.setPage(self.parent.leasePage)

        self.settings = SidebarElement(self)
        self.settings.setIcon('../../assets/img/settings_w.png')
        self.settings.setLabel('Settings')
        # self.settings.setPage(self.parent.settingsPage)

        self.test = SidebarElement(self)
        self.test.setIcon('../../assets/img/edit_w.png')
        self.test.setLabel('Test')
        self.test.setPage(self.parent.testPage)

        self.elements.append(self.dashboard)
        self.elements.append(self.profile)
        self.elements.append(self.rent)
        self.elements.append(self.lease)
        self.elements.append(self.settings)
        self.elements.append(self.test)

        # NOTE
        # layout is Vertical
        layout = QVBoxLayout()
        layout.addWidget(self.dashboard, alignment=QtCore.Qt.AlignLeft)
        layout.addWidget(self.profile, alignment=QtCore.Qt.AlignLeft)
        layout.addWidget(self.rent, alignment=QtCore.Qt.AlignLeft)
        layout.addWidget(self.lease, alignment=QtCore.Qt.AlignLeft)
        layout.addWidget(self.settings, alignment=QtCore.Qt.AlignLeft)
        layout.addWidget(self.test, alignment=QtCore.Qt.AlignLeft)

        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        widget = QWidget()
        widget.setLayout(layout)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

    # NOTE:
    # selectPage function opens the desired page
    def selectPage(self, sender, toBeOpened):
        sender.selectPage()
        for e in self.elements:
            if (e != sender):
                e.unSelectPage()
            else:
                if (e.page_title == 'Test'):
                    self.parent.testPage = TestPage()
                    e.setPage(self.parent.testPage)
                elif (e.page_title == 'Rent'):
                    self.parent.rentPage = RentPage(self.parent)
                    e.setPage(self.parent.rentPage)
                elif (e.page_title == 'Lease'):
                    self.parent.leasePage = LeasePage(self.parent)
                    self.parent.leasePage.openLeasePage()
                    e.setPage(self.parent.leasePage)
                elif (e.page_title == 'Dashboard'):
                    self.parent.dashboardPage = DashboardPage(self.parent)
                    e.setPage(self.parent.dashboardPage)
                self.parent.content.setCentralWidget(e.page)
        self.current_page = sender.getText()
        self.parent.current_page = sender.getText()

    # NOTE:
    # showing labels when hovered
    def enterEvent(self, e):
        self.setFixedWidth(200)

    # NOTE:
    # hiding labels when mouse leves
    def leaveEvent(self, e):
        self.setFixedWidth(70)

# NOTE:
# LoggedInWindow is the main window with sidebar and dynamic content
class LoggedInWidget(QWidget):
    def __init__(self):
        super(LoggedInWidget, self).__init__()

        self.setStyleSheet('background: rgba(40, 40, 40, 1)')

        # NOTE:
        # class state variables
        self.current_page = "Dashboard"
        self.current_font = "Arial"
        self.current_theme = "Dark"
        self.pages = []
        self.content = QMainWindow()

        self.lease_status = 'not_leasing'

        self.sender = None
        self.receiver = None

        # NOTE:
        # initializing all the pages
        self.dashboardPage = DashboardPage(self)
        # self.profilePage = ProfilePage()
        self.rentPage = RentPage(self)
        self.leasePage = LeasePage(self)
        # self.settingsPage = SettingsPage()
        self.testPage = TestPage()

        self.pages.append(self.dashboardPage)
        # self.pages.append(self.profilePage)
        self.pages.append(self.rentPage)
        self.pages.append(self.leasePage)
        # self.pages.append(self.settingsPage)
        self.pages.append(self.testPage)

        # NOTE:
        # setting current page
        self.content.setCentralWidget(self.dashboardPage)
        self.sidebar = Sidebar(self)

        # NOTE:
        # layout is Horizontal
        layout = QHBoxLayout()
        layout.addWidget(self.sidebar, alignment=QtCore.Qt.AlignTop)
        layout.addWidget(self.content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        widget = QWidget(self)
        widget.setLayout(layout)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

    def setAuthToken(self, auth_token):
        self.receiver = Receiver(auth_token)
        self.sender = Sender(auth_token)

    # NOTE:
    # setter function to change the theme
    def setTheme(self, e):
        self.current_theme = e

    # NOTE:
    # setter function to change the font
    def setFont(self, e):
        self.current_font = e

# NOTE:
# MainWindow class which will display all the pages inside
class LoggedInWindow(QMainWindow):
    def __init__(self, parent=None):
        super(LoggedInWindow, self).__init__(parent)

        # NOTE:
        # class configurations
        self.resize(1024, 768)
        self.widget = LoggedInWidget()
        self.setWindowTitle('rendt')
        self.setWindowIcon(QtGui.QIcon(
            '../../assets/img/rendt_new_logo_square.png'))

        layout = QHBoxLayout()
        layout.addWidget(self.widget)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.centralWidget().layout.setContentsMargins(0, 0, 0, 0)