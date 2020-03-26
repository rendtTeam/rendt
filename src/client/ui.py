import sys
import os
import psutil
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget

import sender
import receiver

class TaskFinishedWindow(QWidget):
    def __init__(self, parent):
        super(TaskFinishedWindow, self).__init__(parent)
        layout = QVBoxLayout()

        self.backBtn = QPushButton(self)
        self.backBtn.setText('<')
        self.backBtn.setStyleSheet( 'background: transparent;\n'
                                    'color: white;\n'
                                    'border: 1px solid white;\n')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.setFixedHeight(10)
        self.backBtn.setFixedWidth(10)
        self.backBtn.clicked.connect(parent.goBack)

        label = QLabel(self)
        label.setText('Task finished successfully')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)

        label.setFont(font)
        label.adjustSize()

        self.label = label

        self.layout = layout
        self.layout.addWidget(self.backBtn)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


class ReceivedWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel(self)
        label.setText('Files successfully received')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)

        label.setFont(font)
        label.adjustSize()

        self.label = label
        self.label.setGeometry(QtCore.QRect(135, 100, 144, 17))

        self.layout = layout
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


class WaitingWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WaitingWindow, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout()
        
        self.waitingLabel = QtWidgets.QLabel(self)
        self.waitingLabel.setStyleSheet('color: white')
        self.waitingLabel.setGeometry(QtCore.QRect(135, 100, 144, 17))
        self.waitingLabel.setText('Waiting...')

        self.backBtn = QPushButton(self)
        self.backBtn.setGeometry(QtCore.QRect(0, 0, 20, 20))
        self.backBtn.setText('<')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.clicked.connect(parent.goBack)
        self.backBtn.setFixedWidth(10)
        self.backBtn.setFixedHeight(10)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.waitingLabel.setFont(font)
        self.waitingLabel.setObjectName("waitingLabel")
        self.waitingLabel.adjustSize()

        # self.layout.addWidget(self.backBtn)
        self.layout.addWidget(self.waitingLabel)
        self.setLayout(self.layout)

class JobsFrame(QScrollArea):
    def __init__(self, parent):
        super().__init__()
        self.all_jobs = []
        self.container = parent
        self.setFixedHeight(241)
        self.setStyleSheet( 'background: transparent;\n'
                            'border: 1px solid white;\n'
                            'color: white;\n')        
        self.form = QtWidgets.QFormLayout()
        self.groupBox = QtWidgets.QGroupBox('')
        self.setWidgetResizable(True)
        self.updateJobs()

    def updateJobs(self):
        jobs = self.container.receiveJobs()

        for job in jobs:
            if (job not in self.all_jobs):
                self.addJob(job)

    def addJob(self, e):
        self.all_jobs.append(e)
        jobId = QLabel(str(e))
        jobId.setFont(QtGui.QFont('Arial', 11))
        jobId.adjustSize()

        jobExecBtn = QPushButton(self)
        jobExecBtn.jobId = e
        jobExecBtn.setText('Run')
        jobExecBtn.setFixedWidth(50)
        jobExecBtn.setFont(QtGui.QFont('Arial', 11))
        jobExecBtn.setStyleSheet(   'QPushButton {\n'
                                    '   background: transparent;\n'
                                    '   color: white;\n'
                                    '   border: 1px solid white;}\n'
                                    'QPushButton:hover {\n'
                                    '   background: rgb(76, 175, 80);\n'
                                    '   border: rgb(76, 175, 80);}\n'
                                    'QPushButton:clicked {\n'
                                    '   background: rgb(46, 125, 50);\n'
                                    '   border: rgb(46, 125, 50);}\n')

        jobExecBtn.clicked.connect(self.container.execJob)
        self.form.addRow(jobId, jobExecBtn)
        self.groupBox.setLayout(self.form)
        self.setWidget(self.groupBox)

class AvailableJobs(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.backBtn = QPushButton(self)
        self.backBtn.setText('<')
        self.backBtn.setStyleSheet( 'background: transparent;\n'
                                    'color: white;\n'
                                    'border: 1px solid white;\n')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.setFixedHeight(10)
        self.backBtn.setFixedWidth(10)
        self.backBtn.clicked.connect(parent.goBack)

        self.refreshBtn = QPushButton(self)
        self.refreshBtn.setText('Refresh')
        self.refreshBtn.setStyleSheet( 'background: transparent;\n'
                                    'color: white;\n'
                                    'border: 1px solid white;\n')
        self.refreshBtn.setFont(QtGui.QFont('Arial', 12))
        self.refreshBtn.setFixedHeight(20)
        self.refreshBtn.setFixedWidth(40)
        

        self.label = QLabel('Available Jobs: ')
        self.label.setFont(QtGui.QFont('Arial', 20))
        self.label.adjustSize()
        self.label.setFixedHeight(25)

        self.jobsFrame = JobsFrame(parent)
        self.refreshBtn.clicked.connect(self.jobsFrame.updateJobs)
        
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.backBtn)
        self.layout.addWidget(self.refreshBtn)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.jobsFrame)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.setLayout(self.layout)

class HardwareInfoWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.container = parent
        self.label = QLabel('Hardware Information\n')
        self.label.setFont(QtGui.QFont('Arial', 20))
        self.label.adjustSize()

        self.physCores = QLabel('Physical Cores: ' + str(psutil.cpu_count(logical = False)))
        self.totalCores = QLabel('Total Cores: ' + str(psutil.cpu_count(logical = True)) + '\n')

        self.maxFreq = QLabel(f'Max Frequency: {psutil.cpu_freq().max: .2f} MHz')
        self.minFreq = QLabel(f'Min Frequency: {psutil.cpu_freq().min: .2f} MHz')
        self.curFreq = QLabel(f'Current Frequency: {psutil.cpu_freq().current: .2f} MHz\n')
        
        self.totalMem = QLabel(f'Total: {self.get_size(psutil.virtual_memory().total)}')
        self.avalMem = QLabel(f'Available: {self.get_size(psutil.virtual_memory().available)}')
        self.usedMem = QLabel(f'Used: {self.get_size(psutil.virtual_memory().used)}')
        self.percentMem = QLabel(f'Percentage: {self.get_size(psutil.virtual_memory().percent)}%\n')

        self.physCores.setFont(QtGui.QFont('Arial', 14))
        self.physCores.adjustSize()
        self.totalCores.setFont(QtGui.QFont('Arial', 14))
        self.totalCores.adjustSize()
        self.maxFreq.setFont(QtGui.QFont('Arial', 14))
        self.maxFreq.adjustSize()
        self.minFreq.setFont(QtGui.QFont('Arial', 14))
        self.minFreq.adjustSize()
        self.curFreq.setFont(QtGui.QFont('Arial', 14))
        self.curFreq.adjustSize()
        self.totalMem.setFont(QtGui.QFont('Arial', 14))
        self.totalMem.adjustSize()
        self.avalMem.setFont(QtGui.QFont('Arial', 14))
        self.avalMem.adjustSize()
        self.usedMem.setFont(QtGui.QFont('Arial', 14))
        self.usedMem.adjustSize()
        self.percentMem.setFont(QtGui.QFont('Arial', 14))
        self.percentMem.adjustSize()

        self.startBtn = QPushButton(self)
        self.startBtn.setFont(QtGui.QFont('Arial', 14))
        self.startBtn.setText('Lease')
        self.startBtn.setStyleSheet('background: transparent;\n'
                                    'border: 1px solid white;\n'
                                    'color: white;\n')
        self.startBtn.setFixedWidth(50)
        self.startBtn.clicked.connect(self.container.showAvailableJobs)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.physCores)
        self.layout.addWidget(self.totalCores)
        self.layout.addWidget(self.maxFreq)
        self.layout.addWidget(self.minFreq)
        self.layout.addWidget(self.curFreq)
        self.layout.addWidget(self.totalMem)
        self.layout.addWidget(self.avalMem)
        self.layout.addWidget(self.usedMem)
        self.layout.addWidget(self.percentMem)
        self.layout.addWidget(self.startBtn)

        self.setLayout(self.layout)


    #* Reference: https://www.thepythoncode.com/article/get-hardware-system-information-python 
    def get_size(self, bytes, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor


class ReceiverWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.container = parent
        self.started = False
    
    def startWindow(self):
        self.started = True
        self.container.setWindowTitle('Rendt Receiver Demo')
        self.setWindowIcon(QtGui.QIcon(
            '../../assets/img/rendt_new_logo_square.png'))
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setStyleSheet("QPushButton {\n"
                           "    background: rgb(232, 232, 232);\n"
                           "    border: 1px solid rgb(227, 227, 227);\n"
                           "    color: white;\n"
                           "}\n"
                           "\n"
                           "QPushButton:hover {\n"
                           "    background: rgb(200, 200, 200);\n"
                           "}\n"
                           "\n"
                           "QPushButton:pressed {\n"
                           "    background: rgb(150, 150, 150);\n"
                           "}\n"
                           "\n"
                           "QWidget {\n"
                           "    background: rgb(120, 120, 120);\n"
                           "}\n"
                           "\n"
                           "")

        # Setting up the layout
        self.layout = QVBoxLayout()

        # Adding back button
        self.backBtn = QPushButton(self)
        self.backBtn.setGeometry(QtCore.QRect(0, 0, 20, 20))
        self.backBtn.setText('<')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.clicked.connect(self.goBack)
        self.backBtn.hide()

        # Setting up Waiting Screen
        self.waitingWindow = WaitingWindow(self)
        self.waitingWindow.hide()

        # Setting up Received Window
        self.receivedWindow = ReceivedWindow()
        self.receivedWindow.hide()

        # Setting up Task Finished Window
        self.taskFinishedWindow = TaskFinishedWindow(self)
        self.taskFinishedWindow.hide()

        # Adding Hardware Info Window
        self.hardwareInfoWindow = HardwareInfoWindow(self)

        # Adding Available Jobs Window
        self.availableJobs = AvailableJobs(self)
        self.availableJobs.hide()

        # Adding everything into the layout
        self.layout.addWidget(self.backBtn)
        self.layout.addWidget(self.waitingWindow)
        self.layout.addWidget(self.receivedWindow)
        self.layout.addWidget(self.taskFinishedWindow)
        self.layout.addWidget(self.hardwareInfoWindow)
        self.layout.addWidget(self.availableJobs)

        self.setLayout(self.layout)

    def execJob(self):
        self.availableJobs.hide()
        self.waitingWindow.show()

        # Getting sent job Id from Push Button
        job_id = self.sender().jobId

        # Getting permission for execution
        db_token, size = receiver.get_permission_to_execute_task(job_id)

        # Downloading file to be executed
        receiver.download_file_from_db('sender_job.py', db_token, size)

        # Executing downloaded file
        receiver.execute_job('sender_job.py', f'sender_output.txt')

        # Getting permission to upload output from execution
        out_db_token = receiver.get_permission_to_upload_output(job_id, 'sender_output.txt')

        # Uploading execution output
        receiver.upload_output_to_db('sender_output.txt', job_id, out_db_token)

        self.waitingWindow.hide()
        self.taskFinishedWindow.show()

    def receiveJobs(self):
        return receiver.get_available_jobs()
        # # Show received message
        # self.waitingWindow.hide()
        # self.receivedWindow.show()

        # # Show execution finished
        # self.receiver.execute()
        # self.receivedWindow.hide()
        # self.taskFinishedWindow.show()
    
    def goBack(self):
        self.hideWindow()
        self.container.resetUi()
    
    def hideWindow(self):
        self.waitingWindow.hide()
        self.taskFinishedWindow.hide()
        self.backBtn.hide()
        self.hardwareInfoWindow.hide()
        self.availableJobs.hide()

    def showWindow(self):
        self.container.setWindowTitle('Rendt Receiver Demo')
        self.hardwareInfoWindow.show()
        # self.waitingWindow.show()
    
    def showAvailableJobs(self):
        self.hardwareInfoWindow.hide()
        self.availableJobs.show()


class FileButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.file_src = ''

    def setFileSource(self, e):
        self.file_src = e

    def getFileSource(self):
        return self.file_src


class ScrollFrame(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.form = QtWidgets.QFormLayout()
        self.setFixedHeight(121)
        self.container = parent
        self.groupBox = QtWidgets.QGroupBox('')
        self.files = []

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
            print('Accepted')
        else:
            e.ignore()
            print('Ignored')
        self.setStyleSheet("background: rgb(30, 136, 229);\n"
                           "border: 1px solid rgb(25, 118, 210);\n"
                           "color: white")

    def dragLeaveEvent(self, e):
        self.setStyleSheet("background: rgb(150, 150, 150);\n"
                           "border: 1px solid rgb(150, 150, 150);\n"
                           "color: white")

    def dropEvent(self, e):
        self.setStyleSheet("QScrollArea{\n"
                           "    color: white;\n"
                           "}\n"
                           "QLabel{\n"
                           "    color: white;\n"
                           "}\n"
                           "QPushButton {\n"
                           "    background: rgb(232, 232, 232);\n"
                           "    color: white;\n"
                           "    border: 1px solid rgb(227, 227, 227);\n"
                           "}\n"
                           "\n"
                           "QPushButton:hover {\n"
                           "    background: rgb(255,0,0);\n"
                           "    border: 1px solid rgb(255,0,0);\n"
                           "}\n"
                           "\n"
                           "QPushButton:pressed {\n"
                           "    background: rgb(182,0,0);\n"
                           "    border: 1px solid rgb(182,0,0);\n"
                           "}\n"
                           "\n"
                           "QWidget {\n"
                           "    background: rgb(120, 120, 120);\n"
                           "}\n"
                           "\n"
                           "")
        if (self.form.rowCount() == 0):
            self.container.switchLabel(False)

        for url in e.mimeData().urls():
            f, file_src = str(url.toString()).split('///')
            file_dir, file_name = os.path.split(file_src)

            print(file_src)
            label = QLabel(file_name)
            btn = FileButton('Remove')

            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)

            label.setFont(font)
            label.setFixedWidth(270)
            btn.setFont(font)
            btn.setFixedWidth(50)
            btn.setFixedHeight(20)

            btn.setFileSource(str(file_src))
            btn.clicked.connect(self.clickedRemove)

            self.form.addRow(label, btn)

        self.groupBox.setLayout(self.form)
        self.setWidget(self.groupBox)

    def clickedRemove(self):
        self.form.removeRow(self.sender())

        if (self.form.rowCount() == 0):
            self.container.switchLabel(True)

    def uploadFiles(self):
        for i in range(self.form.rowCount() * 2):
            if (i % 2):
                self.files.append(self.form.itemAt(i).widget().getFileSource())

        for f in self.files:
            print(f'File: {f}')
            filelist.append(f)


class OutputFrame(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.form = QtWidgets.QFormLayout()
        self.setFixedHeight(121)
        self.container = parent
        self.groupBox = QtWidgets.QGroupBox('')
        self.files = []

    def addLine(self, e):
        label = QLabel(e)
        label.setStyleSheet('color: white')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        label.setFont(font)
        label.setFixedHeight(14)
        label.adjustSize()

        self.form.addRow(label)
        self.groupBox.setLayout(self.form)
        self.setWidget(self.groupBox)


class LoadingWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LoadingWindow, self).__init__(parent)
        self.loadingLabel = QtWidgets.QLabel(self)
        self.loadingLabel.setStyleSheet('color: white')
        self.loadingLabel.setGeometry(QtCore.QRect(135, 100, 144, 17))
        self.loadingLabel.setText('Loading...')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.loadingLabel.setFont(font)
        self.loadingLabel.setObjectName("loadingLabel")
        self.loadingLabel.adjustSize()


class UploadFinishedWindow(QWidget):
    def __init__(self, parent):
        super(UploadFinishedWindow, self).__init__(parent)
        self.container = parent

    def startWindow(self, job_id):
        self.layout = QVBoxLayout()

        self.backBtn = QPushButton(self)
        self.backBtn.setText('<')
        self.backBtn.setStyleSheet( 'background: transparent;\n'
                                    'color: white;\n'
                                    'border: 1px solid white;\n')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.setFixedHeight(20)
        self.backBtn.setFixedWidth(20)
        self.backBtn.clicked.connect(self.container.goBack)

        self.label = QLabel(self)
        self.label.setText('Files uploaded successfully')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)

        self.label.setFont(font)
        self.label.adjustSize()
        self.label.setGeometry(QtCore.QRect(135, 100, 144, 30))

        self.downloadId = QLabel(self)
        self.downloadId.setText('Job ID: ' + str(job_id))
        self.downloadId.setFont(QtGui.QFont('Arial', 20))
        self.downloadId.setGeometry(QtCore.QRect(150, 130, 144, 22))
        self.downloadId.adjustSize()

        self.layout.addWidget(self.backBtn)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.downloadId)
        self.setLayout(self.layout)


class DownloadWindow(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.container = parent
        self.layout = QVBoxLayout()
        self.setStyleSheet('color: white')

        self.label = QLabel(self)
        self.label.setText('Download executed files with Job ID')
        self.label.setFont(QtGui.QFont('Arial', 20))
        self.label.setGeometry(QtCore.QRect(50, 60, 20, 22))
        self.label.adjustSize()

        self.jobIdLabel = QLabel(self)
        self.jobIdLabel.setText('Job ID: ')
        self.jobIdLabel.setFont(QtGui.QFont('Arial', 14))
        self.jobIdLabel.setGeometry(QtCore.QRect(50, 100, 20, 16))
        self.jobIdLabel.adjustSize()

        self.jobId = QtWidgets.QLineEdit(self)
        self.jobId.setFont(QtGui.QFont('Arial', 14))
        self.jobId.setStyleSheet(   'background: white;\n'
                                    'border: 1px solid transparent;\n'
                                    'color: black;\n')
        self.jobId.setGeometry(QtCore.QRect(100, 100, 100, 16))

        self.sendBtn = QPushButton(self)
        self.sendBtn.setText('Send')
        self.sendBtn.setFont(QtGui.QFont('Arial', 12))
        self.sendBtn.setStyleSheet( "QPushButton:hover {\n"
                                    "    background: rgb(200, 200, 200);\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:pressed {\n"
                                    "    background: rgb(150, 150, 150);\n"
                                    "}\n"
                                    "QPushButton {\n"
                                    "   background: transparent;\n"
                                    "   border: 1px solid rgb(227, 227, 227);\n"
                                    "   color: white;\n}\n")
        self.sendBtn.setGeometry(QtCore.QRect(202, 100, 50, 16))
        self.sendBtn.clicked.connect(self.downloadFile)

        # Adding back button
        self.backBtn = QPushButton(self)
        self.backBtn.setGeometry(QtCore.QRect(0, 0, 20, 20))
        self.backBtn.setText('<')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.clicked.connect(self.container.goBack)

        # Adding download files button
        self.uploadBtn = QPushButton(self)
        self.uploadBtn.setText('Upload')
        self.uploadBtn.setFont(QtGui.QFont('Arial', 12))
        self.uploadBtn.setGeometry(22, 0, 50, 20)
        self.uploadBtn.clicked.connect(self.startUploadWindow)

        # Adding Download Finished Successfully Label
        self.downloadFinishedLabel = QLabel(self)
        self.downloadFinishedLabel.setText('Download Finished Successfully')
        self.downloadFinishedLabel.setGeometry(QtCore.QRect(50, 60, 20, 22))
        self.downloadFinishedLabel.setFont(QtGui.QFont('Arial', 20))
        self.downloadFinishedLabel.adjustSize()
        self.downloadFinishedLabel.hide()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.jobIdLabel)
        self.layout.addWidget(self.jobId)
        self.layout.addWidget(self.sendBtn)
        self.layout.addWidget(self.backBtn)
        self.layout.addWidget(self.uploadBtn)
        self.layout.addWidget(self.downloadFinishedLabel)

        # self.setLayout(self.layout)

    def startUploadWindow(self):
        self.destroy()
        self.container.resetUi()
    
    def downloadFile(self):
        job_id = int(str(self.jobId.text()))
        perm = sender.get_permission_to_download_output(job_id)

        if perm:
            out_db_token, file_size = perm
            sender.download_output_from_db('received_output.txt', out_db_token, file_size)

        self.label.hide()
        self.jobId.hide()
        self.jobIdLabel.hide()
        self.sendBtn.hide()
        self.backBtn.show()
        self.uploadBtn.hide()
        self.downloadFinishedLabel.show()
        

class SenderWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.container = parent
        self.started = False

    def startWindow(self):
        self.started = True
        self.container.setWindowTitle('Rendt Sender Demo')
        self.setWindowIcon(QtGui.QIcon(
            '../../assets/img/rendt_new_logo_square.png'))
        # self.resize(600, 300)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setStyleSheet("QPushButton {\n"
                           "    background: rgb(232, 232, 232);\n"
                           "    border: 1px solid rgb(227, 227, 227);\n"
                           "    color: white;\n"
                           "}\n"
                           "\n"
                           "QPushButton:hover {\n"
                           "    background: rgb(200, 200, 200);\n"
                           "}\n"
                           "\n"
                           "QPushButton:pressed {\n"
                           "    background: rgb(150, 150, 150);\n"
                           "}\n"
                           "\n"
                           "QWidget {\n"
                           "    background: rgb(120, 120, 120);\n"
                           "}\n"
                           "\n"
                           "")

        # Setting up the layout
        self.layout = QVBoxLayout()

        # Adding back button
        self.backBtn = QPushButton(self)
        self.backBtn.setGeometry(QtCore.QRect(0, 0, 20, 20))
        self.backBtn.setText('<')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.clicked.connect(self.goBack)

        # Adding download files button
        self.downloadBtn = QPushButton(self)
        self.downloadBtn.setText('Download')
        self.downloadBtn.setFont(QtGui.QFont('Arial', 12))
        self.downloadBtn.setGeometry(22, 0, 70, 20)
        self.downloadBtn.clicked.connect(self.startDownloadWindow)

        # Setting up the label and configuring it
        self.label = QLabel(self)
        self.label.setText('Drag & Drop')
        self.label.setGeometry(QtCore.QRect(30, 20, 210, 43))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")

        # Adding Scroll Frame where the Dragging and Dropping will happen
        self.scroll = ScrollFrame(self)
        self.scroll.setGeometry(QtCore.QRect(30, 70, 361, 121))
        self.scroll.setStyleSheet("background: rgb(150, 150, 150);\n"
                                  "border: 1px solid rgb(150, 150, 150);\n")
        self.scroll.setWidgetResizable(True)

        # Adding Download Window
        self.downloadWindow = DownloadWindow(self)
        self.downloadWindow.hide()

        # Setting up the label inside the frame and configuring it
        self.uploadLabel = QLabel(self.scroll)
        self.uploadLabel.setStyleSheet('color: white')
        self.uploadLabel.setGeometry(QtCore.QRect(100, 50, 144, 17))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)

        self.uploadLabel.setFont(font)
        self.uploadLabel.setObjectName("uploadLabel")
        self.uploadLabel.setText('Drag & Drop files here')
        self.uploadLabel.adjustSize()

        # Adding the 'Upload' button and configuring it
        self.uploadBtn = QPushButton(self)
        self.uploadBtn.setGeometry(QtCore.QRect(320, 200, 71, 31))
        self.uploadBtn.setText('Upload')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.uploadBtn.setFont(font)
        self.uploadBtn.setStyleSheet("color: white;")
        self.uploadBtn.setObjectName("uploadBtn")
        self.uploadBtn.clicked.connect(self.startLoadingWindow)

        # Setting up Loading Screen
        self.loadingWindow = LoadingWindow(self)
        self.loadingWindow.hide()

        # Adding Output Details Label
        self.outputDetailsLabel = QLabel(self)
        self.outputDetailsLabel.setText('Received Output')
        self.outputDetailsLabel.setGeometry(QtCore.QRect(30, 20, 210, 43))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.outputDetailsLabel.setFont(font)
        self.outputDetailsLabel.setStyleSheet("color: white;")
        self.outputDetailsLabel.adjustSize()
        self.outputDetailsLabel.hide()

        # Adding Ouput Frame
        self.outputFrame = OutputFrame(self)
        self.outputFrame.setGeometry(QtCore.QRect(30, 70, 361, 121))
        self.outputFrame.setStyleSheet("background: rgb(150, 150, 150);\n"
                                       "border: 1px solid rgb(150, 150, 150);\n")
        self.outputFrame.setWidgetResizable(True)
        self.outputFrame.hide()

        # Adding Upload Finished Window
        self.uploadFinishedWindow = UploadFinishedWindow(self)
        self.uploadFinishedWindow.hide()

        # Adding everything into the layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.uploadLabel)
        self.layout.addWidget(self.uploadBtn)
        self.layout.addWidget(self.loadingWindow)
        self.layout.addWidget(self.outputDetailsLabel)
        self.layout.addWidget(self.outputFrame)
        self.layout.addWidget(self.uploadFinishedWindow)
        self.layout.addWidget(self.backBtn)
        self.layout.addWidget(self.downloadWindow)
    
    def startDownloadWindow(self):
        self.label.hide()
        self.scroll.hide()
        self.uploadLabel.hide()
        self.uploadBtn.hide()
        self.backBtn.hide()
        self.downloadBtn.hide()
        self.downloadWindow.show()

    def startLoadingWindow(self):
        self.label.hide()
        self.scroll.hide()
        self.uploadLabel.hide()
        self.uploadBtn.hide()
        self.loadingWindow.show()

        self.scroll.uploadFiles()
        job_id, db_token = sender.get_permission_to_submit_task(filelist[0])
        sender.upload_file_to_db(filelist[0], job_id, db_token)

        self.loadingWindow.hide()
        self.downloadWindow.hide()
        self.hideWindow()
        self.uploadFinishedWindow.startWindow(job_id)
        self.uploadFinishedWindow.show()

    # def startUploadFinishedWindow(self):
    #     self.scroll.uploadFiles()
    #     self.loadingWindow().hide()
    #     self.uploadFinishedWindow()

    def switchLabel(self, flag):
        if (flag):
            self.uploadLabel.show()
        else:
            self.uploadLabel.hide()
    
    def goBack(self):
        self.container.resetUi()
    
    def resetUi(self):
        self.downloadWindow.hide()
        self.label.show()
        self.scroll.show()
        self.uploadLabel.show()
        self.uploadBtn.show()
        self.backBtn.show()
        self.downloadBtn.show()
    
    def hideWindow(self):
        self.label.hide()
        self.scroll.hide()
        self.uploadLabel.hide()
        self.uploadBtn.hide()
        self.backBtn.hide()
        self.downloadBtn.hide()
        self.downloadWindow.hide()
        self.uploadFinishedWindow.hide()
        self.loadingWindow.hide()
        self.outputDetailsLabel.hide()
        self.outputFrame.hide()
    
    def showWindow(self):
        self.container.setWindowTitle('Rendt Sender Demo')
        self.label.show()
        self.scroll.show()
        self.uploadLabel.show()
        self.uploadBtn.show()
        self.backBtn.show()
        self.downloadBtn.show()


class RenterButton(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.container = parent
        self.layout = QVBoxLayout()
        self.setStyleSheet('QWidget {\nbackground: transparent;\n'
                           'border: 1px solid white;\n'
                           'border-radius: 10px;\n'
                           'color: white;\n}\n'
                           'QWidget:hover {\n'
                           'background: rgba(100, 100, 100, 0.3)\n}\n'
                           'QWidget:clicked {\n'
                           'background: rgba(50, 50, 50, 0.3)\n}\n')

        self.label = QLabel(self)
        self.label.setText('rent')
        self.label.setFont(QtGui.QFont('Arial', 36))
        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.adjustSize()

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setMouseTracking(True)
        self.clicked = self.container.startSenderWindow

    def mousePressEvent(self, e):
        self.clicked()
    
    def changeClickedEvent(self, e):
        self.clicked = e


class LeaserButton(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.container = parent
        self.layout = QVBoxLayout()
        self.setStyleSheet('QWidget {\nbackground: transparent;\n'
                           'border: 1px solid white;\n'
                           'border-radius: 10px;\n'
                           'color: white;\n}\n'
                           'QWidget:hover {\n'
                           'background: rgba(100, 100, 100, 0.3)\n}\n'
                           'QWidget:clicked {\n'
                           'background: rgba(50, 50, 50, 0.3)\n}\n')

        self.label = QLabel(self)
        self.label.setText('lease')
        self.label.setFont(QtGui.QFont('Arial', 36))
        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.adjustSize()

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setMouseTracking(True)
        self.clicked = self.container.startReceiverWindow

    def mousePressEvent(self, e):
        self.clicked()

    def changeClickedEvent(self, e):
        self.clicked = e

class RenterLeiserWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon(
            '../../assets/img/rendt_new_logo_square.png'))
        self.setWindowTitle('rendt')

        self.resize(440, 283)
        self.setStyleSheet('background: rgb(120, 120, 120);\n'
                           'color: white;\n')

        self.layout = QtWidgets.QHBoxLayout()
        self.senderButton = RenterButton(self)
        self.receiverButton = LeaserButton(self)

        self.senderWindow = SenderWindow(self)
        self.receiverWindow = ReceiverWindow(self)

        self.senderWindow.hide()
        self.receiverWindow.hide()

        self.layout.addWidget(self.senderButton)
        self.layout.addWidget(self.receiverButton)
        self.layout.addWidget(self.senderWindow)
        self.layout.addWidget(self.receiverWindow)
        self.setLayout(self.layout)

    def startSenderWindow(self):
        self.senderButton.hide()
        self.receiverButton.hide()
        self.senderWindow.startWindow()
        self.senderWindow.show()
    
    def startReceiverWindow(self):
        self.senderButton.hide()
        self.receiverButton.hide()
        self.receiverWindow.startWindow()
        self.receiverWindow.show()
    
    def showSenderWindow(self):
        self.senderButton.hide()
        self.receiverButton.hide()
        self.senderWindow.showWindow()
        self.senderWindow.show()
    
    def showReceiverWindow(self):
        self.senderButton.hide()
        self.receiverButton.hide()
        self.receiverWindow.showWindow()
        self.receiverWindow.show()

    def resetUi(self):
        self.setWindowTitle('rendt')
        self.senderButton.show()
        self.receiverButton.show()
        self.senderWindow.hide()
        self.receiverWindow.hide()

        if (self.senderWindow.started):
            self.senderWindow.hideWindow()
            self.senderButton.changeClickedEvent(self.showSenderWindow)
        
        if (self.receiverWindow.started):
            self.receiverWindow.hideWindow()
            self.receiverButton.changeClickedEvent(self.showReceiverWindow)

if __name__ == "__main__":
    filelist = []
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)

    window = RenterLeiserWindow()
    window.show()

    sys.exit(app.exec_())