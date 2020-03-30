import sys
import os
import psutil
import platform
from fontTools.ttLib import TTFont
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget

from sender import Sender
from receiver import Receiver


class TaskFinishedWindow(QWidget):
    def __init__(self, parent):
        super(TaskFinishedWindow, self).__init__(parent)
        layout = QVBoxLayout()

        self.backBtn = QPushButton(self)
        self.backBtn.setText('<')
        self.backBtn.setStyleSheet("QPushButton {\n"
                                   "    background: transparent;\n"
                                   "    border: 1px solid rgb(227, 227, 227);\n"
                                   "    color: white;\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton:hover {\n"
                                   "    background: rgba(200, 200, 200, 0.3);\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton:pressed {\n"
                                   "    background: rgba(150, 150, 150, 0.3);\n"
                                   "}\n"
                                   "\n")
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.setFixedHeight(50)
        self.backBtn.setFixedWidth(50)
        self.backBtn.clicked.connect(parent.goBack)

        label = QLabel(self)
        label.setText('\nTask finished successfully')
        label.setStyleSheet('background: transparent')
        label.setAlignment(QtCore.Qt.AlignHCenter)

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
        self.setStyleSheet('background: transparent;\n'
                           'border: 1px solid white;\n'
                           'color: white;\n')
        self.form = QtWidgets.QFormLayout()
        self.groupBox = QtWidgets.QGroupBox('')
        self.setWidgetResizable(True)
        self.updateJobs()

    def updateJobs(self):
        self.all_jobs = []
        jobs = self.container.receiveJobs()
        self.form = QtWidgets.QFormLayout()

        for job in jobs:
            self.addJob(job)

    def addJob(self, e):
        self.all_jobs.append(e)
        jobId = QLabel(str(e))
        jobId.setFont(QtGui.QFont('Arial', 14))
        jobId.adjustSize()
        jobId.setStyleSheet('border: 1px solid transparent;')
        jobId.setFixedWidth(self.width() - 150)

        jobExecBtn = QPushButton(self)
        jobExecBtn.jobId = e
        jobExecBtn.setText('Run')
        jobExecBtn.setFixedWidth(100)
        jobExecBtn.setFixedHeight(50)
        jobExecBtn.setFont(QtGui.QFont('Arial', 14))
        jobExecBtn.setStyleSheet('QPushButton {\n'
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

        self.setStyleSheet('background: transparent')
        self.backBtn = QPushButton(self)
        self.backBtn.setText('<')
        self.backBtn.setStyleSheet('background: transparent;\n'
                                   'color: white;\n'
                                   'border: 1px solid white;\n')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.setFixedHeight(50)
        self.backBtn.setFixedWidth(50)
        self.backBtn.clicked.connect(parent.goBack)
        self.backBtn.setStyleSheet("QPushButton {\n"
                                   "    background: transparent;\n"
                                   "    border: 1px solid rgb(227, 227, 227);\n"
                                   "    color: white;\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton:hover {\n"
                                   "    background: rgba(200, 200, 200, 0.3);\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton:pressed {\n"
                                   "    background: rgba(150, 150, 150, 0.3);\n"
                                   "}\n"
                                   "\n")

        self.refreshBtn = QPushButton(self)
        self.refreshBtn.setText('Refresh')
        self.refreshBtn.setStyleSheet("QPushButton {\n"
                                      "    background: transparent;\n"
                                      "    border: 1px solid rgb(227, 227, 227);\n"
                                      "    color: white;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover {\n"
                                      "    background: rgba(200, 200, 200, 0.3);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:pressed {\n"
                                      "    background: rgba(150, 150, 150, 0.3);\n"
                                      "}\n"
                                      "\n")
        self.refreshBtn.setFont(QtGui.QFont('Arial', 12))
        self.refreshBtn.setFixedHeight(50)
        self.refreshBtn.setFixedWidth(100)

        self.label = QLabel('Available Jobs: ')
        self.label.setFont(QtGui.QFont('Arial', 20, 1000))
        self.label.adjustSize()
        self.label.setFixedHeight(30)

        self.jobsFrame = JobsFrame(parent)
        self.refreshBtn.clicked.connect(self.jobsFrame.updateJobs)

        self.layout = QVBoxLayout()

        topButtons = QtWidgets.QHBoxLayout()
        topButtons.addWidget(self.backBtn)
        topButtons.addWidget(self.refreshBtn)
        topButtons.setContentsMargins(0, 0, 0, 0)
        topButtons.setAlignment(QtCore.Qt.AlignTop)
        topButtonsCombo = QWidget(self)
        topButtonsCombo.setLayout(topButtons)
        topButtonsCombo.setFixedHeight(60)

        self.layout.addWidget(topButtonsCombo)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.jobsFrame)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.setLayout(self.layout)
        self.layout.setContentsMargins(60, 0, 60, 80)


class HardwareInfoWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.container = parent
        self.setStyleSheet('background: transparent')
        self.label = QLabel('Hardware Information')
        self.label.setFont(QtGui.QFont('Century Gothic', 40, 1000))

        self.label.adjustSize()
        self.label.setAlignment(QtCore.Qt.AlignVCenter)

        self.physCores = QLabel(
            'Physical Cores: \t\t' + str(psutil.cpu_count(logical=False)))
        self.totalCores = QLabel(
            'Total Cores: \t\t' + str(psutil.cpu_count(logical=True)) + '\n')

        self.maxFreq = QLabel(
            f'Max Frequency: \t{psutil.cpu_freq().max: .2f} MHz')
        self.minFreq = QLabel(
            f'Min Frequency: \t{psutil.cpu_freq().min: .2f} MHz')
        self.curFreq = QLabel(
            f'Current Frequency: \t{psutil.cpu_freq().current: .2f} MHz\n')

        self.totalMem = QLabel(
            f'Total: \t\t\t{self.get_size(psutil.virtual_memory().total)}')
        self.avalMem = QLabel(
            f'Available: \t\t{self.get_size(psutil.virtual_memory().available)}')
        self.usedMem = QLabel(
            f'Used: \t\t\t{self.get_size(psutil.virtual_memory().used)}')
        self.percentMem = QLabel(
            f'Percentage: \t\t{self.get_size(psutil.virtual_memory().percent)}%\n')

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
        self.startBtn.setStyleSheet("QPushButton {\n"
                                    "    background: transparent;\n"
                                    "    border: 1px solid rgb(227, 227, 227);\n"
                                    "    color: white;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover {\n"
                                    "    background: rgba(200, 200, 200, 0.3);\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:pressed {\n"
                                    "    background: rgba(150, 150, 150, 0.3);\n"
                                    "}\n"
                                    "\n")
        self.startBtn.setFixedWidth(100)
        self.startBtn.setFixedHeight(50)
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
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)
    # * Reference: https://www.thepythoncode.com/article/get-hardware-system-information-python

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
        self.receiver = Receiver()

    def startWindow(self):
        self.started = True
        self.container.setWindowTitle('Rendt Receiver Demo')
        self.setWindowIcon(QtGui.QIcon(
            '../../assets/img/rendt_new_logo_square.png'))
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)
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
        # self.backBtn.setGeometry(QtCore.QRect(0, 0, 20, 20))
        self.backBtn.setText('<')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.clicked.connect(self.goBack)
        self.backBtn.setFixedWidth(50)
        self.backBtn.setFixedHeight(50)
        self.backBtn.hide()

        # Setting up Waiting Screen
        self.waitingWindow = WaitingWindow(self)
        self.waitingWindow.hide()

        # Setting up Received Window
        # self.receivedWindow = ReceivedWindow()
        # self.receivedWindow.hide()

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
        # self.layout.addWidget(self.receivedWindow)
        self.layout.addWidget(self.taskFinishedWindow)
        self.layout.addWidget(self.hardwareInfoWindow)
        self.layout.addWidget(self.availableJobs)

        self.setLayout(self.layout)
        self.selectDefaultFont('Century Gothic')

    def execJob(self):
        self.availableJobs.hide()
        self.waitingWindow.show()

        # Getting sent job Id from Push Button
        job_id = self.sender().jobId

        # Getting permission for execution
        db_token, size = self.receiver.get_permission_to_execute_task(job_id)

        # Downloading file to be executed
        self.receiver.download_file_from_db('sender_job.py', db_token, size)

        # Executing downloaded file
        self.receiver.execute_job('sender_job.py', f'sender_output.txt')

        # Getting permission to upload output from execution
        out_db_token = self.receiver.get_permission_to_upload_output(
            job_id, 'sender_output.txt')

        # Uploading execution output
        self.receiver.upload_output_to_db(
            'sender_output.txt', job_id, out_db_token)

        self.waitingWindow.hide()
        self.taskFinishedWindow.show()

    def receiveJobs(self):
        return self.receiver.get_available_jobs()
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

    def selectDefaultFont(self, f):
        self.container.selectDefaultFont(f)


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
        self.setFixedHeight(250)
        self.container = parent
        self.groupBox = QtWidgets.QGroupBox('')
        self.files = []

        self.layout = QVBoxLayout()

        self.uploadLabel = QLabel(self)
        self.uploadLabel.setStyleSheet(
            'color: white;\nbackground: transparent;')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)

        self.uploadLabel.setFont(font)
        self.uploadLabel.setObjectName("uploadLabel")
        self.uploadLabel.setText('Drag & Drop files here')
        self.uploadLabel.setStyleSheet('border: 1px solid transparent')
        self.uploadLabel.adjustSize()

        self.layout.addWidget(self.uploadLabel)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
            print('Accepted')
        else:
            e.ignore()
            print('Ignored')
        self.setStyleSheet("QScrollArea {\n background: rgba(30, 136, 229, 0.3);\n"
                           "border: 1px solid rgb(25, 118, 210);\n"
                           "color: white;\n}")

    def dragLeaveEvent(self, e):
        self.setStyleSheet("background: transparent;\n"
                           "border: 1px solid white;\n"
                           "color: white")

    def dropEvent(self, e):
        self.setStyleSheet("QScrollArea{\n"
                           "    background: transparent;"
                           "    color: white;\n"
                           "}\n"
                           "QLabel{\n"
                           "    color: white;\n"
                           "}\n"
                           "QPushButton {\n"
                           "    background: transparent;\n"
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
                           "\n"
                           "")
        if (self.form.rowCount() == 0):
            self.switchLabel(False)

        for url in e.mimeData().urls():
            if platform.system() == 'Windows':
                f, file_src = str(url.toString()).split('///')
            else:
                f, file_src = str(url.toString()).split('//')
            file_dir, file_name = os.path.split(file_src)

            print(file_src)
            label = QLabel(file_name)
            btn = FileButton('Remove')

            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(14)

            label.setFont(font)
            label.setAlignment(QtCore.Qt.AlignLeft)
            label.setFixedWidth(self.width() - 160)
            btn.setFont(font)
            btn.setFixedWidth(100)
            btn.setFixedHeight(40)

            btn.setFileSource(str(file_src))
            btn.clicked.connect(self.clickedRemove)

            self.form.addRow(label, btn)

        self.groupBox.setLayout(self.form)
        self.setWidget(self.groupBox)

    def clickedRemove(self):
        self.form.removeRow(self.sender())

        if (self.form.rowCount() == 0):
            self.switchLabel(True)

    def uploadFiles(self):
        for i in range(self.form.rowCount() * 2):
            if (i % 2):
                self.files.append(self.form.itemAt(i).widget().getFileSource())

        for f in self.files:
            print(f'File: {f}')
            filelist.append(f)
            self.form.removeRow(0)

        self.switchLabel(True)

    def switchLabel(self, flag):
        if (flag):
            self.uploadLabel.show()
        else:
            self.uploadLabel.hide()


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
        self.started = False

    def startWindow(self, job_id):
        self.started = True
        self.layout = QVBoxLayout()

        self.backBtn = QPushButton(self)
        self.backBtn.setText('<')
        self.backBtn.setStyleSheet("QPushButton:hover {\n"
                                   "    background: rgba(200, 200, 200, 0.3);\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton:pressed {\n"
                                   "    background: rgba(150, 150, 150, 0.3);\n"
                                   "}\n"
                                   "QPushButton {\n"
                                   "   background: transparent;\n"
                                   "   border: 1px solid white;\n"
                                   "   color: white;\n}\n")
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.setFixedHeight(50)
        self.backBtn.setFixedWidth(50)
        self.backBtn.clicked.connect(self.container.goBack)

        self.label = QLabel(self)
        self.label.setText('Files uploaded successfully')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)

        self.label.setFont(font)
        self.label.adjustSize()
        self.label.setFixedHeight(70)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # self.label.setGeometry(QtCore.QRect(135, 100, 144, 30))

        self.downloadId = QLabel(self)
        self.downloadId.setText('Job ID: ' + str(job_id))
        self.downloadId.setFont(QtGui.QFont('Arial', 20))
        # self.downloadId.setGeometry(QtCore.QRect(150, 130, 144, 22))
        self.downloadId.adjustSize()
        self.downloadId.setFixedHeight(70)
        self.downloadId.setFixedWidth(220)
        # self.downloadId.setAlignment(QtCore.Qt.AlignCenter)

        self.copyBtn = QPushButton(self)
        self.copyBtn.setStyleSheet("QPushButton:hover {\n"
                                   "    background: rgba(200, 200, 200, 0.3);\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton:pressed {\n"
                                   "    background: rgba(150, 150, 150, 0.3);\n"
                                   "}\n"
                                   "QPushButton {\n"
                                   "   background: transparent;\n"
                                   "   border: 1px solid white;\n"
                                   "   color: white;\n}\n")
        self.copyBtn.setText('Copy')
        self.copyBtn.setFont(QtGui.QFont('Arial', 12))
        self.copyBtn.setFixedWidth(80)
        self.copyBtn.setFixedHeight(50)
        self.copyBtn.clicked.connect(lambda: self.copyToClipBoard(str(job_id)))

        self.buttonsCombo = QWidget(self)
        buttons = QtWidgets.QHBoxLayout(self)
        buttons.addWidget(self.downloadId)
        buttons.addWidget(self.copyBtn)
        buttons.setAlignment(QtCore.Qt.AlignCenter)
        self.buttonsCombo.setLayout(buttons)

        self.layout.addWidget(self.backBtn)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.buttonsCombo)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.selectDefaultFont('Century Gothic')

    def copyToClipBoard(self, e):
        cb = QtWidgets.QApplication.clipboard()
        cb.setText(e)

    def selectDefaultFont(self, f):
        self.label.setFont(QtGui.QFont(f, 28))
        self.downloadId.setFont(QtGui.QFont(f, 20))
        self.copyBtn.setFont(QtGui.QFont(f, 12))


class DownloadWindow(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.container = parent
        self.layout = QVBoxLayout()
        self.setStyleSheet('color: white')

        self.label = QLabel(self)
        self.label.setText('Download executed files with Job ID')
        self.label.setFont(QtGui.QFont('Arial', 40))
        self.label.setFixedHeight(60)
        self.label.adjustSize()
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.jobIdLabel = QLabel(self)
        self.jobIdLabel.setText('Job ID: ')
        self.jobIdLabel.setFont(QtGui.QFont('Century Gothic', 14))
        self.jobIdLabel.adjustSize()
        self.jobIdLabel.setFixedWidth(100)
        self.jobIdLabel.setFixedHeight(50)
        self.jobIdLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.jobId = QtWidgets.QLineEdit(self)
        self.jobId.setFont(QtGui.QFont('Arial', 14))
        self.jobId.setStyleSheet('background: transparent;\n'
                                 'border: 1px solid white;\n'
                                 'color: white;\n')
        self.jobId.setFixedHeight(50)
        self.jobId.setFixedWidth(200)

        self.sendBtn = QPushButton(self)
        self.sendBtn.setText('Send')
        self.sendBtn.setFont(QtGui.QFont('Arial', 12))
        self.sendBtn.setStyleSheet("QPushButton:hover {\n"
                                   "    background: rgba(200, 200, 200, 0.3);\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton:pressed {\n"
                                   "    background: rgba(150, 150, 150, 0.3);\n"
                                   "}\n"
                                   "QPushButton {\n"
                                   "   background: transparent;\n"
                                   "   border: 1px solid rgb(227, 227, 227);\n"
                                   "   color: white;\n}\n")
        self.sendBtn.setFixedHeight(50)
        self.sendBtn.setFixedWidth(70)
        self.sendBtn.clicked.connect(self.downloadFile)

        midWidgets = QtWidgets.QHBoxLayout(self)
        midWidgets.addWidget(self.jobIdLabel)
        midWidgets.addWidget(self.jobId)
        midWidgets.addWidget(self.sendBtn)
        midWidgets.setAlignment(QtCore.Qt.AlignCenter)
        midWidgetsCombo = QWidget(self)
        midWidgetsCombo.setLayout(midWidgets)

        # Adding back button
        self.backBtn = QPushButton(self)
        self.backBtn.setText('<')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.clicked.connect(self.container.goBack)
        self.backBtn.setFixedHeight(50)
        self.backBtn.setFixedWidth(50)

        # Adding download files button
        self.uploadBtn = QPushButton(self)
        self.uploadBtn.setText('Upload')
        self.uploadBtn.setFont(QtGui.QFont('Arial', 12))
        self.uploadBtn.clicked.connect(self.startUploadWindow)
        self.uploadBtn.setFixedWidth(100)
        self.uploadBtn.setFixedHeight(50)

        # Adding Download Finished Successfully Label
        self.downloadFinishedLabel = QLabel(self)
        self.downloadFinishedLabel.setText('\nDownload Finished Successfully')
        self.downloadFinishedLabel.setGeometry(QtCore.QRect(50, 60, 20, 22))
        self.downloadFinishedLabel.setFont(QtGui.QFont('Arial', 30, 1000))
        self.downloadFinishedLabel.adjustSize()
        self.downloadFinishedLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.downloadFinishedLabel.hide()

        topButtons = QtWidgets.QHBoxLayout(self)
        topButtons.addWidget(self.backBtn)
        topButtons.addWidget(self.uploadBtn)
        topButtonsCombo = QWidget(self)
        topButtonsCombo.setLayout(topButtons)
        # topButtonsCombo.setFixedHeight(55)
        topButtons.setAlignment(QtCore.Qt.AlignTop)
        topButtons.setContentsMargins(0, 0, 0, 0)
        topButtonsCombo.setContentsMargins(0, 0, 0, 0)
        # topButtonsCombo.setStyleSheet('background: black')

        self.layout.addWidget(topButtonsCombo)
        self.layout.addWidget(self.label)
        self.layout.addWidget(midWidgetsCombo)
        self.layout.addWidget(self.downloadFinishedLabel)

        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

    def startUploadWindow(self):
        self.destroy()
        self.container.resetUi()

    def downloadFile(self):
        job_id = int(str(self.jobId.text()))
        perm = self.container.sender.get_permission_to_download_output(job_id)

        if perm:
            out_db_token, file_size = perm
            self.container.sender.download_output_from_db(
                'received_output.txt', out_db_token, file_size)

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
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)
        self.setStyleSheet("QPushButton {\n"
                           "    background: transparent;\n"
                           "    border: 1px solid rgb(227, 227, 227);\n"
                           "    color: white;\n"
                           "}\n"
                           "\n"
                           "QPushButton:hover {\n"
                           "    background: rgb(200, 200, 200);\n"
                           "}\n"
                           "\n"
                           "QPushButton:pressed {\n"
                           "    background: rgba(150, 150, 150, 1);\n"
                           "}\n"
                           "\n"
                           "QWidget {\n"
                           "    background: transparent;\n"
                           "}\n"
                           "\n"
                           "")

        # Setting up the layout
        self.layout = QVBoxLayout()

        # Adding back button
        self.backBtn = QPushButton(self)
        # self.backBtn.setGeometry(QtCore.QRect(0, 0, 20, 20))
        self.backBtn.setText('<')
        self.backBtn.setFont(QtGui.QFont('Arial', 12))
        self.backBtn.clicked.connect(self.goBack)
        self.backBtn.setFixedHeight(50)
        self.backBtn.setFixedWidth(50)
        self.backBtn.setStyleSheet("QPushButton {\n"
                                   "    background: transparent;\n"
                                   "    border: 1px solid rgb(227, 227, 227);\n"
                                   "    color: white;\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton:hover {\n"
                                   "    background: rgba(200, 200, 200, 0.3);\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton:pressed {\n"
                                   "    background: rgba(150, 150, 150, 0.3);\n"
                                   "}\n"
                                   "\n")

        # Adding download files button
        self.downloadBtn = QPushButton(self)
        self.downloadBtn.setText('Download')
        self.downloadBtn.setFont(QtGui.QFont('Arial', 12))
        # self.downloadBtn.setGeometry(22, 0, 70, 20)
        self.downloadBtn.clicked.connect(self.startDownloadWindow)
        self.downloadBtn.setFixedHeight(50)
        self.downloadBtn.setFixedWidth(150)
        self.downloadBtn.setStyleSheet("QPushButton {\n"
                                       "    background: transparent;\n"
                                       "    border: 1px solid rgb(227, 227, 227);\n"
                                       "    color: white;\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:hover {\n"
                                       "    background: rgba(200, 200, 200, 0.3);\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:pressed {\n"
                                       "    background: rgba(150, 150, 150, 0.3);\n"
                                       "}\n"
                                       "\n")

        # Setting up the label and configuring it
        self.label = QLabel(self)
        self.label.setText('Drag & Drop')
        # self.label.setGeometry(QtCore.QRect(30, 20, 210, 43))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")
        self.label.setFixedHeight(100)
        self.label.setAlignment(QtCore.Qt.AlignVCenter)

        # Adding Scroll Frame where the Dragging and Dropping will happen
        self.scroll = ScrollFrame(self)
        # self.scroll.setGeometry(QtCore.QRect(30, 70, 361, 121))
        self.scroll.setStyleSheet("background: transparent;\n"
                                  "border: 1px solid white;\n")
        self.scroll.setWidgetResizable(True)

        # Adding Download Window
        self.downloadWindow = DownloadWindow(self)
        self.downloadWindow.hide()

        # Setting up the label inside the frame and configuring it
        # self.uploadLabel = QLabel(self.scroll)
        # self.uploadLabel.setStyleSheet('color: white')
        # # self.uploadLabel.setGeometry(QtCore.QRect(100, 50, 144, 17))

        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setPointSize(14)

        # self.uploadLabel.setFont(font)
        # self.uploadLabel.setObjectName("uploadLabel")
        # self.uploadLabel.setText('Drag & Drop files here')
        # self.uploadLabel.adjustSize()

        # Adding the 'Upload' button and configuring it
        self.uploadBtn = QPushButton(self)
        # self.uploadBtn.setGeometry(QtCore.QRect(320, 200, 71, 31))
        self.uploadBtn.setText('Upload')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.uploadBtn.setFont(font)
        self.uploadBtn.setObjectName("uploadBtn")
        self.uploadBtn.clicked.connect(self.startLoadingWindow)
        self.uploadBtn.setFixedHeight(50)
        self.uploadBtn.setFixedWidth(120)
        self.uploadBtn.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.uploadBtn.setStyleSheet("QPushButton {\n"
                                     "    background: transparent;\n"
                                     "    border: 1px solid rgb(227, 227, 227);\n"
                                     "    color: white;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover {\n"
                                     "    background: rgba(200, 200, 200, 0.3);\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:pressed {\n"
                                     "    background: rgba(150, 150, 150, 0.3);\n"
                                     "}\n"
                                     "\n")

        # Setting up Loading Screen
        self.loadingWindow = LoadingWindow(self)
        self.loadingWindow.hide()

        # Adding Output Details Label
        self.outputDetailsLabel = QLabel(self)
        self.outputDetailsLabel.setText('Received Output')
        # self.outputDetailsLabel.setGeometry(QtCore.QRect(30, 20, 210, 43))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.outputDetailsLabel.setFont(font)
        self.outputDetailsLabel.setStyleSheet("color: white;")
        self.outputDetailsLabel.adjustSize()
        self.outputDetailsLabel.hide()

        # Adding Ouput Frame
        self.outputFrame = OutputFrame(self)
        # self.outputFrame.setGeometry(QtCore.QRect(30, 70, 361, 121))
        self.outputFrame.setStyleSheet("background: rgb(150, 150, 150);\n"
                                       "border: 1px solid rgb(150, 150, 150);\n")
        self.outputFrame.setWidgetResizable(True)
        self.outputFrame.hide()

        # Adding Upload Finished Window
        self.uploadFinishedWindow = UploadFinishedWindow(self)
        self.uploadFinishedWindow.hide()

        # Adding everything into the layout
        topButtonsCombo = QWidget()
        # topButtonsCombo.setFixedHeight(55)

        topButtons = QtWidgets.QHBoxLayout(self)

        topButtons.addWidget(self.backBtn)
        topButtons.addWidget(self.downloadBtn)
        topButtons.setContentsMargins(0, 0, 0, 0)

        topButtons.setAlignment(QtCore.Qt.AlignTop)
        topButtonsCombo.setLayout(topButtons)
        topButtonsCombo.setStyleSheet('background: transparent')
        topButtonsCombo.setFixedHeight(55)
        self.topButtons = topButtonsCombo

        self.layout.addWidget(self.topButtons)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.uploadBtn)
        # self.layout.addWidget(self.uploadLabel)
        self.layout.addWidget(self.loadingWindow)
        self.layout.addWidget(self.outputDetailsLabel)
        self.layout.addWidget(self.outputFrame)
        self.layout.addWidget(self.uploadFinishedWindow)
        self.layout.addWidget(self.downloadWindow)

        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(60, 0, 60, 80)
        # self.layout.setSpacing(10)

        self.setLayout(self.layout)

        self.sender = Sender()
        self.selectDefaultFont('Century Gothic')

    def startDownloadWindow(self):
        self.label.hide()
        self.scroll.hide()
        # self.uploadLabel.hide()
        self.uploadBtn.hide()
        self.backBtn.hide()
        self.downloadBtn.hide()
        self.topButtons.hide()
        self.downloadWindow.show()

    def startLoadingWindow(self):
        self.label.hide()
        self.scroll.hide()
        # self.uploadLabel.hide()
        self.uploadBtn.hide()
        self.loadingWindow.show()

        self.scroll.uploadFiles()
        job_id, db_token = self.sender.get_permission_to_submit_task(
            filelist[0])
        self.sender.upload_file_to_db(filelist[0], job_id, db_token)

        self.loadingWindow.hide()
        self.downloadWindow.hide()
        self.hideWindow()
        self.uploadFinishedWindow.startWindow(job_id)
        self.uploadFinishedWindow.show()

    # def startUploadFinishedWindow(self):
    #     self.scroll.uploadFiles()
    #     self.loadingWindow().hide()
    #     self.uploadFinishedWindow()

    def goBack(self):
        self.container.resetUi()

    def resetUi(self):
        self.downloadWindow.hide()
        self.label.show()
        self.scroll.show()
        self.scroll.uploadLabel.show()
        self.uploadBtn.show()
        self.backBtn.show()
        self.downloadBtn.show()
        self.topButtons.show()

    def hideWindow(self):
        self.label.hide()
        self.scroll.hide()
        # self.uploadLabel.hide()
        self.topButtons.hide()
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
        # self.uploadLabel.show()
        self.uploadBtn.show()
        self.backBtn.show()
        self.downloadBtn.show()
        self.topButtons.show()

    def selectDefaultFont(self, f):
        self.container.selectDefaultFont(f)


class RenterButton(QScrollArea):
    def __init__(self, parent):
        super().__init__()

        self.container = parent
        self.layout = QVBoxLayout()

        icon = QtGui.QPixmap('../../assets/img/cloud_w_no_border.png')

        self.icon = QLabel(self)
        self.icon.setPixmap(icon.scaled(80, 80, QtCore.Qt.KeepAspectRatio))
        self.icon.adjustSize()
        self.icon.setAlignment(QtCore.Qt.AlignCenter)

        self.setStyleSheet('QScrollArea {\nbackground: transparent;\n'
                           'border: 1px solid white;\n'
                           'border-radius: 5px;\n'
                           'color: white;\n}\n'
                           'QScrollArea:hover {\n'
                           'background: rgba(100, 100, 100, 0.3)\n}\n'
                           'QScrollArea:clicked {\n'
                           'background: rgba(50, 50, 50, 0.3)\n}\n'
                           'QWidget {\n'
                           '    background: transparent;\n}\n')

        self.label = QLabel(self)
        self.label.setText('rent')
        self.label.setFont(QtGui.QFont('Century Gothic', 50, 1000))
        # self.label.setStyleSheet('font-family: Century Gothic;\nfont-size: 80px;\nfont-weight: bold;')
        # self.label.setSizePolicy(
        #     QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.adjustSize()
        self.label.setMargin(0)

        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setMouseTracking(True)
        self.clicked = self.container.startSenderWindow

    def mousePressEvent(self, e):
        self.container.renterMode()
        self.clicked()

    def changeClickedEvent(self, e):
        self.clicked = e


class LeaserButton(QScrollArea):
    def __init__(self, parent):
        super().__init__()

        self.container = parent
        self.layout = QVBoxLayout()
        self.setStyleSheet('QScrollArea {\nbackground: transparent;\n'
                           'border: 1px solid white;\n'
                           'border-radius: 5px;\n'
                           'color: white;\n}\n'
                           'QScrollArea:hover {\n'
                           'background: rgba(100, 100, 100, 0.3)\n}\n'
                           'QScrollArea:clicked {\n'
                           'background: rgba(50, 50, 50, 0.3)\n}\n'
                           'QWidget {\n'
                           '    background: transparent;\n}\n')

        icon = QtGui.QPixmap('../../assets/img/cpu_w_no_border.png')

        self.icon = QLabel(self)
        self.icon.setPixmap(icon.scaled(80, 80, QtCore.Qt.KeepAspectRatio))
        self.icon.adjustSize()
        self.icon.setAlignment(QtCore.Qt.AlignCenter)

        self.label = QLabel(self)
        self.label.setText('lease')
        self.label.setFont(QtGui.QFont('Century Gothic', 50, 1000))
        # self.label.setSizePolicy(
        #     QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.adjustSize()

        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setMouseTracking(True)
        self.clicked = self.container.startReceiverWindow

    def mousePressEvent(self, e):
        self.container.leaserMode()
        self.clicked()

    def changeClickedEvent(self, e):
        self.clicked = e


class RenterLeaserWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon(
            '../../assets/img/rendt_new_logo_square.png'))
        self.setWindowTitle('rendt')

        self.resize(1000, 600)
        self.setStyleSheet('background: rgb(0, 23, 37);\n'
                           'color: white;\n')

        self.layout = QtWidgets.QHBoxLayout()
        self.senderButton = RenterButton(self)
        self.receiverButton = LeaserButton(self)

        self.senderWindow = SenderWindow(self)
        self.receiverWindow = ReceiverWindow(self)

        self.senderWindow.hide()
        self.receiverWindow.hide()
        self.seperator = QWidget()
        self.seperator.setFixedWidth(15)

        self.rendt = QLabel(self)
        self.rendt.setText('rendt')
        # self.rendt.setStyleSheet('background: black')
        self.rendt.setFixedWidth(110)
        self.rendt.setFixedHeight(60)
        self.rendt.setFont(QtGui.QFont('Century Gothic', 20, 1000))
        self.rendt.adjustSize()
        self.rendt.setAlignment(QtCore.Qt.AlignCenter)

        self.renter = QLabel(self)
        self.renter.setText('renter')
        self.renter.setFixedWidth(260)
        self.renter.setFixedHeight(100)
        self.renter.setStyleSheet(
            'background: transparent;\ncolor: rgb(198, 0, 255)')
        self.renter.setFont(QtGui.QFont('Century Gothic', 20, 1000))
        self.renter.adjustSize()
        self.renter.setAlignment(QtCore.Qt.AlignCenter)
        self.renter.hide()

        self.leaser = QLabel(self)
        self.leaser.setText('leaser')
        self.leaser.setFixedWidth(260)
        self.leaser.setFixedHeight(100)
        self.leaser.setStyleSheet(
            'background: transparent;\ncolor: rgb(0, 255, 72)')
        self.leaser.setFont(QtGui.QFont('Century Gothic', 20, 1000))
        self.leaser.adjustSize()
        self.leaser.setAlignment(QtCore.Qt.AlignCenter)
        self.leaser.hide()

        # self.layout.addWidget(self.rendt)
        self.layout.addWidget(self.senderButton)
        self.layout.addWidget(self.seperator)
        self.layout.addWidget(self.receiverButton)
        self.layout.addWidget(self.senderWindow)
        self.layout.addWidget(self.receiverWindow)
        self.layout.setContentsMargins(30, 60, 30, 30)
        # self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(self.layout)
        self.selectDefaultFont('Century Gothic')

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
        self.renter.hide()
        self.leaser.hide()
        self.layout.setContentsMargins(30, 60, 30, 30)
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

    def renterMode(self):
        self.renter.show()
        self.layout.setContentsMargins(30, 100, 30, 30)

    def leaserMode(self):
        self.leaser.show()
        self.layout.setContentsMargins(30, 100, 30, 30)

    def selectDefaultFont(self, f):
        self.rendt.setFont(QtGui.QFont(f, 20, 1000))
        self.renter.setFont(QtGui.QFont(f, 20, 1000))
        self.leaser.setFont(QtGui.QFont(f, 20, 1000))
        self.receiverButton.label.setFont(QtGui.QFont(f, 50, 1000))
        self.senderButton.label.setFont(QtGui.QFont(f, 50, 1000))

        if (self.receiverWindow.started == True):
            self.receiverWindow.taskFinishedWindow.label.setFont(
                QtGui.QFont(f, 28, 1000))

            self.receiverWindow.availableJobs.label.setFont(
                QtGui.QFont(f, 20, 1000))

            self.receiverWindow.hardwareInfoWindow.label.setFont(
                QtGui.QFont(f, 40, 1000))
            self.receiverWindow.hardwareInfoWindow.physCores.setFont(
                QtGui.QFont(f, 14))
            self.receiverWindow.hardwareInfoWindow.physCores.adjustSize()
            self.receiverWindow.hardwareInfoWindow.totalCores.setFont(
                QtGui.QFont(f, 14))
            self.receiverWindow.hardwareInfoWindow.totalCores.adjustSize()
            self.receiverWindow.hardwareInfoWindow.maxFreq.setFont(
                QtGui.QFont(f, 14))
            self.receiverWindow.hardwareInfoWindow.maxFreq.adjustSize()
            self.receiverWindow.hardwareInfoWindow.minFreq.setFont(
                QtGui.QFont(f, 14))
            self.receiverWindow.hardwareInfoWindow.minFreq.adjustSize()
            self.receiverWindow.hardwareInfoWindow.curFreq.setFont(
                QtGui.QFont(f, 14))
            self.receiverWindow.hardwareInfoWindow.curFreq.adjustSize()
            self.receiverWindow.hardwareInfoWindow.totalMem.setFont(
                QtGui.QFont(f, 14))
            self.receiverWindow.hardwareInfoWindow.totalMem.adjustSize()
            self.receiverWindow.hardwareInfoWindow.avalMem.setFont(
                QtGui.QFont(f, 14))
            self.receiverWindow.hardwareInfoWindow.avalMem.adjustSize()
            self.receiverWindow.hardwareInfoWindow.usedMem.setFont(
                QtGui.QFont(f, 14))
            self.receiverWindow.hardwareInfoWindow.usedMem.adjustSize()
            self.receiverWindow.hardwareInfoWindow.percentMem.setFont(
                QtGui.QFont(f, 14))
            self.receiverWindow.hardwareInfoWindow.percentMem.adjustSize()

        if (self.senderWindow.started == True):
            self.senderWindow.label.setFont(QtGui.QFont(f, 36))
            self.senderWindow.uploadBtn.setFont(QtGui.QFont(f, 12))
            self.senderWindow.downloadBtn.setFont(QtGui.QFont(f, 12))
            self.senderWindow.outputDetailsLabel.setFont(QtGui.QFont(f, 36))

            self.senderWindow.scroll.uploadLabel.setFont(QtGui.QFont(f, 15))

            self.senderWindow.downloadWindow.label.setFont(QtGui.QFont(f, 25))
            self.senderWindow.downloadWindow.jobIdLabel.setFont(
                QtGui.QFont(f, 20))
            self.senderWindow.downloadWindow.jobId.setFont(QtGui.QFont(f, 14))
            self.senderWindow.downloadWindow.uploadBtn.setFont(
                QtGui.QFont(f, 12))
            self.senderWindow.downloadWindow.downloadFinishedLabel.setFont(
                QtGui.QFont(f, 30, 1000))



if __name__ == "__main__":
    filelist = []
    app = QtWidgets.QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont(
        '../../assets/fonts/CenturyGothic.ttf')
    QtGui.QFontDatabase.addApplicationFont(
        '../../assets/fonts/CenturyGothicBold.ttf')

    window = RenterLeaserWindow()
    window.show()

    sys.exit(app.exec_())
