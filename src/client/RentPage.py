from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QMainWindow

import os

class CustomSquareButton(QPushButton):
    def __init__(self, parent):
        super(CustomSquareButton, self).__init__()

        self.parent = parent

        # self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # self.setSizePolicy(self.sizePolicy)
        self.setMinimumHeight(400)
        self.setMinimumWidth(400)

        self.setStyleSheet( 'QPushButton {\n'
                            '   background: rgba(155, 155, 155, 0.8);\n'
                            '   border: 0px solid white;\n'
                            '   color: white;\n'
                            '}\n'
                            'QPushButton:hover {\n'
                            '   background: rgba(100, 100, 100, 0.6);\n'
                            '}\n'
                            'QPushButton:pressed {\n'
                            '   background: rgba(100, 100, 100, 0.5);\n'
                            '}\n'
                            'QLabel {\n'
                            '   background: transparent;\n'
                            '   border: 0px solid white;\n'
                            '}\n')
        
        self.headerLabel = QLabel(self)
        self.headerLabel.setFont(QtGui.QFont('Arial', 20, 10000))
        self.headerLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.headerLabel.setStyleSheet('background: transparent')

        self.image = QLabel(self)
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        
        self.footerLabel = QLabel(self)
        self.footerLabel.setFont(QtGui.QFont('Arial', 10, 800))
        self.footerLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.footerLabel.setStyleSheet('color: rgba(200, 200, 200, 0.8)')

        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.setGraphicsEffect(self.shadow)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.image)
        self.layout.addWidget(self.footerLabel)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(self.layout)

    def setHeader(self, e):
        self.headerLabel.setText(e)
        self.headerLabel.adjustSize()
    
    def setImage(self, e):
        img = QtGui.QPixmap(e)
        self.image.setPixmap(img.scaled(
            100, 100, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))
    
    def setFooter(self, e):
        self.footerLabel.setText(e)
        self.footerLabel.adjustSize()

class LeaserRow(QWidget):
    def __init__(self, parent):
        super(LeaserRow, self).__init__()

        self.parent = parent
        self.clicked = None
        self.setMouseTracking(True)
        self.layout = None

    def setClicked(self, e):
        self.clicked = e

    def mousePressEvent(self, e):
        self.clicked(self) 

    def setOddStyle(self):
        self.setStyleSheet( 'QWidget {\n'
                            '  background: rgb(58, 58, 58);'
                            '  border: 0px solid white;\n'
                            '}\n'
                            'QWidget:hover {\n'
                            '  background: rgb(48, 48, 48);\n'
                            '}\n'
                            'QWidget:pressed {\n'
                            '  background: rgb(40, 40, 40);\n'
                            '}\n')
    
    def setEvenStyle(self):
        self.setStyleSheet( 'QWidget {\n'
                            '  background: rgb(81, 81, 81);'
                            '  border: 0px solid white;\n'
                            '}\n'
                            'QWidget:hover {\n'
                            '  background: rgb(65, 65, 65);\n'
                            '}\n'
                            'QWidget:pressed {\n'
                            '  background: rgb(50, 50, 50);\n'
                            '}\n')

class LeasersList(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWidgetResizable(True)

        self.form = QtWidgets.QFormLayout()
        # self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setSizeIncrement(50, 50)
        self.heightForWidth(True)
        self.setMinimumHeight(400)
        self.setMaximumWidth(1000)
        self.groupBox = QtWidgets.QGroupBox('')
        # self.groupBox.setContentsMargins(100, 100, 100, 100)
        self.leasers = []

        self.form.setContentsMargins(0, 65, 0, 0)
        self.form.setAlignment(QtCore.Qt.AlignHCenter)
        self.form.setSpacing(0)

        self.setStyleSheet( 'background: rgba(100, 100, 100, 0.8);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')
        
        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(10)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.setGraphicsEffect(self.shadow)

        leaserCol = QLabel()
        leaserCol.setText('leaser')
        leaserCol.setFont(QtGui.QFont('Arial', 12, 800))
        leaserCol.adjustSize()
        leaserCol.setStyleSheet('background: transparent;\n'
                                'border: 0px solid white;\n'
                                'color: white')
        leaserCol.setAlignment(QtCore.Qt.AlignLeft)

        specsCol = QLabel()
        specsCol.setText('specifications')
        specsCol.setFont(QtGui.QFont('Arial', 12, 800))
        specsCol.adjustSize()
        specsCol.setStyleSheet('background: transparent;\n'
                                'border: 0px solid white;\n'
                                'color: white')
        specsCol.setAlignment(QtCore.Qt.AlignHCenter)

        priceCol = QLabel()
        priceCol.setText('price')
        priceCol.setFont(QtGui.QFont('Arial', 12, 800))
        priceCol.adjustSize()
        priceCol.setStyleSheet('background: transparent;\n'
                                'border: 0px solid white;\n'
                                'color: white')
        priceCol.setAlignment(QtCore.Qt.AlignRight)

        colsRow = QWidget()
        colsRow.setStyleSheet('background: rgb(61, 61, 61);\n'
                                'border: 0px solid white;\n'
                                'color: white')
        colsRow.setFixedHeight(65)

        colsRowLayout = QHBoxLayout()
        colsRowLayout.addWidget(leaserCol, alignment = QtCore.Qt.AlignLeft)
        colsRowLayout.addWidget(specsCol, alignment = QtCore.Qt.AlignHCenter)
        colsRowLayout.addWidget(priceCol, alignment = QtCore.Qt.AlignRight)
        colsRowLayout.setAlignment(QtCore.Qt.AlignVCenter)
        colsRowLayout.setContentsMargins(40, 0, 40, 0)
        
        colsRow.setLayout(colsRowLayout)

        self.layout = QVBoxLayout()
        self.layout.addWidget(colsRow, alignment = QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 65)
        self.setLayout(self.layout)
        # self.setMouseTracking(True)

    def addLeaser(self, user, specs, price):
        widget = LeaserRow(self)
        layout = QHBoxLayout()
        
        leaser = QLabel()
        leaser.setText(user)
        leaser.setFont(QtGui.QFont('Arial', 12, 1000))
        leaser.adjustSize()
        leaser.setStyleSheet('background: transparent;\n'
                             'color: rgb(0, 200, 56);\n'
                             'border: 0px solid white;\n')
        leaser.setAlignment(QtCore.Qt.AlignLeft)
        # leaser.setFixedHeight(50)

        leaserSpecs = QLabel()
        leaserSpecs.setText(specs)
        leaserSpecs.setFont(QtGui.QFont('Arial', 12, 1000))
        leaserSpecs.adjustSize()
        leaserSpecs.setStyleSheet('background: transparent;\n'
                             'color: rgb(255, 255, 255);\n'
                             'border: 0px solid white;\n')
        leaserSpecs.setAlignment(QtCore.Qt.AlignCenter)
        # leaserSpecs.setFixedHeight(50)

        leaserPrice = QLabel()
        leaserPrice.setText(price)
        leaserPrice.setFont(QtGui.QFont('Arial', 12, 1000))
        leaserPrice.adjustSize()
        leaserPrice.setStyleSheet('background: transparent;\n'
                             'color: rgb(255, 255, 255);\n'
                             'border: 0px solid white;\n')
        leaserPrice.setAlignment(QtCore.Qt.AlignRight)
        # leaserPrice.setFixedHeight(50)


        layout.addWidget(leaser)
        layout.addWidget(leaserSpecs)
        layout.addWidget(leaserPrice)
        layout.setContentsMargins(30, 0, 30, 0)
        # layout.setSpacing(10)
        layout.setAlignment(QtCore.Qt.AlignVCenter)
        widget.layout = layout
        widget.setLayout(layout)
        widget.setFixedHeight(65)
        widget.setClicked(self.selectLeaser)
        # widget.setFixedWidth(807)

        if (self.form.rowCount() % 2 == 0):
            widget.setEvenStyle()
        else:
            widget.setOddStyle()

        self.form.addRow(widget)

        if (self.form.rowCount() == 1):
            self.groupBox.setLayout(self.form)
            self.setWidget(self.groupBox)
    
    def selectLeaser(self, e):
        leaser = e
        print(str(leaser))
        
        for i in range (self.form.rowCount()):
            widget = self.form.itemAt(i).widget()
            if (i % 2 == 0):
                widget.setEvenStyle()
            else:
                widget.setOddStyle()

        leaser.setStyleSheet(   'QWidget {\n'
                                '  background: rgb(120, 120, 120);'
                                '  border: 0px solid white;\n'
                                '}\n'
                                'QWidget:hover {\n'
                                '  background: rgb(120, 120, 120);\n'
                                '}\n'
                                'QWidget:pressed {\n'
                                '  background: rgb(120, 120, 120);\n'
                                '}\n')

        self.parent.selectedLeaser = leaser.layout.itemAt(0).widget().text()
        print('Selected Leaser: ' + leaser.layout.itemAt(0).widget().text())

# TODO: Filter and allow only ZIP files
class UploadPage(QWidget):
    def __init__(self, parent):
        super(UploadPage, self).__init__()

        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.sizePolicy.setHeightForWidth(True)

        self.parent = parent

        self.current_theme = self.parent.current_theme
        self.current_font = self.parent.current_font

        if (self.current_theme == 'Dark'):
            self.darkTheme()
        elif (self.current_theme == 'Light'):
            self.lightTheme()
        else:
            self.classicTheme()

        self.fileName = ''

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

        self.uploadFilesLabel = QLabel(self)
        self.uploadFilesLabel.setText('Upload files')
        self.uploadFilesLabel.setFont(QtGui.QFont('Arial', 40, 400))
        self.uploadFilesLabel.adjustSize()
        self.uploadFilesLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.uploadFilesLabel.setStyleSheet('background: transparent;\n'
                                            'border: 0px solid white;\n'
                                            'margin-top: 50px;\n'
                                            'font-weight: bold;\n')                    
        

        self.uploadZipBtn = CustomSquareButton(self)
        self.uploadZipBtn.setHeader('Upload .zip')
        self.uploadZipBtn.setImage('../../assets/img/zip_w.png')

        self.uploadZipBtn.setFooter('.zip file should include files to be executed\nwith necessary libraries and bash files etc.')   
        self.uploadZipBtn.clicked.connect(self.chooseFile)
        # self.uploadZipBtn.setGraphicsEffect(self.shadow)     

        self.uploadBtn = QPushButton(self)
        self.uploadBtn.setStyleSheet('QPushButton {\n'
                                     '   background: rgb(0, 149, 144);\n'
                                     '   color: white;\n'
                                     '   border: 0px solid white;\n'
                                     '   margin-bottom: 10px;\n'
                                     '}\n'
                                     'QPushButton:hover {\n'
                                     '   background: rgb(0, 120, 115);\n'
                                     '}\n'
                                     'QPushButton:pressed {\n'
                                     '   background: rgb(0, 75, 72);\n'
                                     '}\n')
        self.uploadBtn.setFont(QtGui.QFont('Arial', 12, 800))
        self.uploadBtn.setText('Upload')
        self.uploadBtn.setFixedHeight(65)
        self.uploadBtn.setFixedWidth(180)
        self.uploadBtn.clicked.connect(lambda:self.uploadFile(self.fileName))

        layout = QVBoxLayout()
        layout.addWidget(self.uploadFilesLabel, alignment = QtCore.Qt.AlignHCenter)
        layout.addWidget(self.uploadZipBtn, alignment = QtCore.Qt.AlignHCenter)
        layout.addWidget(self.uploadBtn, alignment = QtCore.Qt.AlignHCenter)
        layout.setAlignment(QtCore.Qt.AlignTop)
        # self.layout.setContentsMargins(50, 80, 50, 50)
        layout.setSpacing(30)

        widget = QWidget(self)
        widget.setLayout(layout)

        self.uploadFilesLabel.setGraphicsEffect(self.shadow)
        self.uploadBtn.setGraphicsEffect(self.shadow2)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widget)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def chooseFile(self):
        dialog = QtWidgets.QFileDialog()
        fileName = dialog.getOpenFileName(self, 'Open file', '.')
        self.fileName = fileName[0]
        print('File name: ' + str(self.fileName))
    
    def uploadFile(self, e):
        if (len(self.fileName) > 0):
            job_id, db_token = self.parent.parent.sender.get_permission_to_upload_job(e, 'test')
            self.parent.parent.sender.upload_file_to_db(e, job_id, db_token)
            self.goToRentalTypePage(job_id)
            self.parent.fileName = self.fileName
        else:
            print("Choose file")

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
    
    def goToRentalTypePage(self, jobId):
        self.parent.rentalTypePage.show()
        self.parent.rentalTypePage.setJobId(jobId)
        self.parent.leasersListPage.hide()

class RentalTypePage(QWidget):
    def __init__(self, parent):
        super(RentalTypePage, self).__init__()

        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.sizePolicy.setHeightForWidth(True)

        self.parent = parent
        self.jobId = None

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

        self.selectRentalTypeLabel = QLabel(self)
        self.selectRentalTypeLabel.setText('Select rental type')
        self.selectRentalTypeLabel.setFont(QtGui.QFont('Arial', 40, 400))
        self.selectRentalTypeLabel.adjustSize()
        self.selectRentalTypeLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.selectRentalTypeLabel.setStyleSheet('background: transparent;\n'
                                                 'border: 0px solid white;\n'
                                                 'margin-top: 50px;\n'
                                                 'font-weight: bold;\n')                    

        self.singularBtn = CustomSquareButton(self)
        self.singularBtn.setHeader('Singular')
        self.singularBtn.setImage('../../assets/img/cpu_w.png')
        self.singularBtn.setFooter('Singular rentals use single machine and leaser for\ncomputations and run on one machine')   
        self.singularBtn.clicked.connect(self.goToLeasersListPage)

        self.distributedBtn = CustomSquareButton(self)
        self.distributedBtn.setHeader('Distributed')
        self.distributedBtn.setImage('../../assets/img/distributed_w.png')
        self.distributedBtn.setFooter('Distributed rentals use multiple machines for\n computations to make the execution faster for\nparallel programs')   
        # self.distributedBtn.setGraphicsEffect(self.shadow)     

        self.buttonsRow = QWidget()
        self.buttonsRowLayout = QHBoxLayout()
        self.buttonsRowLayout.addWidget(self.singularBtn, alignment = QtCore.Qt.AlignLeft)
        self.buttonsRowLayout.addWidget(self.distributedBtn, alignment = QtCore.Qt.AlignRight)
        self.buttonsRow.setLayout(self.buttonsRowLayout)
        self.buttonsRowLayout.setAlignment(QtCore.Qt.AlignJustify)
        self.buttonsRowLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsRowLayout.setSpacing(40)
        self.buttonsRow.setFixedWidth(900)
        self.buttonsRow.setFixedHeight(430)

        layout = QVBoxLayout()
        layout.addWidget(self.selectRentalTypeLabel, alignment = QtCore.Qt.AlignHCenter)
        layout.addWidget(self.buttonsRow, alignment = QtCore.Qt.AlignHCenter)
        layout.setAlignment(QtCore.Qt.AlignTop)
        # self.layout.setContentsMargins(50, 80, 50, 50)
        layout.setSpacing(10)

        widget = QWidget(self)
        widget.setLayout(layout)

        self.selectRentalTypeLabel.setGraphicsEffect(self.shadow)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widget)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def setJobId(self, e):
        self.jobId = e

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
    
    def goToLeasersListPage(self):
        self.parent.leasersListPage.show()
        self.parent.leasersListPage.getAvalLeasers()
        self.parent.leasersListPage.setJobId(self.jobId)

class LeasersListPage(QWidget):
    def __init__(self, parent):
        super(LeasersListPage, self).__init__()

        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.sizePolicy.setHeightForWidth(True)

        self.parent = parent
        self.jobId = None
        self.selectedLeaser = None

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

        self.shadow2 = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow2.setBlurRadius(30)
        self.shadow2.setXOffset(0)
        self.shadow2.setYOffset(0)
        self.shadow2.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.leasersLabel = QLabel(self)
        self.leasersLabel.setText('Leasers')
        self.leasersLabel.setFont(QtGui.QFont('Arial', 40, 400))
        self.leasersLabel.adjustSize()
        self.leasersLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.leasersLabel.setStyleSheet('background: transparent;\n'
                                        'border: 0px solid white;\n'
                                        'margin-top: 50px;\n'
                                        'font-weight: bold;\n')
        self.leasersLabel.setGraphicsEffect(self.shadow2)
        
        self.leasersList = LeasersList(self)
        
        self.sendReqBtn = QPushButton(self)
        self.sendReqBtn.setStyleSheet('QPushButton {\n'
                                     '   background: rgb(0, 149, 144);\n'
                                     '   color: white;\n'
                                     '   border: 0px solid white;\n'
                                     '}\n'
                                     'QPushButton:hover {\n'
                                     '   background: rgb(0, 120, 115);\n'
                                     '}\n'
                                     'QPushButton:pressed {\n'
                                     '   background: rgb(0, 75, 72);\n'
                                     '}\n')
        self.sendReqBtn.setFont(QtGui.QFont('Arial', 12, 800))
        self.sendReqBtn.setText('Send request')
        self.sendReqBtn.setFixedHeight(55)
        self.sendReqBtn.setFixedWidth(180)
        self.sendReqBtn.setGraphicsEffect(self.shadow)
        self.sendReqBtn.clicked.connect(self.sendReq)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.leasersLabel)
        self.layout.addWidget(self.leasersList)
        self.layout.addWidget(self.sendReqBtn, alignment = QtCore.Qt.AlignCenter)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(50, 0, 50, 50)
        self.layout.setAlignment(QtCore.Qt.AlignHCenter)
        self.setLayout(self.layout)

    def sendReq(self):
        self.parent.parent.sender.submit_job_order(int(self.jobId), self.selectedLeaser)
        # self.parent.parent.rentPage = RentPage(self.parent.parent)

    def setJobId(self, jobId):
        self.jobId = jobId

    def getAvalLeasers(self):
        leasers = self.parent.parent.sender.get_available_leasers()
        print('Leasers: \n---------------------\n' + str(leasers))
        
        for l in leasers:
            self.leasersList.addLeaser(str(l[0]), l[1], '3$/h')

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

class RentPage(QScrollArea):
    def __init__(self, parent):
        super(RentPage, self).__init__()

        self.parent = parent
        self.setStyleSheet("background: rgb(57, 57, 57);\n"
                           "border: 0px solid rgb(25, 118, 210);\n"
                           "color: white;\n")

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setWidgetResizable(True)

        self.fileName = None
        self.current_theme = self.parent.current_theme
        self.current_font = self.parent.current_font

        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.uploadPage = UploadPage(self)
        self.rentalTypePage = RentalTypePage(self)
        self.leasersListPage = LeasersListPage(self)
        self.rentalTypePage.hide()
        self.leasersListPage.hide()

        widget = QWidget(self)
        layout = QVBoxLayout()

        layout.addWidget(self.uploadPage)
        layout.addWidget(self.rentalTypePage)
        layout.addWidget(self.leasersListPage)
        layout.setContentsMargins(0, 0, 0, 50)
        layout.setAlignment(QtCore.Qt.AlignHCenter)
        layout.setSpacing(30)

        widget.setLayout(layout)
        widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.setWidget(widget)