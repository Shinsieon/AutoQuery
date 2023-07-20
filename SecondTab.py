from ctypes.wintypes import HBITMAP
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt
from refDlg import refDlg

class SecondTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vBoxParent = QVBoxLayout()
        hBoxParent = QHBoxLayout()
        
        hBox = QHBoxLayout()
        scrNumLbl = QLabel("화면번호", self)
        self.scrNumEdit = QLineEdit("",self)
        self.scrNumEdit.returnPressed.connect(self.scrNumBtnClicked)
        self.scrNumBtn = addButton("추가")
        self.scrNumBtn.clicked.connect(self.scrNumBtnClicked)
        self.scrNumBtn.setEnabled(False)
        self.insertBtn = QPushButton('Query Insert', self)
        self.insertBtn.setStyleSheet("height: 30px; border : 2px solid #e9e9e9; color: #222; background: #fff; border-radius : 10px; font-size :13px;")
        self.cleanBtn = QPushButton("Clean",self)
        self.cleanBtn.clicked.connect(self.cleanBtnClicked)
        self.cleanBtn.setStyleSheet("background: #ffd0d5; color: #ff132f; border-radius : 10px; border: none;height:30px;")
        self.insertBtn.clicked.connect(self.insertBtnClicked)
        self.insertBtn.setEnabled(False)

        hBox.addWidget(scrNumLbl)
        hBox.addWidget(self.scrNumEdit)
        hBox.addWidget(self.scrNumBtn)
        hBox.addStretch(3)
        self.scrListBox = QListWidget()
        self.scrListBox.itemDoubleClicked.connect(lambda : self.ListBoxDblCliecked(self.scrListBox))
        vBox = QVBoxLayout()
        vBox.addLayout(hBox)
        vBox.addWidget(self.scrListBox)
        
        hBox2 = QHBoxLayout()
        grpNameLbl = QLabel("메뉴그룹", self)
        self.grpNameEdit = QLineEdit("",self)
        self.grpNameEdit.returnPressed.connect(self.grpNameBtnClicked)
        self.grpNameBtn = addButton("추가")
        self.grpNameBtn.clicked.connect(self.grpNameBtnClicked)
        self.grpNameBtn.setEnabled(False)
        
        self.refScrBtn = QPushButton('화면참조', self)
        self.refScrBtn.setEnabled(False)
        self.refScrBtn.clicked.connect(self.refScrBtnClicked)
        hBox2.addWidget(grpNameLbl)
        hBox2.addWidget(self.grpNameEdit)
        hBox2.addWidget(self.grpNameBtn)
        hBox2.addWidget(self.refScrBtn)
        hBox2.addStretch(3)
        self.grpNameBox = QListWidget()
        self.grpNameBox.itemDoubleClicked.connect(lambda : self.ListBoxDblCliecked(self.grpNameBox))
        vBox2 = QVBoxLayout()
        vBox2.addLayout(hBox2)
        vBox2.addWidget(self.grpNameBox)
        vBox2.addWidget(self.insertBtn)
        vBox2.addWidget(self.cleanBtn)

        hBoxParent.addLayout(vBox)
        hBoxParent.addLayout(vBox2)
        
        rsthBox = QHBoxLayout()
        vBoxParent.addLayout(hBoxParent)
        vBoxParent.addLayout(rsthBox)
        
        self.setLayout(vBoxParent)

    def initDB(self, dbConnection):
        self.dbConnection = dbConnection

    def scrNumBtnClicked(self):
        if(self.scrNumEdit.text() == '' or self.dupCheck(self.scrListBox,self.scrNumEdit.text())):
            return
        else:
            self.scrListBox.addItem(self.scrNumEdit.text())
            self.scrNumEdit.setText('')

    def dupCheck(self, listbox, editTxt):
        if(len(listbox.findItems(editTxt,QtCore.Qt.MatchExactly))==0):
            return False
        else : return True

        
    def grpNameBtnClicked(self):
        if(self.grpNameEdit.text() == '' or self.dupCheck(self.grpNameBox,self.grpNameEdit.text())):
            return
        else:
            self.grpNameBox.addItem(self.grpNameEdit.text())
            self.grpNameEdit.setText('')
    def refScrBtnClicked(self):
        dlg = refDlg()
        dlg.initDB(self.dbConnection)
        dlg.exec()
        if len(dlg.scr)>0 :
            self.addGrpNameBox(dlg.scr)
    def ListBoxDblCliecked(self, LW):
        LW.takeItem(LW.currentRow())
        
    def selectBtnEnabled(self,bool):
        self.scrNumBtn.setEnabled(bool)
        self.grpNameBtn.setEnabled(bool)
        self.refScrBtn.setEnabled(bool)
        self.insertBtn.setEnabled(bool)
    
    def cleanBtnClicked(self):
        self.scrListBox.clear()
        self.grpNameBox.clear()
    def addGrpNameBox(self,scr):
        self.grpNameBox.clear()
        cursor = self.dbConnection.db.cursor()
        cursor.execute("SELECT Group_Name FROM Scr_TBL Where Screen_No ='"+scr+"'")
        rows = cursor.fetchall()
        grpList = []
        for row in rows:
            if row[0] in grpList:
                continue
            else:
                grpList.append(row[0])
                self.grpNameBox.addItem(row[0])
                    
        self.dbConnection.db.commit()
        cursor.close()

    def insertBtnClicked(self):
        Qmsg = QMessageBox()
        Qmsg.setIcon(QMessageBox.Information)
        Qmsg.setWindowTitle('MessageBox')
        Qmsg.setText('추가하시겠습니까?')
        Qmsg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = Qmsg.exec_()

        if(retval == QMessageBox.Ok):
            scrList = [self.scrListBox.item(x).text() for x in range(self.scrListBox.count())]
            
            grpList = [self.grpNameBox.item(x).text() for x in range(self.grpNameBox.count())]
            sql_query1 = 'insert into Scr_TBL values '
            sql_query2 = ""
            isEnd = ","
            if len(scrList)>0 and len(grpList)>0:
                for i in range(len(scrList)):
                    for j in range(len(grpList)):
                        if (i == (len(scrList)-1)) & (j==(len(grpList)-1)): isEnd = ";"
                        #sql_query2 += "('"+str(grpList[j])+"','B0','A','"+str(scrList[i])+"'), ('"+str(grpList[j])+"','B2','A','"+str(scrList[i])+"')"+isEnd
                        sql_query2 += '("%s", "B0","A","%s"),("%s", "B2","A","%s")%s' % (''.join(str(grpList[j])), ''.join(str(scrList[i])), ''.join(str(grpList[j])),''.join(str(scrList[i])),isEnd)
                try:
                    cursor = self.dbConnection.db.cursor()
                    sql = sql_query1+sql_query2
                    cursor.execute(sql)
                    self.dbConnection.db.commit()
                    cursor.close()
                    QMessageBox.about(self,'success',"success")
                except self.dbConnection.mdb.Error as e:
                    QMessageBox.about(self,'fail',str(e))

class addButton(QPushButton):
    def __init__(self,text):
        super().__init__()
        self.setText(text)
        self.setIcon(QIcon('assets/plus.png'))
        self.setStyleSheet("background-color:transparent;")
