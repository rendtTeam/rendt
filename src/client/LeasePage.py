from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QMainWindow

import platform
import docker
from numexpr import cpuinfo
from pprint import pprint
import threading
from datetime import datetime
import time

# NOTE:
# Class for getting information about docker installation
class DockerInfo:
    def __init__(self):
        self.exists = False
        self.info = []
        self.client = docker.from_env()

        # NOTE:
        # Trying initializing DockerClient instance
        try:
            self.client = docker.from_env()
            if (len(self.client.info())):
                self.exists = True  
        except:
            self.exists = False

    # NOTE:
    # Docker is installed and running or not
    def dockerExists(self):
        return self.exists

    # NOTE:
    # Get number of CPUs used in docker
    def getNumCPU(self):
        if (self.exists):
            return self.client.info()['NCPU']
        else:
            return -1

    # NOTE:
    # Get total memory of docker in bytes
    def getMemTotal(self):
        if (self.exists):
            return self.client.info()['MemTotal']
        else:
            return -1

    # NOTE:
    # Get total memory of docker in GigaBytes
    def getMemTotalGB(self):
        if (self.exists):
            return self.client.info()['MemTotal'] / (1 << 30)
        else:
            return -1

    # NOTE:
    # Get CPU model
    def getCPUModel(self):
        if (self.exists):
            if (platform.system() == 'Windows'):
                return cpuinfo.cpu.info[0]['ProcessorNameString']
            else:
                return cpuinfo.cpu.info[0]['model name']
        else:
            return ""

    # NOTE:
    # Get total number of logical cores of the CPU
    def getCPUTotalNum(self):
        if (self.exists):
            return len(cpuinfo.cpu.info)
        else:
            return -1

    # NOTE:
    # Get version of docker installation
    def getDockerVersion(self):
        if (self.exists):
            return self.client.info()['ServerVersion']
        else:
            return ""

    # NOTE:
    # Get full docker info
    def getFullInfoJSON(self):
        if (self.exists):
            return self.client.info()
        else:
            return ""
    
    # NOTE:
    # Get Docker Stats for CPU Usage percentage
    def getCpuUsage(self):
        if (self.exists): 
            return self.client.containers.get('rendtcont').stats(stream = False).get('cpu_stats')['cpu_usage']['total_usage'] / self.client.containers.get('rendtcont').stats(stream = False).get('cpu_stats')['system_cpu_usage'] * 100 
        else:
            return ''

    # NOTE:
    # Get Docker Stats for Memory Usage percentage
    def getMemUsage(self):
        if (self.exists):
            self.mem_stats = self.client.containers.get('rendtcont').stats(stream = False).get('memory_stats')
            return self.mem_stats['usage'] / self.mem_stats['limit'] * 100
        else:
            return ''

class DockerSpecsLabel(QWidget):
    def __init__(self, parent):
        super(DockerSpecsLabel, self).__init__()

        self.parent = parent

        self.label1 = QLabel(self)
        self.label1.setFont(QtGui.QFont('Arial', 25, 800))
        self.label1.adjustSize()
        # self.label1.setAlignment(QtCore.Qt.AlignHCenter)
        self.label1.setStyleSheet(  'background: transparent;\n'
                                    'border: 0px solid white;\n'
                                    'color: white;\n'
                                    'font-weight: bold;\n')
        
        self.label2 = QLabel(self)
        self.label2.setFont(QtGui.QFont('Arial', 25, 800))
        self.label2.adjustSize()
        # self.label2.setAlignment(QtCore.Qt.AlignHCenter)
        self.label2.setStyleSheet(  'background: transparent;\n'
                                    'border: 0px solid white;\n'
                                    'color: rgb(120, 120, 120);\n'
                                    'font-weight: bold;\n')
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)

        self.setLayout(self.layout)

    def setFirstLabel(self, e):
        self.label1.setText(e)
        self.label1.adjustSize()

    def setSecondLabel(self, e):
        self.label2.setText(e)
        self.label2.adjustSize()

class NoDockerFoundPage(QWidget):
    def __init__(self, parent):
        super(NoDockerFoundPage, self).__init__()

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

        self.shadow2 = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow2.setBlurRadius(30)
        self.shadow2.setXOffset(0)
        self.shadow2.setYOffset(0)
        self.shadow2.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.noDockerFoundLabel = QLabel(self)
        self.noDockerFoundLabel.setText('Docker is not running')
        self.noDockerFoundLabel.setFont(QtGui.QFont('Arial', 40, 400))
        self.noDockerFoundLabel.adjustSize()
        self.noDockerFoundLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.noDockerFoundLabel.setStyleSheet('background: transparent;\n'
                                              'border: 0px solid white;\n'
                                              'margin-top: 50px;\n'
                                              'font-weight: bold;\n')

        self.noDockerFoundLabel.setGraphicsEffect(self.shadow)

        self.errorReasonLabel = QLabel(self)
        self.errorReasonLabel.setText('You are seeing this error because:')
        self.errorReasonLabel.setFont(QtGui.QFont('Arial', 20, 800))
        self.errorReasonLabel.adjustSize()
        self.errorReasonLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.errorReasonLabel.setStyleSheet('background: transparent;\n'
                                            'border: 0px solid white;\n'
                                            'margin: 0px;\n'
                                            'padding: 30px 30px 0px 30px;\n')

        self.firstReasonLabel = QLabel(self)
        self.firstReasonLabel.setText('\t1. Docker daemon is not running')
        self.firstReasonLabel.setFont(QtGui.QFont('Arial', 14, 800))
        self.firstReasonLabel.adjustSize()
        self.firstReasonLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.firstReasonLabel.setStyleSheet('background: transparent;\n'
                                            'border: 0px solid white;\n'
                                            'margin: 0px;\n'
                                            'padding: 0px 30px 0px 30px;\n')

        self.firstReasonALabel = QLabel(self)
        self.firstReasonALabel.setText(
            '\t\ta. Please start your docker daemon or check docker status')
        self.firstReasonALabel.setFont(QtGui.QFont('Arial', 14, 800))
        self.firstReasonALabel.adjustSize()
        self.firstReasonALabel.setAlignment(QtCore.Qt.AlignLeft)
        self.firstReasonALabel.setStyleSheet('background: transparent;\n'
                                             'border: 0px solid white;\n'
                                             'color: rgba(200, 200, 200, 0.8);\n'
                                             'margin: 0px;\n'
                                             'padding: 0px 30px 0px 30px;\n')

        self.secondReasonLabel = QLabel(self)
        self.secondReasonLabel.setText('\t2. No docker installation is found')
        self.secondReasonLabel.setFont(QtGui.QFont('Arial', 14, 800))
        self.secondReasonLabel.adjustSize()
        self.secondReasonLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.secondReasonLabel.setStyleSheet('background: transparent;\n'
                                             'border: 0px solid white;\n'
                                             'margin: 0px;\n'
                                             'padding: 0px 30px 0px 30px;\n')

        self.secondReasonALabel = QLabel(self)
        self.secondReasonALabel.setText('\t\ta. To lease your machine you need to\n\t\t    have a running docker daemon on your computer')
        self.secondReasonALabel.setFont(QtGui.QFont('Arial', 14, 800))
        self.secondReasonALabel.adjustSize()
        self.secondReasonALabel.setAlignment(QtCore.Qt.AlignLeft)
        self.secondReasonALabel.setStyleSheet('background: transparent;\n'
                                              'border: 0px solid white;\n'
                                              'color: rgba(200, 200, 200, 0.8);\n'
                                              'padding: 0px;\n'
                                              'margin-top: 0px;\n')

        self.infoBox = QWidget(self)
        self.infoBox.setStyleSheet( 'background: rgb(71, 71, 71);\n'
                                    'color: white;\n'
                                    'border: 0px solid white;\n'
                                    'padding: 0px;\n'
                                    'margin: 30px;\n')
        
        self.infoBox.setMinimumHeight(400)
        self.infoBox.setMinimumWidth(800)

        self.infoBoxLayout = QVBoxLayout()
        self.infoBoxLayout.addWidget(self.errorReasonLabel)
        self.infoBoxLayout.addWidget(self.firstReasonLabel)
        self.infoBoxLayout.addWidget(self.firstReasonALabel)
        self.infoBoxLayout.addWidget(self.secondReasonLabel)
        self.infoBoxLayout.addWidget(self.secondReasonALabel)

        self.infoBoxLayout.setAlignment(QtCore.Qt.AlignTop)
        self.infoBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.infoBoxLayout.setSpacing(20)
        self.infoBox.setLayout(self.infoBoxLayout)
        self.infoBox.setGraphicsEffect(self.shadow2)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.noDockerFoundLabel)
        self.layout.addWidget(self.infoBox)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 50)
        self.layout.setSpacing(20)

        self.setLayout(self.layout)
    
    def darkTheme(self):
        self.setStyleSheet( 'background: rgb(57, 57, 57);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

    def lightTheme(self):
        self.setStyleSheet( 'background: rgb(204, 204, 204);\n'
                            'color: black;\n'
                            'border: 0px solid black;\n')

    def classicTheme(self):
        self.setStyleSheet( 'background: rgb(0, 23, 37);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

class DockerSpecificationsPage(QWidget):
    def __init__(self, parent):
        super(DockerSpecificationsPage, self).__init__()

        self.parent = parent
        self.dockerInfo = self.parent.dockerInfo

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

        self.shadow3 = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow3.setBlurRadius(30)
        self.shadow3.setXOffset(0)
        self.shadow3.setYOffset(0)
        self.shadow3.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.dockerSpecsLabel = QLabel(self)
        self.dockerSpecsLabel.setText('Docker specifications')
        self.dockerSpecsLabel.setFont(QtGui.QFont('Arial', 40, 400))
        self.dockerSpecsLabel.adjustSize()
        self.dockerSpecsLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.dockerSpecsLabel.setStyleSheet('background: transparent;\n'
                                            'border: 0px solid white;\n'
                                            'margin-top: 50px;\n'
                                            'font-weight: bold;\n')

        self.dockerSpecsLabel.setGraphicsEffect(self.shadow)

        img = QtGui.QPixmap('../../assets/img/docker_w.png')
        self.dockerLogo = QLabel(self)
        self.dockerLogo.setPixmap(img.scaled(
            250, 250, QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation))
        self.dockerLogo.setStyleSheet(   'background: transparent;\n'
                                        'border: 0px solid white;\n')
        
        self.cpuModel = DockerSpecsLabel(self)
        self.cpuModel.setFirstLabel('CPU: ')
        self.cpuModel.setSecondLabel(str(self.dockerInfo.getNumCPU()) + 'x')

        self.memory = DockerSpecsLabel(self)
        self.memory.setFirstLabel('RAM: ')
        self.memory.setSecondLabel('%.3fGB' % self.dockerInfo.getMemTotalGB())

        self.version = DockerSpecsLabel(self)
        self.version.setFirstLabel('Version: ')
        self.version.setSecondLabel(self.dockerInfo.getDockerVersion())

        self.specsList = QWidget(self)
        self.specsList.setStyleSheet(   'background: transparent;\n'
                                        'border: 0px solid white;\n')
        
        self.specsListLayout = QVBoxLayout()
        self.specsListLayout.addWidget(self.cpuModel)
        self.specsListLayout.addWidget(self.memory)
        self.specsListLayout.addWidget(self.version)
        self.specsListLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.specsListLayout.setContentsMargins(0, 0, 0, 0)

        self.specsList.setLayout(self.specsListLayout)

        self.infoBox = QWidget(self)
        self.infoBox.setStyleSheet( 'background: rgb(71, 71, 71);\n'
                                    'color: white;\n'
                                    'border: 0px solid white;\n'
                                    'margin: 20px;\n')

        self.infoBox.setMinimumHeight(400)
        self.infoBox.setMinimumWidth(800)
        
        self.infoBoxLayout = QHBoxLayout()
        self.infoBoxLayout.addWidget(self.dockerLogo, alignment = QtCore.Qt.AlignVCenter)
        self.infoBoxLayout.addWidget(self.specsList, alignment = QtCore.Qt.AlignVCenter)
        self.infoBoxLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.infoBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.infoBoxLayout.setSpacing(30)
        self.infoBox.setLayout(self.infoBoxLayout)

        self.infoBox.setGraphicsEffect(self.shadow2)


        self.leaseBtn = QPushButton(self)
        self.leaseBtn.setStyleSheet('QPushButton {\n'
                                     '   background: rgb(0, 223, 71);\n'
                                     '   color: white;\n'
                                     '   border: 0px solid white;\n'
                                     '   margin-bottom: 10px;\n'
                                     '   margin-right: 20px;\n'
                                     '}\n'
                                     'QPushButton:hover {\n'
                                     '   background: rgb(0, 160, 45);\n'
                                     '}\n'
                                     'QPushButton:pressed {\n'
                                     '   background: rgb(0, 110, 35);\n'
                                     '}\n')
        self.leaseBtn.setFont(QtGui.QFont('Arial', 12, 800))
        self.leaseBtn.setText('Lease')
        self.leaseBtn.setFixedHeight(65)
        self.leaseBtn.setFixedWidth(180)
        self.leaseBtn.setGraphicsEffect(self.shadow3)
        self.leaseBtn.clicked.connect(self.goToLeaseIdlePage)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.dockerSpecsLabel)
        self.layout.addWidget(self.infoBox, alignment = QtCore.Qt.AlignTop)
        self.layout.addWidget(self.leaseBtn, alignment = QtCore.Qt.AlignRight)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(30)

        self.setLayout(self.layout)

    def darkTheme(self):
        self.setStyleSheet( 'background: rgb(57, 57, 57);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

    def lightTheme(self):
        self.setStyleSheet( 'background: rgb(204, 204, 204);\n'
                            'color: black;\n'
                            'border: 0px solid black;\n')

    def classicTheme(self):
        self.setStyleSheet( 'background: rgb(0, 23, 37);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')
    
    def goToLeaseIdlePage(self):
        self.parent.parent.receiver.mark_available()
        self.parent.leaseIdlePage.show()
        self.parent.dockerSpecificationsPage.hide()
        self.parent.leaseIdlePage.startLeasing()
        self.destroy()
        # self.parent.leaseExecPage.show()
        # self.parent.dockerSpecificationsPage.hide()

class LeaseIdlePage(QWidget):
    def __init__(self, parent):
        super(LeaseIdlePage, self).__init__()

        self.parent = parent

        self.current_theme = self.parent.current_theme
        self.current_font = self.parent.current_font

        self.setStyleSheet( 'background: rgb(149, 149, 149);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

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

        self.idleLabel = QLabel(self)
        self.idleLabel.setText('Idle')
        self.idleLabel.setFont(QtGui.QFont('Arial', 100, 400))
        self.idleLabel.adjustSize()
        self.idleLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.idleLabel.setStyleSheet(   'background: transparent;\n'
                                        'border: 0px solid black;\n'
                                        'font-weight: bold;\n')

        # self.idleLabel.setGraphicsEffect(self.shadow)

        self.stopBtn = QPushButton(self)
        self.stopBtn.setStyleSheet('QPushButton {\n'
                                     '   background: rgb(246, 49, 49);\n'
                                     '   color: white;\n'
                                     '   border: 0px solid black;\n'
                                     '   margin: 20px;\n'
                                     '   font-weight: bold;\n'
                                     '}\n'
                                     'QPushButton:hover {\n'
                                     '   background: rgb(200, 39, 39);\n'
                                     '}\n'
                                     'QPushButton:pressed {\n'
                                     '   background: rgb(123, 25, 25);\n'
                                     '}\n')
        self.stopBtn.setFont(QtGui.QFont('Arial', 25, 900))
        self.stopBtn.setText('Stop')
        self.stopBtn.setFixedHeight(125)
        self.stopBtn.setFixedWidth(325)
        self.stopBtn.setGraphicsEffect(self.shadow2)
        self.stopBtn.clicked.connect(self.goToDockerSpecificationsPage)

        layout = QVBoxLayout()
        layout.addWidget(self.idleLabel, alignment = QtCore.Qt.AlignHCenter)
        layout.addWidget(self.stopBtn, alignment = QtCore.Qt.AlignHCenter)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)

        widget = QWidget(self)
        widget.setLayout(layout)
        widget.setContentsMargins(0, -120, 0, -120)
        widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widget)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)
    
    def startLeasing(self):
        self.parent.changeStatus('idle')

    def goToDockerSpecificationsPage(self):
        self.parent.changeStatus('not_leasing')
        # self.parent.parent.receiver.mark_unava
        self.parent.dockerSpecificationsPage.show()
        self.parent.leaseIdlePage.hide()
    
    def goToExecPage(self):
        self.parent.leaseExecPage.show()
        self.parent.leaseExecPage.startExecuting()
        self.parent.leaseIdlePage.hide()

class LeaseExecPage(QWidget):
    def __init__(self, parent):
        super(LeaseExecPage, self).__init__()

        self.parent = parent
        self.started = datetime.now()

        self.current_theme = self.parent.current_theme
        self.current_font = self.parent.current_font

        self.setStyleSheet( 'background: rgb(2, 54, 50);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor('rgb(0, 0, 0)'))

        self.execLabel = QLabel(self)
        self.execLabel.setText('Executing')
        self.execLabel.setFont(QtGui.QFont('Arial', 100, 400))
        self.execLabel.adjustSize()
        self.execLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.execLabel.setStyleSheet(   'background: transparent;\n'
                                        'border: 0px solid black;\n'
                                        'font-weight: bold;\n')

        
        self.cpuUsageLabel = QLabel(self)# self.hardwareUsageLabel.setText('CPU: ' + str('%.2f' % self.parent.dockerInfo.getCpuUsage()) + '\nRAM: ' + str('%.2f' % self.parent.dockerInfo.getMemUsage()) + '\nET: ' + str(datetime.now() - self.started))
        self.cpuUsageLabel.setFont(QtGui.QFont('Arial', 20, 400))
        self.cpuUsageLabel.adjustSize()
        self.cpuUsageLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.cpuUsageLabel.setStyleSheet(  'background: transparent;\n'
                                            'border: 0px solid black;\n'
                                            'font-weight: bold;\n'
                                            'margin-left: 5px;\n')
        
        self.memUsageLabel = QLabel(self)
        self.memUsageLabel.setFont(QtGui.QFont('Arial', 20, 400))
        self.memUsageLabel.adjustSize()
        self.memUsageLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.memUsageLabel.setStyleSheet(   'background: transparent;\n'
                                            'border: 0px solid black;\n'
                                            'font-weight: bold;\n'
                                            'margin-left: 5px;\n')
        
        self.elapsedTimeLabel = QLabel(self)
        self.elapsedTimeLabel.setFont(QtGui.QFont('Arial', 20, 400))
        self.elapsedTimeLabel.adjustSize()
        self.elapsedTimeLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.elapsedTimeLabel.setStyleSheet('background: transparent;\n'
                                            'border: 0px solid black;\n'
                                            'font-weight: bold;\n'
                                            'margin-left: 5px;\n')

        layout = QVBoxLayout()
        layout.addWidget(self.execLabel, alignment = QtCore.Qt.AlignHCenter)
        layout.addWidget(self.cpuUsageLabel, alignment = QtCore.Qt.AlignVCenter)
        layout.addWidget(self.memUsageLabel, alignment = QtCore.Qt.AlignVCenter)
        layout.addWidget(self.elapsedTimeLabel, alignment = QtCore.Qt.AlignVCenter)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        widget = QWidget(self)
        widget.setLayout(layout)
        widget.setContentsMargins(0, -120, 0, -120)
        widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widget)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)
    
    def darkTheme(self):
        self.setStyleSheet( 'background: rgb(149, 149, 149);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')

    def lightTheme(self):
        self.setStyleSheet( 'background: rgb(204, 204, 204);\n'
                            'color: black;\n'
                            'border: 0px solid black;\n')

    def classicTheme(self):
        self.setStyleSheet( 'background: rgb(0, 23, 37);\n'
                            'color: white;\n'
                            'border: 0px solid white;\n')
    
    def startExecuting(self):
        self.parent.changeStatus('executing')
        self.getRealTimeHWUsage()
    
    def getRealTimeHWUsage(self):
        t1 = threading.Thread(target=self.getDockerCpuUsage)
        t1.daemon = True
        t1.start()

        t2 = threading.Thread(target=self.getDockerMemUsage)
        t2.daemon = True
        t2.start()

        t3 = threading.Thread(target=self.getElapsedTime)
        t3.daemon = True
        t3.start()

    def getDockerCpuUsage(self):
        starttime=time.time()
        while True:
            self.cpuUsage = str('%.2f' % self.parent.dockerInfo.getCpuUsage())
            self.cpuUsageLabel.setText('CPU: ' + self.cpuUsage + '%')
            self.cpuUsageLabel.adjustSize()
            time.sleep(1)
    
    def getDockerMemUsage(self):
        starttime=time.time()
        while True:
            self.memUsage = str('%.2f' % self.parent.dockerInfo.getMemUsage())
            self.memUsageLabel.setText('RAM: ' + self.memUsage + '%')
            self.memUsageLabel.adjustSize()
            time.sleep(1)
    
    def getElapsedTime(self):
        starttime=time.time()
        while True:
            self.elapsedTimeLabel.setText('ET: ' + str(datetime.now() - self.started))
            self.elapsedTimeLabel.adjustSize()
            time.sleep(1)

    def getRealTimeCpuUsage(self):
        self.hardwareUsageLabel.setText('CPU: %.2f' % self.parent.dockerInfo.getCpuUsage())
    
    def finishExecuting(self, e):
        self.parent.changeStatus('idle')
        self.parent.leaseExecPage.hide()
        self.parent.leaseIdlePage.show()

class LeasePage(QWidget):
    def __init__(self, parent):
        super(LeasePage, self).__init__()

        self.parent = parent
        self.setStyleSheet("background: rgb(57, 57, 57);\n"
                           "border: 0px solid rgb(25, 118, 210);\n"
                           "color: white;\n")

        self.current_theme = self.parent.current_theme
        self.current_font = self.parent.current_font

        self.status = self.parent.lease_status

        self.dockerInfo = DockerInfo()

        self.dockerSpecificationsPage = DockerSpecificationsPage(self)
        self.noDockerFoundPage = NoDockerFoundPage(self)
        self.leaseIdlePage = LeaseIdlePage(self)
        self.leaseExecPage = LeaseExecPage(self)

        layout = QVBoxLayout()

        layout.addWidget(self.noDockerFoundPage)
        layout.addWidget(self.dockerSpecificationsPage)
        layout.addWidget(self.leaseIdlePage)
        layout.addWidget(self.leaseExecPage)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignHCenter)
        layout.setSpacing(30)

        widget = QWidget(self)
        widget.setLayout(layout)
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.setLayout(self.layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    
    def openLeasePage(self):
        if (self.status == 'idle'):
            self.dockerSpecificationsPage.goToLeaseIdlePage()
            self.leaseIdlePage.startLeasing()
            self.leaseExecPage.hide()
            self.noDockerFoundPage.hide()
            self.dockerSpecificationsPage.hide()
        elif (self.status == 'executing'):
            self.leaseIdlePage.goToExecPage()
            self.leaseExecPage.startExecuting()
            self.leaseIdlePage.hide()
            self.noDockerFoundPage.hide()
            self.dockerSpecificationsPage.hide()
        elif (self.status == 'not_leasing'):
            self.leaseIdlePage.hide()
            self.leaseExecPage.hide()
            if (self.dockerInfo.dockerExists()):
                self.noDockerFoundPage.hide()
            else:
                self.dockerSpecificationsPage.hide()

    def changeStatus(self, e):
        self.parent.lease_status = e
        self.status = e