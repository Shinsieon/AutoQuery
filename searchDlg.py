
from ctypes.wintypes import HBITMAP
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt

class searchDlg(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.searchText= ""
        self.setWindowTitle('검색')
        self.initUI()

    def initUI(self):
        self.resize(200, 100)
        vBox = QVBoxLayout()
        self.searchTxtField = QLineEdit()
        self.searchTxtField.setFocusPolicy(Qt.StrongFocus)
        self.searchTxtField.textChanged.connect(self.searchtextChanged)
        self.searchTxtField.returnPressed.connect(lambda : self.searchbtnClicked(True))
        self.moreBtn = QPushButton("다음 찾기")
        self.moreBtn.setEnabled(False)
        self.moreBtn.clicked.connect(self.moreBtnClicked)
        self.searchbtn = QPushButton('찾기',self)
        self.searchbtn.clicked.connect(lambda : self.searchbtnClicked(False))
        vBox.addWidget(self.searchTxtField)
        vBox.addWidget(self.searchbtn)
        vBox.addWidget(self.moreBtn)

        self.setLayout(vBox)
        self.searchTxtField.setFocus()
    def searchtextChanged(self):
        self.searchbtn.setEnabled(True)
        self.moreBtn.setEnabled(False)
    def moreBtnEnabled(self, bool):
        self.moreBtn.setEnabled(bool)
        
        if self.itemcount>1: self.searchbtn.setEnabled(not bool)
        else: self.searchbtn.setEnabled(bool)

    def moreBtnClicked(self):
        if self.parent.item:
            self.parent.item.setSelected(False)
        self.parent.findMenu(self.searchTxtField.text(), self.itemcount)


    def searchbtnClicked(self, isTxtField):
        if isTxtField == True:
            if self.moreBtn.isEnabled() == True:
                self.moreBtnClicked()
                return
        if self.parent.item:
            self.parent.item.setSelected(False)
        self.itemcount = 0
        self.searchText=self.searchTxtField.text()
        if not self.searchText : return
        self.parent.findMenu(self.searchText,0)
    
        #self.close()