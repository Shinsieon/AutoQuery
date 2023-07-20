from ctypes.wintypes import HBITMAP
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt
from addUser import addUser

class FirstTab(QWidget):
    def __init__(self):
        super().__init__()
        self.scrChangeList = []
        self.initUI()
        
    def selectBtnEnabled(self,bool):
        self.selectBtn.setEnabled(bool)
        self.menuGrpSearchBtn.setEnabled(bool)
        self.scrSearchBtn.setEnabled(bool)
        self.addUsrBtn.setEnabled(bool)
        if bool == True:
            self.scrEdit.returnPressed.connect(self.scrSearchBtnClicked)
            self.menuGrpEdit.returnPressed.connect(self.menuGrpSearchBtnClicked)
            self.idEdit.returnPressed.connect(self.selectUserTBL)

        else:
            self.scrEdit.returnPressed.disconnect()
            self.menuGrpEdit.returnPressed.disconnect()
            self.idEdit.returnPressed.disconnect()
    def initDB(self, dbConnection):
        self.dbConnection = dbConnection

    def initUI(self):
        self.vBox = QVBoxLayout()
        
        hBox = QHBoxLayout()
        idLabel = QLabel("사번/이름/부서코드", self)
        self.idEdit = QLineEdit('',self)
        self.selectBtn = SelectButton('조회')
        self.delUsrBtn = deleteButton('')
        self.delUsrBtn.setStyleSheet("background-color:transparent")

        self.addUsrBtn = QPushButton('',self)
        self.addUsrBtn.setIcon(QIcon('assets/plus.png'))
        self.addUsrBtn.setStyleSheet("background-color:transparent")
        
        self.selectBtn.clicked.connect(self.selectUserTBL)
        self.delUsrBtn.clicked.connect(self.deleteUsrItem)
        self.addUsrBtn.clicked.connect(self.addUsrItem)

        self.selectBtn.setEnabled(False)
        self.addUsrBtn.setEnabled(False)
        
        self.userTBL = QTableWidget()
        hBox.addWidget(idLabel)
        hBox.addWidget(self.idEdit)

        hBox.addWidget(self.selectBtn)
        hBox.addWidget(self.delUsrBtn)
        hBox.addWidget(self.addUsrBtn)
        hBox.addStretch(3)
        hBox.setAlignment(QtCore.Qt.AlignTop)

        hBox2 = QHBoxLayout()
        menuGrpLabel = QLabel("메뉴그룹조회",self)
        self.menuGrpEdit = QLineEdit('',self)
        self.menuGrpSearchBtn = SelectButton('조회')
        self.menuGrpSearchBtn.clicked.connect(self.menuGrpSearchBtnClicked)
        self.menuGrpSearchBtn.setEnabled(False)
        
        
        self.menuGrpSearchTbl = QTableWidget()
        hBox2.addWidget(menuGrpLabel)
        hBox2.addWidget(self.menuGrpEdit)
        hBox2.addWidget(self.menuGrpSearchBtn)
        hBox2.addStretch(3)

        hBox3 = QHBoxLayout()
        scrLabel = QLabel("화면번호조회(그룹조회가능)",self)
        self.scrEdit = QLineEdit('',self)
        self.scrSearchBtn = SelectButton('조회')
        self.scrSearchBtn.clicked.connect(self.scrSearchBtnClicked)
        self.scrSearchBtn.setEnabled(False)

        self.delScrBtn = deleteButton('')
        self.delScrBtn.clicked.connect(self.deleteScrItem)

        self.updateScrBtn = modifyButton('')
        self.updateScrBtn.clicked.connect(self.updateScrTBL)

        self.scrSearchTbl = QTableWidget()
        self.scrSearchTbl.cellChanged.connect(self.scrTBLChanged)

        hBox3.addWidget(scrLabel)
        hBox3.addWidget(self.scrEdit)
        hBox3.addWidget(self.scrSearchBtn)
        hBox3.addWidget(self.delScrBtn)
        hBox3.addWidget(self.updateScrBtn)
        hBox3.addStretch(3)
        
        
        self.vBox.addLayout(hBox)
        self.vBox.addWidget(self.userTBL)

        self.vBox.addLayout(hBox2)
        self.vBox.addWidget(self.menuGrpSearchTbl)

        self.vBox.addLayout(hBox3)
        self.vBox.addWidget(self.scrSearchTbl)
        
        self.vBox.addStretch(3)
        self.setLayout(self.vBox)

    def selectUserTBL(self):
        cursor = self.dbConnection.db.cursor()
        cursor.execute("SELECT * FROM User_Total_TBL Where ID like '%" +str(self.idEdit.text())+"%' or Node_Name='"+str(self.idEdit.text())+"' or Part_Code = '"+str(self.idEdit.text())+"'")
        rows = cursor.fetchall()
        self.clearUserTBL()
        if(len(rows)==0):
            QMessageBox.about(self,'alert','검색 내용이 존재하지 않습니다.')
        else:
            self.userTBL.setRowCount(len(rows))
            self.userTBL.setColumnCount(len(rows[0]))
            self.userTBL.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.userTBL.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.userTBL.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.userTBL.setHorizontalHeaderLabels(['Seq','Root','Dept','Parent','Group_No','Node_Type','Node_Name','View_Yn','ID','Duty','Menu_No','Gender','Biz_Assign','Part','Duty_Code','Part_Code'])
            for i in range(len(rows)):
                for j in range(len(rows[0])):
                    self.userTBL.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
            self.userTBL.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.userTBL.itemDoubleClicked.connect(self.userTBLDblClicked)

        self.dbConnection.db.commit()
        cursor.close()
    def deleteUsrItem(self):
        if self.userTBL.currentRow() !=-1:
            self.Qmsg = QMessageBox()
            self.Qmsg.setIcon(QMessageBox.Information)
            self.Qmsg.setWindowTitle('MessageBox')
            self.Qmsg.setText('선택한 행을 지우시겠습니까?')
            self.Qmsg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = self.Qmsg.exec_()

            if(retval == QMessageBox.Ok):
                id = self.userTBL.selectedItems()[8].text()
                userName = self.userTBL.selectedItems()[6].text()
                try:
                    sql = "DELETE FROM User_Total_TBL where ID='"+id+"' and Node_Name ='"+userName+"';"
                    cursor = self.dbConnection.db.cursor()
                    cursor.execute(sql)
                    self.dbConnection.db.commit()
                    cursor.close()
                    QMessageBox.about(self, "MessageBox","Success")
                    self.userTBL.removeRow(self.userTBL.currentRow())
                except self.dbConnection.mdb.Error as e:
                    QMessageBox.about(self, "MessageBox",str(e))

    def addUsrItem(self):
        dlg = addUser()
        dlg.exec()
        if dlg.flag == True:
            sql_query = 'insert into User_Total_TBL values ("%s", "%s", "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' % (dlg.Seq, dlg.Root,dlg.Dept, dlg.Parent, dlg.Group_No, dlg.Node_Type, dlg.Node_Name, dlg.View_YN, dlg.ID, dlg.Duty, dlg.Menu_No, dlg.Gender, dlg.Biz_Assign, dlg.Part, dlg.Duty_Code, dlg.Part_Code)
            try:
                cursor = self.dbConnection.db.cursor()
                cursor.execute(sql_query)
                self.dbConnection.db.commit()
                cursor.close()
                QMessageBox.about(self,'success',"success")
            except self.dbConnection.mdb.Error as e:
                QMessageBox.about(self,'fail',str(e))


    def menuGrpSearchBtnClicked(self):
        cursor = self.dbConnection.db.cursor()
        cursor.execute("SELECT * FROM Menu_Mapping_TBL Where Biz_Assign like '%"+str(self.menuGrpEdit.text())+"%' or Map_Assign like '%"+str(self.menuGrpEdit.text())+"%'")
        rows = cursor.fetchall()
        self.clearMenuGrpTBL()
        if(len(rows) ==0):
            QMessageBox.about(self,'MessageBox','검색 내용이 존재하지 않습니다.')
        else:
            self.menuGrpSearchTbl.setRowCount(len(rows))
            self.menuGrpSearchTbl.setColumnCount(len(rows[0]))
            self.menuGrpSearchTbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.menuGrpSearchTbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.menuGrpSearchTbl.setHorizontalHeaderLabels(['Map_Assign','Biz_Assign','note'])
            for i in range(len(rows)):
                for j in range(len(rows[0])):
                    self.menuGrpSearchTbl.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
            self.menuGrpSearchTbl.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.menuGrpSearchTbl.itemDoubleClicked.connect(self.menuGrpDblClicked)

        self.dbConnection.db.commit()
        cursor.close()
            
    def scrSearchBtnClicked(self):
        cursor = self.dbConnection.db.cursor()
        cursor.execute("SELECT * FROM Scr_TBL Where Screen_No='"+str(self.scrEdit.text())+"' or Group_Name='"+str(self.scrEdit.text()+"'"))
        rows = cursor.fetchall()
        self.clearScrTBL()
        if(len(rows) ==0):
            QMessageBox.about(self,'alert','검색 내용이 존재하지 않습니다.')
        else:
            self.scrSearchTbl.setRowCount(len(rows))
            self.scrSearchTbl.setColumnCount(len(rows[0]))
            self.scrSearchTbl.setEditTriggers(QAbstractItemView.DoubleClicked)
            self.scrSearchTbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.scrSearchTbl.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.scrSearchTbl.setSelectionMode(QAbstractItemView.MultiSelection)
            self.scrSearchTbl.setHorizontalHeaderLabels(['Group_Name','Project_CLS','Use_CLS','Screen_No'])
            self.prevItems = rows
            self.scrSearchTbl.blockSignals(True)
            for i in range(len(rows)):
                for j in range(len(rows[0])):
                    self.scrSearchTbl.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
            self.scrSearchTbl.blockSignals(False)
        self.dbConnection.db.commit()
        cursor.close()
    
    def userTBLDblClicked(self, item):
        self.menuGrpEdit.setText(self.userTBL.selectedItems()[12].text())
    def menuGrpDblClicked(self,item):
        self.scrEdit.setText(self.menuGrpSearchTbl.selectedItems()[0].text())

    def deleteScrItem(self):
        crtRow = self.scrSearchTbl.currentRow()
        deleteItems = self.scrSearchTbl.selectedItems()
        if(crtRow == -1): return
        clItems = []
        clarr=[]

        for i in range(1, len(deleteItems)+1):
            clarr.append(deleteItems[i-1].text())
            if(i%4==0):
                clItems.append(clarr)
                clarr = []

        self.Qmsg = QMessageBox()
        self.Qmsg.setIcon(QMessageBox.Information)
        self.Qmsg.setWindowTitle('MessageBox')
        self.Qmsg.setText('선택한 행을 지우시겠습니까?')
        self.Qmsg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.Qmsg.exec_()

        if(retval == QMessageBox.Ok):
            try:
                for i in clItems:
                    sql = "DELETE FROM Scr_TBL where Group_Name='"+i[0] + "' and Project_CLS = '"+i[1] + "' and Use_CLS = '"+i[2] + "' and Screen_No='"+i[3] + "'"
                    cursor = self.dbConnection.db.cursor()
                    cursor.execute(sql)
                    self.dbConnection.db.commit()
                    cursor.close()
                QMessageBox.about(self, "MessageBox","선택한 행을 성공적으로 제거했습니다.")
                rows = set()
                for index in self.scrSearchTbl.selectedIndexes():
                    rows.add(index.row())
                for row in sorted(rows, reverse=True):
                    self.scrSearchTbl.removeRow(row)
            except self.dbConnection.mdb.Error as e:
                QMessageBox.about(self, "MessageBox",str(e))

        
    def scrTBLChanged(self,row, col):
        isdup = False
        for i in self.scrChangeList:
            if row == i[0] and col == i[1]:
                isdup = True
        
        if(isdup == True): return

        self.scrChangeList.append([row,col])

    def updateScrTBL(self):
        if len(self.scrChangeList) == 0 : return
        Qmsg = QMessageBox()
        Qmsg.setIcon(QMessageBox.Information)
        Qmsg.setWindowTitle('MessageBox')
        Qmsg.setText('수정하시겠습니까?')
        Qmsg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = Qmsg.exec_()

        if(retval == QMessageBox.Ok):
            for i in self.scrChangeList:
                row = i[0]
                col = i[1]
                curItems = []
                prevItems = []
                for j in range(4):
                    curItems.append(self.scrSearchTbl.item(row,j).text())
                    prevItems.append(self.prevItems[row][j])
                
                try:
                    sql = "UPDATE Scr_TBL SET Group_Name = '"+curItems[0] + "' ,Project_CLS = '" +curItems[1] + "' ,Use_CLS ='"+curItems[2] + "' ,Screen_No= '"+ curItems[3] +"' " 
                    sql_wh = "where Group_Name = '"+prevItems[0] + "' and Project_CLS = '" +prevItems[1] + "' and Use_CLS ='"+prevItems[2] + "' and Screen_No= '"+ prevItems[3] +"'"
                    cursor = self.dbConnection.db.cursor()
                    cursor.execute(sql+sql_wh)
                    self.dbConnection.db.commit()
                    cursor.close()
                    self.scrSearchBtnClicked()
                    self.scrChangeList = []
                    QMessageBox.about(self, "MessageBox","Success")
                except self.dbConnection.mdb.Error as e:
                    QMessageBox.about(self, "MessageBox",str(e))
        else:
            self.scrSearchBtnClicked()


    def clearUserTBL(self):
        if(self.userTBL.rowCount()>0):
            self.userTBL.setRowCount(0)
    def clearMenuGrpTBL(self):
        if(self.menuGrpSearchTbl.rowCount()>0):
            self.menuGrpSearchTbl.setRowCount(0)
    def clearScrTBL(self):
        if(self.scrSearchTbl.rowCount()>0):
            self.scrSearchTbl.setRowCount(0)

class SelectButton(QPushButton):
    def __init__(self,text):
        super().__init__()
        self.setText(text)
        self.setStyleSheet("color : white;background-color: rgb(58,134,255);"
        "border-radius: 5px; width : '80px'; font-weight: bold; height: 18px")

class deleteButton(QPushButton):
    def __init__(self,text):
        super().__init__()
        self.setText(text)
        self.setToolTip("지우기")
        self.setIcon(QIcon('assets/delete.png'))
        self.setStyleSheet("background-color:transparent")

class modifyButton(QPushButton):
    def __init__(self,text):
        super().__init__()
        self.setText(text)
        self.setToolTip("수정하기")
        self.setIcon(QIcon('assets/pen.png'))
        self.setStyleSheet("background-color:transparent")