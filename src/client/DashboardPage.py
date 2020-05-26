from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QMainWindow

import threading

from RentPage import CustomSquareButton

class LeasingRequest(QWidget):
    def __init__(self, parent):
        super(LeasingRequest, self).__init__()

        self.parent = parent

        self.jobId = None
        self.orderId = None
        self.renterId = None
        self.jobDesc = None
        self.jobMode = None
        self.status = None

        self.requests = []

        self.setStyleSheet( 'background: rgba(255, 255, 255, 0.1);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')
        self.setFixedHeight(100)

        self.requestByLabel = QLabel(self)
        self.requestByLabel.setText('Request by ')
        self.requestByLabel.setFont(QtGui.QFont('Arial', 20, 800))
        self.requestByLabel.adjustSize()
        self.requestByLabel.setStyleSheet( 'background: transparent;\n'
                                            'color: white;\n'
                                            'font-weight: bold;\n'
                                            'border: 0px solid white;\n')
        self.requestByLabel.setAlignment(QtCore.Qt.AlignLeft)

        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.renterLabel = QLabel(self)
        self.renterLabel.setText('')
        self.renterLabel.setFont(QtGui.QFont('Arial', 20, 800))
        self.renterLabel.adjustSize()
        self.renterLabel.setStyleSheet( 'background: transparent;\n'
                                        'color: rgb(197, 0, 255);\n'
                                        'font-weight: bold;\n'
                                        'border: 0px solid white;\n')
        self.renterLabel.setAlignment(QtCore.Qt.AlignLeft)

        self.requestLabel = QWidget(self)
        self.requestLabel.setStyleSheet('background: transparent;\n'
                                        'border: 0px solid white;\n')
        
        self.requestLayout = QHBoxLayout()
        self.requestLayout.addWidget(self.requestByLabel)
        self.requestLayout.addWidget(self.renterLabel)
        self.requestLayout.setSpacing(0)
        self.requestLayout.setContentsMargins(0, 0, 0, 0)
        self.requestLayout.setAlignment(QtCore.Qt.AlignVCenter)

        self.requestLabel.setLayout(self.requestLayout)

        self.acceptBtn = QPushButton(self)
        self.acceptBtn.setStyleSheet(  'QPushButton {\n'
                                        '   background: rgba(0, 149, 20, 0.7);\n'
                                        '   color: white;\n'
                                        '   border: 0px solid white;\n'
                                        '}\n'
                                        'QPushButton:hover {\n'
                                        '   background: rgba(0, 100, 14, 0.7);\n'
                                        '}\n'
                                        'QPushButton:pressed {\n'
                                        '   background: rgba(0, 75, 10, 0.7);\n'
                                        '}\n')
        self.acceptBtn.setFont(QtGui.QFont('Arial', 12, 800))
        self.acceptBtn.setText('Accept')
        self.acceptBtn.setFixedWidth(130)
        self.acceptBtn.setFixedHeight(100)
        # self.acceptBtn.clicked.connect(self.goToRentalTypePage)

        self.rejectBtn = QPushButton(self)
        self.rejectBtn.setStyleSheet(  'QPushButton {\n'
                                        '   background: rgba(246, 49, 49, 0.7);\n'
                                        '   color: white;\n'
                                        '   border: 0px solid black;\n'
                                        '}\n'
                                        'QPushButton:hover {\n'
                                        '   background: rgba(200, 39, 39, 0.7);\n'
                                        '}\n'
                                        'QPushButton:pressed {\n'
                                        '   background: rgba(123, 25, 25, 0.7);\n'
                                        '}\n')
        self.rejectBtn.setFont(QtGui.QFont('Arial', 12, 800))
        self.rejectBtn.setText('Reject')
        self.rejectBtn.setFixedWidth(130)
        self.rejectBtn.setFixedHeight(100)
        # self.rejectBtn.clicked.connect(self.goToRentalTypePage)
        
        self.buttonsGroup = QWidget(self)
        self.buttonsGroup.setStyleSheet('background: transparent;\n'
                                        'border: 0px solid white;\n')
        
        self.buttonsGroupLayout = QHBoxLayout()
        self.buttonsGroupLayout.addWidget(self.acceptBtn)
        self.buttonsGroupLayout.addWidget(self.rejectBtn)
        self.buttonsGroupLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.buttonsGroupLayout.setSpacing(0)
        self.buttonsGroupLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsGroup.setLayout(self.buttonsGroupLayout)

        layout = QHBoxLayout()
        layout.addWidget(self.requestLabel, alignment = QtCore.Qt.AlignLeft)
        layout.addWidget(self.buttonsGroup, alignment = QtCore.Qt.AlignRight)
        layout.setAlignment(QtCore.Qt.AlignVCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(30, 0, 0, 0)

        widget = QWidget(self)
        widget.setLayout(layout)
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        widget.setGraphicsEffect(self.shadow)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widget)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)
    
    def setRenter(self, e):
        self.renterLabel.setText(str(e))
        self.renterLabel.adjustSize()
        self.acceptBtn.clicked.connect(self.acceptReq)
        self.rejectBtn.clicked.connect(self.rejectReq)

    def acceptReq(self, e):
        self.parent.parent.parent.leasePage.changeStatus('executing')
        t1 = threading.Thread(target=self.startExec)
        t1.daemon = True
        t1.start()

    def startExec(self):
        response = self.parent.parent.parent.receiver.accept_order(self.orderId)

        if (response is not None):
            db_token = response[0]
            f_size = response[1]

            self.parent.parent.parent.receiver.download_file_from_db('files.zip', db_token, f_size)

            self.parent.parent.parent.receiver.execute_job('files.zip', 'renter_output.zip')
            db_token = self.parent.parent.parent.receiver.get_permission_to_upload_output(self.jobId, 'renter_output.zip')
            self.parent.parent.parent.receiver.upload_output_to_db('renter_output.zip', self.jobId, db_token)
            self.hide()
            self.destroy()
            self.parent.parent.parent.leasePage.changeStatus('idle')

    def rejectReq(self, e):
        response = self.parent.parent.parent.receiver.decline_order(self.orderId)
        self.destroy()

class RentingRequest(QWidget):
    def __init__(self, parent):
        super(RentingRequest, self).__init__()

        self.parent = parent
        self.taskPage = ''

        self.setStyleSheet( 'background: rgb(70, 70, 70);\n'
                            'color: white;\n'
                            'border: 0px solid rgb(100, 100, 100);\n')
        self.setFixedHeight(100)

        self.requestForLabel = QLabel(self)
        self.requestForLabel.setText('Request for ')
        self.requestForLabel.setFont(QtGui.QFont('Arial', 20, 800))
        self.requestForLabel.adjustSize()
        self.requestForLabel.setStyleSheet( 'background: transparent;\n'
                                            'color: white;\n'
                                            'font-weight: bold;\n'
                                            'border: 0px solid white;\n')
        self.requestForLabel.setAlignment(QtCore.Qt.AlignLeft)

        self.leaserLabel = QLabel(self)
        self.leaserLabel.setText('')
        self.leaserLabel.setFont(QtGui.QFont('Arial', 20, 800))
        self.leaserLabel.adjustSize()
        self.leaserLabel.setStyleSheet( 'background: transparent;\n'
                                        'color: rgb(0, 200, 56);\n'
                                        'font-weight: bold;\n'
                                        'border: 0px solid white;\n')
        self.leaserLabel.setAlignment(QtCore.Qt.AlignLeft)

        self.requestLabel = QWidget(self)
        self.requestLabel.setStyleSheet('background: transparent;\n'
                                        'border: 0px solid white;\n')
        
        self.requestLayout = QHBoxLayout()
        self.requestLayout.addWidget(self.requestForLabel)
        self.requestLayout.addWidget(self.leaserLabel)
        self.requestLayout.setSpacing(0)
        self.requestLayout.setContentsMargins(0, 0, 0, 0)
        self.requestLayout.setAlignment(QtCore.Qt.AlignVCenter)

        self.requestLabel.setLayout(self.requestLayout)

        self.requestBtn = QPushButton(self)
        self.requestBtn.setStyleSheet(  'QPushButton {\n'
                                        '   background: rgb(0, 149, 20);\n'
                                        '   color: white;\n'
                                        '   border: 0px solid white;\n'
                                        '}\n'
                                        'QPushButton:hover {\n'
                                        '   background: rgb(0, 100, 14);\n'
                                        '}\n'
                                        'QPushButton:pressed {\n'
                                        '   background: rgb(0, 75, 10);\n'
                                        '}\n')
        self.requestBtn.setFont(QtGui.QFont('Arial', 12, 800))
        self.requestBtn.setText('Status')
        self.requestBtn.setFixedWidth(130)
        self.requestBtn.setFixedHeight(100)
        # self.requestBtn.clicked.connect(self.goToRentalTypePage)

        layout = QHBoxLayout()
        layout.addWidget(self.requestLabel, alignment = QtCore.Qt.AlignLeft)
        layout.addWidget(self.requestBtn, alignment = QtCore.Qt.AlignRight)
        layout.setAlignment(QtCore.Qt.AlignVCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(30, 0, 0, 0)

        widget = QWidget(self)
        widget.setLayout(layout)
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widget)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(30, 30, 30))

        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)
        self.setGraphicsEffect(self.shadow)

    def setLeaserLabel(self, e):
        self.leaserLabel.setText(e)
        self.leaserLabel.adjustSize()
    
    def setRequestStatus(self, e):
        self.taskPage = TaskPage(self.parent)
        self.requestBtn.clicked.connect(lambda:self.parent.parent.goToTaskPage(self.taskPage))

        if (e == 'Pending'):
            self.requestBtn.setText('Pending')
            self.requestBtn.setStyleSheet(  'QPushButton {\n'
                                            '   background: rgba(80, 80, 80, 0.9);\n'
                                            '   color: white;\n'
                                            '   border: 0px solid white;\n'
                                            '}\n'
                                            'QPushButton:hover {\n'
                                            '   background: rgba(80, 80, 80, 0.6);\n'
                                            '}\n'
                                            'QPushButton:pressed {\n'
                                            '   background: rgba(80, 80, 80, 0.3);\n'
                                            '}\n')
        elif (e == 'Executing'):
            self.requestBtn.setText('Executing')
            self.requestBtn.setStyleSheet(  'QPushButton {\n'
                                            '   background: rgba(0, 149, 20, 0.7);\n'
                                            '   color: white;\n'
                                            '   border: 0px solid white;\n'
                                            '}\n'
                                            'QPushButton:hover {\n'
                                            '   background: rgba(0, 100, 14, 0.7);\n'
                                            '}\n'
                                            'QPushButton:pressed {\n'
                                            '   background: rgba(0, 75, 10, 0.7);\n'
                                            '}\n')
            # TODO: Set function to be linked to the button
        elif (e == 'Rejected'):
            self.requestBtn.setText('Rejected')
            self.requestBtn.setStyleSheet(  'QPushButton {\n'
                                            '   background: rgba(246, 49, 49, 0.7);\n'
                                            '   color: white;\n'
                                            '   border: 0px solid black;\n'
                                            '}\n'
                                            'QPushButton:hover {\n'
                                            '   background: rgba(200, 39, 39, 0.7);\n'
                                            '}\n'
                                            'QPushButton:pressed {\n'
                                            '   background: rgba(123, 25, 25, 0.7);\n'
                                            '}\n')
            # TODO: Set function to be linked to the button
        elif (e == 'Finished'):
            self.requestBtn.setText('Finished')
            self.requestBtn.setStyleSheet(  'QPushButton {\n'
                                            '   background: rgba(186, 63, 205, 0.7);\n'
                                            '   color: white;\n'
                                            '   border: 0px solid black;\n'
                                            '}\n'
                                            'QPushButton:hover {\n'
                                            '   background: rgba(140, 53, 170, 0.7);\n'
                                            '}\n'
                                            'QPushButton:pressed {\n'
                                            '   background: rgba(93, 30, 100, 0.7);\n'
                                            '}\n')
            # TODO: Set function to be linked to the button

class TaskPage(QWidget):
    def __init__(self, parent):
        super(TaskPage, self).__init__()

        self.parent = parent

        self.current_theme = self.parent.current_theme
        self.current_font = self.parent.current_font

        if (self.current_theme == 'Dark'):
            self.darkTheme()
        elif (self.current_theme == 'Light'):
            self.lightTheme()
        else:
            self.classicTheme()

        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.requestStatus = 'Pending'
        self.requestStarted = '' #TODO: get execution start time

        self.shadow2 = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow2.setBlurRadius(30)
        self.shadow2.setXOffset(0)
        self.shadow2.setYOffset(0)
        self.shadow2.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.shadow3 = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow3.setBlurRadius(30)
        self.shadow3.setXOffset(0)
        self.shadow3.setYOffset(0)
        self.shadow3.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.shadow4 = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow4.setBlurRadius(30)
        self.shadow4.setXOffset(0)
        self.shadow4.setYOffset(0)
        self.shadow4.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.statusLabel = QLabel(self)
        self.statusLabel.setText('Status')
        self.statusLabel.setFont(QtGui.QFont('Arial', 40, 1000))
        self.statusLabel.adjustSize()
        self.statusLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.statusLabel.setStyleSheet( 'background: transparent;\n'
                                        'border: 0px solid white;\n'
                                        'margin-top: 50px;\n'
                                        'font-weight: bold;\n')   
        self.statusLabel.setGraphicsEffect(self.shadow)

        self.downloadZipBtn = CustomSquareButton(self)
        self.downloadZipBtn.setHeader('Uploaded files')
        self.downloadZipBtn.setImage('../../assets/img/zip_w.png')
        self.downloadZipBtn.setGraphicsEffect(self.shadow2)

        self.statusInfoLabel = QLabel(self)
        self.statusInfoLabel.setText('Status: ' + self.requestStatus)
        self.statusInfoLabel.setFont(QtGui.QFont('Arial', 20, 1000))
        self.statusInfoLabel.adjustSize()
        self.statusInfoLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.statusInfoLabel.setStyleSheet( 'background: transparent;\n'
                                            'border: 0px solid white;\n'
                                            'font-weight: bold;\n')

        if (self.requestStatus == 'Executing'):
            self.elapsedTimeLabel = QLabel(self)
            self.elapsedTimeLabel.setText('ET: ' + self.AlignLeft)
            self.elapsedTimeLabel.setFont(QtGui.QFont('Arial', 20, 1000))
            self.elapsedTimeLabel.adjustSize()
            self.elapsedTimeLabel.setAlignment(QtCore.Qt.AlignLeft)
            self.elapsedTimeLabel.setStyleSheet('background: transparent;\n'
                                                'border: 0px solid white;\n'
                                                'margin-top: 50px;\n'
                                                'font-weight: bold;\n')

            self.feeLabel = QLabel(self)
            self.feeLabel.setText('ET: ' + self.calculateFee())
            self.feeLabel.setFont(QtGui.QFont('Arial', 20, 1000))
            self.feeLabel.adjustSize()
            self.feeLabel.setAlignment(QtCore.Qt.AlignLeft)
            self.feeLabel.setStyleSheet('background: transparent;\n'
                                        'border: 0px solid white;\n'
                                        'margin-top: 50px;\n'
                                        'font-weight: bold;\n')           

        self.statusBox = QWidget(self)

        self.statusBox = QWidget(self)
        self.statusBox.setStyleSheet( 'background: rgb(0, 140, 135);\n'
                                    'color: white;\n'
                                    'border: 0px solid white;\n')

        self.statusBox.setMinimumHeight(400)
        self.statusBox.setMinimumWidth(400)

        self.statusBoxLayout = QVBoxLayout()
        self.statusBoxLayout.addWidget(self.statusInfoLabel)

        if (self.requestStatus == 'Executing'):
            self.statusBoxLayout.addWidget(self.elapsedTimeLabel)
            self.statusBoxLayout.addWidget(self.feeLabel)

        self.statusBoxLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.statusBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.statusBoxLayout.setSpacing(10)
        self.statusBox.setLayout(self.statusBoxLayout)
        self.statusBox.setGraphicsEffect(self.shadow3)

        self.boxRow = QWidget(self)
        self.boxRow.setStyleSheet(  'background: transparent;\n'
                                    'color: white;\n'
                                    'border: 0px solid white;\n')

        self.boxRowLayout = QHBoxLayout()
        self.boxRowLayout.addWidget(self.downloadZipBtn, alignment = QtCore.Qt.AlignLeft)
        self.boxRowLayout.addWidget(self.statusBox, alignment = QtCore.Qt.AlignRight)
        self.boxRowLayout.setContentsMargins(50, 50, 50, 50)
        self.boxRowLayout.setSpacing(50)
        self.boxRow.setLayout(self.boxRowLayout)

        self.stopBtn = QPushButton(self)
        self.stopBtn.setStyleSheet('QPushButton {\n'
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
        self.stopBtn.setFont(QtGui.QFont('Arial', 15, 900))
        self.stopBtn.setText('Stop')
        self.stopBtn.setFixedHeight(105)
        self.stopBtn.setFixedWidth(325)
        self.stopBtn.setGraphicsEffect(self.shadow4)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.statusLabel, alignment = QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.boxRow, alignment = QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.stopBtn, alignment = QtCore.Qt.AlignHCenter)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 50)
        self.layout.setSpacing(30)

        self.setLayout(self.layout)
        
    def calculateFee(self):
        #TODO: Fee calculation
        return ''

    def darkTheme(self):
        self.setStyleSheet( 'background: rgb(57, 57, 57);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

    def lightTheme(self):
        self.setStyleSheet( 'background: rgb(204, 204, 204);\n'
                            'color: white;\n'
                            'border: 0px solid black;\n')

    def classicTheme(self):
        self.setStyleSheet( 'background: rgb(0, 23, 37);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

class RentingList(QWidget):
    def __init__(self, parent):
        super(RentingList, self).__init__()

        self.parent = parent

        self.setMaximumWidth(1000)

        self.current_theme = self.parent.current_theme
        self.current_font = self.parent.current_font

        if (self.current_theme == 'Dark'):
            self.darkTheme()
        elif (self.current_theme == 'Light'):
            self.lightTheme()
        else:
            self.classicTheme()

        self.requests = []

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(10)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)
    
    def addRequest(self, leaserName, reqStatus):
        request = RentingRequest(self)
        request.setLeaserLabel(leaserName)
        request.setRequestStatus(reqStatus)
        self.requests.append(request)
        self.layout.addWidget(request)

    def darkTheme(self):
        self.setStyleSheet( 'background: rgb(69, 69, 69);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

    def lightTheme(self):
        self.setStyleSheet( 'background: rgb(204, 204, 204);\n'
                            'color: white;\n'
                            'border: 0px solid black;\n')

    def classicTheme(self):
        self.setStyleSheet( 'background: rgb(0, 23, 37);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

class LeasingList(QWidget):
    def __init__(self, parent):
        super(LeasingList, self).__init__()

        self.parent = parent

        self.setMaximumWidth(1000)

        self.current_theme = self.parent.current_theme
        self.current_font = self.parent.current_font

        if (self.current_theme == 'Dark'):
            self.darkTheme()
        elif (self.current_theme == 'Light'):
            self.lightTheme()
        else:
            self.classicTheme()

        self.requests = []

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 50)
        self.layout.setSpacing(5)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)
    
    def addRequests(self):
        requests = self.parent.parent.receiver.get_job_notifications()

        for r in requests:
            request = LeasingRequest(self)
            request.orderId = r[0]
            request.renterId = r[1]
            request.jobId = r[2]
            request.jobDesc = r[3]
            request.jobMode = r[4]
            request.status = r[5]
            
            request.setRenter(request.renterId)

        self.requests.append(request)
        self.layout.addWidget(request)

    def darkTheme(self):
        self.setStyleSheet( 'background: rgb(69, 69, 69);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

    def lightTheme(self):
        self.setStyleSheet( 'background: rgb(204, 204, 204);\n'
                            'color: white;\n'
                            'border: 0px solid black;\n')

    def classicTheme(self):
        self.setStyleSheet( 'background: rgb(0, 23, 37);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

class DashboardPage(QScrollArea):
    def __init__(self, parent):
        super(DashboardPage, self).__init__()

        self.parent = parent
        self.setStyleSheet("background: rgb(57, 57, 57);\n"
                           "border: 0px solid rgb(25, 118, 210);\n"
                           "color: white;\n")

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setWidgetResizable(True)

        self.current_theme = self.parent.current_theme
        self.current_font = self.parent.current_font

        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.shadow2 = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow2.setBlurRadius(30)
        self.shadow2.setXOffset(0)
        self.shadow2.setYOffset(0)
        self.shadow2.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.rentingLabel = QLabel(self)
        self.rentingLabel.setText('Renting')
        self.rentingLabel.setFont(QtGui.QFont('Arial', 40, 400))
        self.rentingLabel.adjustSize()
        self.rentingLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.rentingLabel.setStyleSheet('background: transparent;\n'
                                        'border: 0px solid white;\n'
                                        'font-weight: bold;\n'
                                        'margin-left: 10px;\n') 
        self.rentingLabel.setGraphicsEffect(self.shadow)

        self.rentingList = RentingList(self)
        self.rentingList.addRequest('zxyctn', 'Pending')
        self.rentingList.addRequest('zxyctn2', 'Executing')
        self.rentingList.addRequest('zxyctn0', 'Rejected')
        self.rentingList.addRequest('zxyctn1', 'Finished')

        self.leasingLabel = QLabel(self)
        self.leasingLabel.setText('Leasing')
        self.leasingLabel.setFont(QtGui.QFont('Arial', 40, 400))
        self.leasingLabel.adjustSize()
        self.leasingLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.leasingLabel.setStyleSheet('background: transparent;\n'
                                        'border: 0px solid white;\n'
                                        'font-weight: bold;\n'
                                        'margin-left: 10px;\n') 
        self.leasingLabel.setGraphicsEffect(self.shadow2)
        
        self.leasingList = LeasingList(self)
        if (self.parent.sender is not None):
            self.leasingList.addRequests()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.rentingLabel)
        self.layout.addWidget(self.rentingList)
        self.layout.addWidget(self.leasingLabel)
        self.layout.addWidget(self.leasingList)

        self.layout.setContentsMargins(30, 60, 30, 30)
        self.layout.setAlignment(QtCore.Qt.AlignHCenter)

        self.container = QWidget(self)
        self.container.setLayout(self.layout)
        self.container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.setWidget(self.container)

        if (self.current_theme == 'Dark'):
            self.darkTheme()
        elif (self.current_theme == 'Light'):
            self.lightTheme()
        else:
            self.classicTheme()

    def darkTheme(self):
        self.container.setStyleSheet( 'background: rgb(57, 57, 57);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

    def lightTheme(self):
        self.container.setStyleSheet( 'background: rgb(204, 204, 204);\n'
                            'color: white;\n'
                            'border: 0px solid black;\n')

    def classicTheme(self):
        self.container.setStyleSheet( 'background: rgb(0, 23, 37);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

    def goToTaskPage(self, taskPage):
        layout = QVBoxLayout()
        layout.addWidget(taskPage)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.container = QWidget(self)
        self.container.setLayout(layout)
        self.setWidget(self.container)