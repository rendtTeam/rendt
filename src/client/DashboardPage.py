from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QMainWindow

import threading

import os, sys, platform

from RentPage import CustomSquareButton

class LeasingRequest(QWidget):
    def __init__(self, parent):
        super(LeasingRequest, self).__init__()

        self.parent = parent

        self.jobId = None
        self.orderId = None
        self.renterUserName = None
        self.jobDesc = None
        self.jobMode = None
        self.status = None

        self.requests = []

        self.setStyleSheet( 'background: rgb(70, 70, 70);\n'
                            'color: white;\n'
                            'border: 0px solid rgb(100, 100, 100);\n')
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

        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(30, 30, 30))

        self.layout = QVBoxLayout()
        self.layout.addWidget(widget)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)
        self.setGraphicsEffect(self.shadow)
    
    def setRenter(self, e):
        self.renterLabel.setText(e)
        self.renterLabel.adjustSize()
        self.acceptBtn.clicked.connect(self.acceptReq)
        self.rejectBtn.clicked.connect(self.rejectReq)

    def acceptReq(self, e):
        self.hide()
        self.destroy()
        if (self.parent.parent.parent.leasePage.dockerInfo.dockerExists()):
            self.parent.parent.parent.leasePage.changeStatus('executing')
            t1 = threading.Thread(target=self.startExec)
            t1.daemon = True
            t1.start()

    def startExec(self):
        if (self.parent.parent.parent.leasePage.dockerInfo.dockerExists()):
            if (not self.parent.parent.parent.leasePage.dockerInfo.imageExists()):
                self.parent.parent.parent.receiver.build_docker('.')
            self.parent.parent.parent.leasePage.changeStatus('executing')
            response = self.parent.parent.parent.receiver.accept_order(self.orderId)

            if (platform.system() == 'Windows'):
                home_dir = os.system("(echo %" + "cd%)>pwd.txt")

                f = open("pwd.txt", "r")
                x = f.readline()
                x = x.split("\\")        
                y = x[0] + '/' + x[1] + "/" + x[2] + "/rendt"
                home_dir = os.system("DEL pwd.txt")
                home_dir = os.system("mkdir " + y)
            else:
                home_dir = os.system("pwd>pwd.txt")

                f = open("pwd.txt", "r")
                x = f.readline()
                x = x.split("/")        
                y = "/" + x[1] + "/" + x[2] + "/rendt"
                home_dir = os.system("rm pwd.txt")
                home_dir = os.system("mkdir " + y)
            if (response is not None):
                db_token = response[0]
                f_size = response[1]

                path_to_executable = y + '/files.zip'
                path_to_output = y + '/output.zip'
                print('1------------------------------------------------------------------------------------------')

                self.parent.parent.parent.receiver.download_file_from_db(path_to_executable, db_token, f_size)
                print('2------------------------------------------------------------------------------------------')

                self.parent.parent.parent.receiver.execute_job(path_to_executable, path_to_output)
                print('3------------------------------------------------------------------------------------------')

                db_token = self.parent.parent.parent.receiver.get_permission_to_upload_output(self.jobId, path_to_output)
                print('4------------------------------------------------------------------------------------------')

                self.parent.parent.parent.receiver.upload_output_to_db(path_to_output, self.jobId, db_token)
                print('5------------------------------------------------------------------------------------------')

                if (platform.system() == 'Windows'):
                    home_dir = os.system("DEL files.zip")
                    home_dir = os.system("DEL output.zip")
                else:
                    home_dir = os.system("rm -R " + path_to_executable)
                    home_dir = os.system("rm -R " + path_to_output)

                self.hide()
                self.destroy()
                self.parent.parent.parent.leasePage.changeStatus('idle')
                self.parent.parent.parent.leasePage.leaseExecPage.hide()
                self.parent.parent.parent.leasePage.leaseIdlePage.show()

    def rejectReq(self, e):
        response = self.parent.parent.parent.receiver.decline_order(self.orderId)
        self.hide()
        self.destroy()

class RentingRequest(QWidget):
    def __init__(self, parent, jobInfo):
        super(RentingRequest, self).__init__()

        self.parent = parent
        self.jobInfo = jobInfo
        self.taskPage = ''

        self.setStyleSheet( 'background: rgb(70, 70, 70);\n'
                            'color: white;\n'
                            'border: 0px solid rgb(100, 100, 100);\n'
                            'margin: 0px\n')
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
        
        self.setRequestStatus(self.jobInfo[4])
        self.setLeaserLabel(self.jobInfo[3])

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
        self.layout.addWidget(widget, alignment = QtCore.Qt.AlignTop)
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
        self.leaserLabel.setText(str(e))
        self.leaserLabel.adjustSize()
    
    def setRequestStatus(self, e):
        self.requestBtn.clicked.connect(lambda:self.parent.parent.goToTaskPage(self.taskPage))

        if (e == 'p'):
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
            self.taskPage = TaskPage(self.parent, self.jobInfo[0], 'Pending')

        elif (e == 'x'):
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
            self.taskPage = TaskPage(self.parent, self.jobInfo[0], 'Executing')
            # TODO: Set function to be linked to the button
        elif (e == 'd'):
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
            self.taskPage = TaskPage(self.parent, self.jobInfo[0], 'Rejected')
            # TODO: Set function to be linked to the button
        elif (e == 'f'):
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
            self.taskPage = TaskPage(self.parent, self.jobInfo[0], 'Finished')
            # TODO: Set function to be linked to the button

class TaskPage(QWidget):
    def __init__(self, parent, jobId, status):
        super(TaskPage, self).__init__()

        self.parent = parent
        self.jobId = jobId

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

        self.requestStatus = status
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

        self.shadow5 = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow5.setBlurRadius(30)
        self.shadow5.setXOffset(0)
        self.shadow5.setYOffset(0)
        self.shadow5.setColor(QtGui.QColor('rgb(0, 0, 0)'))

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
        self.downloadZipBtn.setHeader('Output files')
        self.downloadZipBtn.setImage('../../assets/img/zip_w.png')
        self.downloadZipBtn.setFooter('Output of the uploaded execution files.\nFiles will be available to download after payment.')
        self.downloadZipBtn.clicked.connect(self.downloadOutput)
        self.downloadZipBtn.setGraphicsEffect(self.shadow2)

        self.statusInfoLabel = QLabel(self)
        self.statusInfoLabel.setText('Status: ' + self.requestStatus)
        self.statusInfoLabel.setFont(QtGui.QFont('Arial', 20, 1000))
        self.statusInfoLabel.adjustSize()
        self.statusInfoLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.statusInfoLabel.setStyleSheet( 'background: transparent;\n'
                                            'border: 0px solid white;\n'
                                            'font-weight: bold;\n')

        # if (self.requestStatus == 'Executing'):
        self.elapsedTimeLabel = QLabel(self)
        self.elapsedTimeLabel.setText('ET: ')
        self.elapsedTimeLabel.setFont(QtGui.QFont('Arial', 20, 1000))
        self.elapsedTimeLabel.adjustSize()
        self.elapsedTimeLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.elapsedTimeLabel.setStyleSheet('background: transparent;\n'
                                            'border: 0px solid white;\n'
                                            'margin-top: 50px;\n'
                                            'font-weight: bold;\n')

        self.feeLabel = QLabel(self)
        self.feeLabel.setText('Fee: ' + self.calculateFee())
        self.feeLabel.setFont(QtGui.QFont('Arial', 20, 1000))
        self.feeLabel.adjustSize()
        self.feeLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.feeLabel.setStyleSheet('background: transparent;\n'
                                    'border: 0px solid white;\n'
                                    'margin-top: 50px;\n'
                                    'font-weight: bold;\n')           

        self.statusBox = QWidget(self)

        self.statusBox = QWidget(self)
        if (status == 'Pending'):
            self.statusBox.setStyleSheet(   'background: rgb(117, 117, 117);\n'
                                            'color: white;\n'
                                            'border: 0px solid white;\n')
        elif (status == 'Executing'):
            self.statusBox.setStyleSheet(   'background: rgb(1, 91, 19);\n'
                                            'color: white;\n'
                                            'border: 0px solid white;\n')
        
        elif (status == 'Rejected'):
            self.statusBox.setStyleSheet(   'background: rgb(163, 0, 0);\n'
                                            'color: white;\n'
                                            'border: 0px solid white;\n')
        
        elif (status == 'Finished'):
            self.statusBox.setStyleSheet(   'background: rgb(131, 0, 123);\n'
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
        self.boxRowLayout.setContentsMargins(50, 50, 50, 20)
        self.boxRowLayout.setSpacing(50)
        self.boxRow.setLayout(self.boxRowLayout)

        self.proceedToPaymentBtn = QPushButton(self)
        self.proceedToPaymentBtn.setStyleSheet('QPushButton {\n'
                                    '   background: rgb(153, 63, 160);\n'
                                    '   color: white;\n'
                                    '   border: 0px solid black;\n'
                                    '   margin: 20px;\n'
                                    '   margin-right: 50px;\n'
                                    '}\n'
                                    'QPushButton:hover {\n'
                                    '   background: rgb(120, 40, 125);\n'
                                    '}\n'
                                    'QPushButton:pressed {\n'
                                    '   background: rgb(75, 30, 80);\n'
                                    '}\n')
        self.proceedToPaymentBtn.setFont(QtGui.QFont('Arial', 12, 900))
        self.proceedToPaymentBtn.setText('Proceed to Payment')
        self.proceedToPaymentBtn.setFixedHeight(105)
        self.proceedToPaymentBtn.setFixedWidth(325)
        self.proceedToPaymentBtn.setGraphicsEffect(self.shadow4)

        self.backBtn = QPushButton(self)
        self.backBtn.setStyleSheet('QPushButton {\n'
                                    '   background: rgb(2, 129, 138);\n'
                                    '   color: white;\n'
                                    '   border: 0px solid black;\n'
                                    '   margin: 20px;\n'
                                    '   margin-left: 50px;\n'
                                    '}\n'
                                    'QPushButton:hover {\n'
                                    '   background: rgb(1, 100, 105);\n'
                                    '}\n'
                                    'QPushButton:pressed {\n'
                                    '   background: rgb(0, 65, 69);\n'
                                    '}\n')
        self.backBtn.setFont(QtGui.QFont('Arial', 12, 900))
        self.backBtn.setText('Back')
        self.backBtn.setFixedHeight(105)
        self.backBtn.setFixedWidth(225)
        self.backBtn.setGraphicsEffect(self.shadow5)
        self.backBtn.clicked.connect(self.goBack)

        self.btnRow = QWidget(self)
        self.btnRow.setStyleSheet(  'background: transparent;\n'
                                    'color: white;\n'
                                    'border: 0px solid white;\n')
        
        self.brl = QHBoxLayout()
        self.brl.addWidget(self.backBtn, alignment = QtCore.Qt.AlignLeft)
        self.brl.addWidget(self.proceedToPaymentBtn, alignment = QtCore.Qt.AlignRight)
        self.brl.setContentsMargins(0, 0, 0, 0)
        self.brl.setAlignment(QtCore.Qt.AlignVCenter)
        self.btnRow.setLayout(self.brl)

        self.centerWidget = QWidget(self)
        self.centerWidget.setStyleSheet(    'background: transparent;\n'
                                            'color: white;\n'
                                            'border: 0px solid white;\n')
        
        self.cwl = QVBoxLayout()
        self.cwl.addWidget(self.boxRow, alignment = QtCore.Qt.AlignVCenter)
        self.cwl.addWidget(self.btnRow, alignment = QtCore.Qt.AlignVCenter)
        self.cwl.setContentsMargins(0, 0, 0, 0)
        self.cwl.setSpacing(5)
        self.cwl.setAlignment(QtCore.Qt.AlignCenter)
        self.centerWidget.setLayout(self.cwl)

        if (status != 'Finished'):
            self.proceedToPaymentBtn.hide()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.statusLabel, alignment = QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.centerWidget, alignment = QtCore.Qt.AlignHCenter)
        # self.layout.addWidget(self.proceedToPaymentBtn, alignment = QtCore.Qt.AlignRight)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 50)
        self.layout.setSpacing(30)

        self.setLayout(self.layout)
    
    def goBack(self):
        self.hide()
        self.parent.parent.parent.sidebar.selectPage(self.parent.parent.parent.sidebar.dashboard, 'Dashboard')

    def downloadOutput(self):
        response = self.parent.parent.parent.sender.get_permission_to_download_output(self.jobId)

        if (response is not None):
            db_token, f_size = response
            home_dir = os.system("pwd>pwd.txt")
            f = open("pwd.txt", "r")
            x = f.readline()
            x = x.split("/")        
            y = "/" + x[1] + "/" + x[2] + "/rendt"
            home_dir = os.system("rm pwd.txt")
            home_dir = os.system("mkdir " + y)
            self.parent.parent.parent.sender.download_output_from_db(y + '/output.zip', db_token, f_size)

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
    
    def addRequests(self):
        self.requests = []
        
        while (not self.layout.isEmpty()):
            self.layout.removeWidget()

        stats = self.parent.parent.sender.get_job_statuses()

        for job in stats:
            request = RentingRequest(self, job)
            self.requests.append(request)
            self.layout.addWidget(request, alignment = QtCore.Qt.AlignTop)

    def darkTheme(self):
        self.setStyleSheet( 'background: rgb(69, 69, 69);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n'
                            'margin: 0px;\n')

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
        self.layout.setContentsMargins(30, 30, 30, 50)
        self.layout.setSpacing(10)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)
    
    def addRequests(self):
        self.requests = []
        requests = self.parent.parent.receiver.get_job_notifications()

        for r in requests:
            request = LeasingRequest(self)
            request.orderId = r[0]
            request.renterUserName = r[1]
            request.jobId = r[2]
            request.jobDesc = r[3]
            request.jobMode = r[4]
            request.status = r[5]
            
            request.setRenter(request.renterUserName)

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
                                        'margin-left: 10px;\n'
                                        'margin-bottom: 10px\n') 
        self.rentingLabel.setGraphicsEffect(self.shadow)

        self.rentingList = RentingList(self)
        if (self.parent.sender is not None):
            self.rentingList.addRequests()

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
        if (self.parent.receiver is not None):
            self.leasingList.addRequests()

        self.rw = QWidget(self)
        self.rw.setStyleSheet(  'background: transparent;\n'
                                'border: 0px solid white;\n')
        self.rwl = QVBoxLayout()
        self.rwl.addWidget(self.rentingLabel, alignment = QtCore.Qt.AlignLeft)
        self.rwl.addWidget(self.rentingList)
        self.rwl.setContentsMargins(0, 0, 0, 0)
        self.rwl.setAlignment(QtCore.Qt.AlignHCenter)
        self.rwl.setSpacing(10)
        self.rw.setLayout(self.rwl)

        self.lw = QWidget(self)
        self.lw.setStyleSheet(  'background: transparent;\n'
                                'border: 0px solid white;\n')
        self.lwl = QVBoxLayout()
        self.lwl.addWidget(self.leasingLabel, alignment = QtCore.Qt.AlignLeft)
        self.lwl.addWidget(self.leasingList)
        self.lwl.setContentsMargins(0, 0, 0, 0)
        self.lwl.setAlignment(QtCore.Qt.AlignHCenter)
        self.lwl.setSpacing(10)
        self.lw.setLayout(self.lwl)


        self.layout = QVBoxLayout()
        self.layout.addWidget(self.rw, alignment = QtCore.Qt.AlignTop)
        self.layout.addWidget(self.lw, alignment = QtCore.Qt.AlignTop)

        self.layout.setContentsMargins(30, 60, 30, 30)
        self.layout.setSpacing(10)
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

    def addRequests(self):
        self.rentingList.addRequests()
        self.leasingList.addRequests()

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