# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DragAndDropScroll.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets

class scrollingFrame(QtWidgets.QScrollArea):
    def __init__(self, parent, container):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.container = container
        self.form = QtWidgets.QFormLayout()
        self.parentWidget = self.container
        self.groupBox = QtWidgets.QGroupBox('')
        self.setFixedHeight(121)
        self.emptyLayout = QtWidgets.QVBoxLayout(self)

        # self.setCentralWidget(self.container)
    
    def dragEnterEvent(self, e):
        # self.uploadLabel = self.container.uploadLabel
        # self.uploadLabel.hide()
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
        # self.uploadLabel.show()
        self.setStyleSheet("background: rgb(150, 150, 150);\n"
                           "border: 1px solid rgb(150, 150, 150);\n"
                           "color: white")

    def dropEvent(self, e):
        # self.container.uploadLabel.setStyleSheet("background: rgb(150, 150, 150);\n"
        #                    "border: 1px solid rgb(150, 150, 150);\n"
        #                    "color: white")
        
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

        # if (self.form.rowCount() == 1 and self.form.takeAt(0).widget().text() == 'Drag & drop files here'):
        #     self.form.removeRow(0)
        #     print(self.form.rowCount())
        #     layout = QtWidgets.QVBoxLayout(self)
        #     layout.addWidget(self)

        for url in e.mimeData().urls():
            f, file_src = str(url.toString()).split('///')
            file_dir, file_name = os.path.split(file_src)
            
            print(file_src)
            # self.container.uploadLabel.setText(self.container.uploadLabel.text() + file_name + '\n')
            # self.container.uploadLabel.adjustSize()
            label = QtWidgets.QLabel(file_name)
            btn = QtWidgets.QPushButton('Remove')

            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)

            label.setFont(font)
            label.setFixedWidth(270)
            btn.setFont(font)
            btn.setFixedWidth(50)

            btn.clicked.connect(self.clickedRemove)

            self.form.addRow(label, btn)
        
        self.groupBox.setLayout(self.form)
        self.setWidget(self.groupBox)
    
    def clickedRemove(self):
        self.form.removeRow(self.sender())
        # if (self.form.rowCount() == 0):
        #     self.uploadLabel.show()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(421, 283)
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(16)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("QPushButton {\n"
"    background: rgb(232, 232, 232);\n"
"    border: 1px solid rgb(227, 227, 227);\n"
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
        # MainWindow.setLayout(QtWidgets.QVBoxLayout())
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scroll = scrollingFrame(self.centralwidget, self)
        self.scroll.setGeometry(QtCore.QRect(30, 70, 361, 121))
        self.scroll.setStyleSheet("background: rgb(150, 150, 150);\n"
                           "border: 1px solid rgb(150, 150, 150)")
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("scroll")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 359, 119))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.uploadLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.uploadLabel.setStyleSheet('color: white')
        self.uploadLabel.setGeometry(QtCore.QRect(100, 50, 144, 17))
        
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(14)
        self.uploadLabel.setFont(font)
        self.uploadLabel.setObjectName("uploadLabel")
        self.scroll.setWidget(self.scrollAreaWidgetContents)
        self.uploadBtn = QtWidgets.QPushButton(self.centralwidget)
        self.uploadBtn.setGeometry(QtCore.QRect(320, 200, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(12)
        self.uploadBtn.setFont(font)
        self.uploadBtn.setStyleSheet("color: white;")
        self.uploadBtn.setObjectName("uploadBtn")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 210, 43))
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 421, 18))
        self.menubar.setObjectName("menubar")
        # self.menuEdit = QtWidgets.QMenu(self.menubar)
        # self.menuEdit.setObjectName('menuEdit')
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # self.actionUndo = QtWidgets.QAction(MainWindow)
        # self.actionUndo.setObjectName('actionUndo')
        # self.menuEdit.addAction(self.actionUndo)
        # self.menubar.addAction(self.menuEdit.menuAction())

        # self.actionUndo.triggered.connect(self.undoLast)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.uploadLabel.setText(_translate("MainWindow", "Drag & drop files here"))
        self.uploadBtn.setText(_translate("MainWindow", "Upload"))
        self.label.setText(_translate("MainWindow", "Drag & Drop"))
        self.uploadLabel.adjustSize()
        # self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        # self.actionUndo.setText(_translate("MainWindow", "Undo"))
        # self.actionUndo.setStatusTip(_translate("MainWindow", "Undo last change"))
        # self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z"))

    def undoLast(self, e):
        if (str(self.uploadLabel.text()) != 'Drag & drop files here'):
            current = str(self.uploadLabel.text())
            self.uploadLabel.setText(current.rsplit('\n', 1)[0])

if __name__ == "__main__":
    import sys
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
