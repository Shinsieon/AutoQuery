from ctypes.wintypes import HBITMAP
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt

class addUser(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('사용자 추가')
        self.initUI()

    def initUI(self):
        self.resize(200, 100)
        self.vBox = QVBoxLayout()
        self.gridlayout = QGridLayout()
        self.makeLayout(['Seq','Root','Dept','Parent','Group No','Node Type','Node Name','View YN','ID','Duty','Menu No','Gender','Biz Assign','Part','Duty Code','Part Code'])
        self.flag = False
        #db scr 조회
        insertBtn = QPushButton("추가", self)
        insertBtn.clicked.connect(self.insertBtnClicked)
        self.vBox.addLayout(self.gridlayout)
        self.vBox.addWidget(insertBtn)

        self.setLayout(self.vBox)
       
    def makeLayout(self, labelArray):
        for i in range(len(labelArray)):
            globals()['lab{}'.format(i)] = QLabel(labelArray[i], self)
            globals()['lineEdit{}'.format(i)] = QLineEdit("", self)
            self.gridlayout.addWidget(globals()['lab{}'.format(i)], i, 0)
            self.gridlayout.addWidget(globals()['lineEdit{}'.format(i)], i, 1)

    def valueCheck(self):
        for i in range(16):
            if len(globals()['lineEdit{}'.format(i)].text()) == 0:
                return False
        return True
    def insertBtnClicked(self):
        if self.valueCheck() == False:
            QMessageBox.about(self,'alert','필드값을 채워주세요')
        else:
            self.Seq = globals()['lineEdit{}'.format(0)].text()
            self.Root = globals()['lineEdit{}'.format(1)].text()
            self.Dept = globals()['lineEdit{}'.format(2)].text()
            self.Parent = globals()['lineEdit{}'.format(3)].text()
            self.Group_No = globals()['lineEdit{}'.format(4)].text()
            self.Node_Type = globals()['lineEdit{}'.format(5)].text()
            self.Node_Name = globals()['lineEdit{}'.format(6)].text()
            self.View_YN = globals()['lineEdit{}'.format(7)].text()
            self.ID = globals()['lineEdit{}'.format(8)].text()
            self.Duty = globals()['lineEdit{}'.format(9)].text()
            self.Menu_No = globals()['lineEdit{}'.format(10)].text()
            self.Gender = globals()['lineEdit{}'.format(11)].text()
            self.Biz_Assign = globals()['lineEdit{}'.format(12)].text()
            self.Part = globals()['lineEdit{}'.format(13)].text()
            self.Duty_Code = globals()['lineEdit{}'.format(14)].text()
            self.Part_Code = globals()['lineEdit{}'.format(15)].text()
            self.flag = True
            self.close()
