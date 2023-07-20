from ctypes.wintypes import HBITMAP
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt

class refDlg(QDialog):
    def __init__(self):
        super().__init__()
        self.scr= ""
        self.setWindowTitle('화면참조')
        

    def initDB(self, dbConnection):
        self.dbConnection = dbConnection
        self.initUI()

    def initUI(self):
        self.resize(200, 100)
        vBox = QVBoxLayout()
        self.refComb = QComboBox()
        #db scr 조회
        cursor = self.dbConnection.db.cursor()
        cursor.execute("SELECT Screen_No FROM Scr_TBL Group by Screen_No order by Screen_No asc")
        rows = cursor.fetchall()
        scrList = []
        for row in rows:
            if '"' in row[0] : continue
            scrList.append(row[0])
        self.refComb.addItems(scrList)        
        refbtn = QPushButton('참조',self)
        refbtn.clicked.connect(self.refBtnClicked)
        vBox.addWidget(self.refComb)
        vBox.addWidget(refbtn)

        self.setLayout(vBox)
        self.dbConnection.db.commit()
        cursor.close()
            
    def refBtnClicked(self):
        self.scr=self.refComb.currentText()
        self.close()