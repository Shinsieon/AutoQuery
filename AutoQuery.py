from ctypes.wintypes import HBITMAP
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt
from FirstTab import FirstTab
from SecondTab import SecondTab
from ThirdTab import ThirdTab
from DBConnection import dbConnection
import json
from collections import OrderedDict

#pip install mysqlclient
#pip install MySQL-python
#command to make exe file : pyinstaller -w -F AutoQuery.py

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        
    def initUI(self):
        self.setWindowTitle("AutoQuery")
        #self.set_style()
        self.makeUI()

    def set_style(self):
        with open("update_style", "r") as f:
            self.setStyleSheet(f.read())
    def makeUI(self):
        Vsetting = QVBoxLayout()
        self.tab1 = FirstTab()
        self.tab2 = SecondTab()
        self.tab3 = ThirdTab(True)
        tabs = QTabWidget()
        tabs.addTab(self.tab1, '권한조회')
        tabs.addTab(self.tab2, '권한할당')  
        tabs.addTab(self.tab3, '메뉴편집')

       
        #db커넥션
        self.devRadBtn = QRadioButton('개발/테스트', self)
        self.devRadBtn.setChecked(True)
        self.realRadBtn = QRadioButton('운영',self)
        self.ipRadBtn = QRadioButton('직접입력', self)
        self.ipEdit = QLineEdit('',self)
        self.ipEdit.hide()

        dbidLabel = QLabel("ID", self)

        self.idEdit = QLineEdit("eam", self)

        pwLabel = QLabel("Password", self)

        self.pwEdit = QLineEdit("eam123", self)
        self.pwEdit.setEchoMode(QLineEdit.Password)

        dbNameLabel = QLabel("DB" ,self)
        self.dbNameEdit = QLineEdit("eam", self)
        connectBtn = QPushButton("connect", self)
        connectBtn.clicked.connect(self.connectBtnClicked)

        self.devRadBtn.clicked.connect(self.radBtnClicked)
        self.realRadBtn.clicked.connect(self.radBtnClicked)
        self.ipRadBtn.clicked.connect(self.radBtnClicked)
        #---------------------------------#
        Lsetting = QHBoxLayout()
        Lsetting.setAlignment(QtCore.Qt.AlignTop)
        Lsetting.addWidget(self.devRadBtn)
        
        Lsetting.addWidget(self.realRadBtn)
        
        Lsetting.addWidget(self.ipRadBtn)
        
        Lsetting.addWidget(self.ipEdit)
        Lsetting.addWidget(dbidLabel)
        Lsetting.addWidget(self.idEdit)
        Lsetting.addWidget(pwLabel)
        Lsetting.addWidget(self.pwEdit)
        Lsetting.addWidget(dbNameLabel)
        Lsetting.addWidget(self.dbNameEdit)
        Lsetting.addWidget(connectBtn)
        Lsetting.addStretch(1)

        Vsetting.addLayout(Lsetting)
        Vsetting.addWidget(tabs)
        self.setLayout(Vsetting)

    def radBtnClicked(self):
        if(self.ipRadBtn.isChecked()):
            self.ipEdit.show()
        else:self.ipEdit.hide()
    
    def connectBtnClicked(self):
        if(self.devRadBtn.isChecked()):
            addtext= '_'
        elif self.realRadBtn.isChecked(): 
            addtext = '_'
        elif self.ipRadBtn.isChecked():
            addtext = self.ipEdit.text()

        dbC = dbConnection()
        dbObj = {
            'host' : addtext,
            'user' : self.idEdit.text(),
            'password' : self.pwEdit.text(),
            'dbName' : self.dbNameEdit.text(),
            'charset' : 'euckr'
        }
        dbC.setDBinfo(dbObj)
        dbC.openConn()
        if(dbC.isConnect):
            self.tab1.selectBtnEnabled(True)
            self.tab2.selectBtnEnabled(True)
            QMessageBox.about(self, 'Connection','Database connected Successfully')
            
            self.tab1.initDB(dbC)
            self.tab2.initDB(dbC)
            self.tab2.initDB(dbC)
        else:
            self.tab1.selectBtnEnabled(False)
            self.tab2.selectBtnEnabled(False)
            QMessageBox.about(self, 'Connection','Failed To Connect Database')
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.initUI()
    screen = app.primaryScreen()
    size = screen.size()
    w, h = 1200,800
    window.setGeometry(int(size.width()/2-w/2), int(size.height()/2-h/2), w,h)
    window.show()

    app.exec_()
