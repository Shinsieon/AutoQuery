from ctypes.wintypes import HBITMAP
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt
from searchDlg import searchDlg
import time

class TreeWidget(QTreeWidget):
    def __init__(self, parent= None):
        QTreeWidget.__init__(self, parent)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.thirdTabCls = parent

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.thirdTabCls.deleteItemFromParent(self.currentItem())
        else:
            super().keyPressEvent(event)
    def setItemArray(self, itemArray):
        self.itemArray = itemArray

    def dropEvent(self, event):
        self.thirdTabCls.changableState=False
        if event.source() == self:
            QAbstractItemView.dropEvent(self, event)
    def dropMimeData(self, parent, row, data, action):
        if action == Qt.MoveAction:
            return self.moveSelection(parent, row)
        return False
    def moveSelection(self, targetItem, row):
        if targetItem is None : return False
        #순서는 selected Item 지우고 target parent 에 selected Item add
        #selected가 파일인지 폴더인지, target 이 파일인지 폴더인지에 따라 달라짐. target 이 파일이면 같은 레벨로 이동, 폴더이면 포함
        selectedItem = self.currentItem()
        self.thirdTabCls.moveSelectItemToTargetItem(targetItem, selectedItem)
        
        return False
        
class ThirdTab(QWidget):
    def __init__(self,isFirst):
        super().__init__()
        if isFirst == True:
            self.initUI()
            self.item = None
            self.fileName = None
            self.save_data = []
            self.itemArray= []      

    def initUI(self):
        controlHBox = QHBoxLayout()

        loadFileBtn = QPushButton("load", self)
        loadFileBtn.clicked.connect(self.loadFileBtnClicked)
        loadFileBtn.setToolTip("Ctrl+L")
        loadFileBtn.setIcon(QIcon('assets/loadIcon.png'))
        loadFileBtn.setShortcut("Ctrl+L")
        loadFileBtn.setStyleSheet("background-color: transparent;")

        saveBtn = QPushButton('save', self)
        saveBtn.clicked.connect(self.saveBtnClicked)
        saveBtn.setShortcut("Ctrl+S")
        saveBtn.setIcon(QIcon('assets/saveIcon.png'))
        saveBtn.setToolTip("Ctrl+S")
        saveBtn.setStyleSheet("background-color: transparent")

        saveAsBtn = QPushButton("save as", self)
        saveAsBtn.clicked.connect(self.saveAsBtnClicked)
        saveAsBtn.setIcon(QIcon('assets/saveAsIcon.png'))
        saveAsBtn.setStyleSheet("background-color: transparent")


        findBtn = QPushButton('find', self)
        findBtn.clicked.connect(self.findBtnClicked)
        findBtn.setShortcut("Ctrl+F")
        findBtn.setIcon(QIcon('assets/searchIcon.png'))
        findBtn.setToolTip("Ctrl+F")
        findBtn.setStyleSheet("background-color: transparent")

        controlHBox.addWidget(loadFileBtn)
        controlHBox.addWidget(saveBtn)
        controlHBox.addWidget(saveAsBtn)
        controlHBox.addWidget(findBtn)
        controlHBox.addStretch()

        self.changableState = False
        #self.textedit = QTextEdit('', self)
        
        self.menuTree = TreeWidget(self)
        self.menuTree.itemChanged.connect(self.treeItemChanged)
        self.menuTree.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.menuTree.resize(500,400)
        self.menuTree.setColumnCount(9)
        self.menuTree.setHeaderLabels(["메뉴이름", "도시여부", "화면번호","상위화면번호","화면구분","파일명","버튼이름","등급","메뉴구분"])

        self.menuTree.header().resizeSection(0, 250)
        self.menuTree.header().resizeSection(1, 50)
        self.menuTree.header().resizeSection(3, 20)
        self.menuTree.header().resizeSection(5, 150)
        self.menuTree.header().resizeSection(8, 20)
        self.menuTree.header().resizeSection(9, 20)
        self.menuTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.menuTree.customContextMenuRequested.connect(self.menuContextRightClick)
        
        #self.statusLabel = QLabel("",self)
        VBox = QVBoxLayout()
        VBox.addLayout(controlHBox)
        VBox.addWidget(self.menuTree)
        #VBox.addWidget(self.statusLabel)

        self.setLayout(VBox)
   
    def loadFileBtnClicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File','','Menu File(*.mnu);;')
        data = ""
        if fname[0] : 
            self.fileName = fname[0]
            f= open(fname[0], 'rt', encoding='cp949')
            data = f.read()
            if(len(data)==0) : return
            self.changableState = False
            self.menuTree.clear()
        
            self.makeTree(data)
    def findBtnClicked(self):
        self.dlg = searchDlg(self)
        self.dlg.exec()
    def findMenu(self, text, idx):
        self.items = self.menuTree.findItems(text, Qt.MatchContains | Qt.MatchRecursive,0)
        self.items += self.menuTree.findItems(text, Qt.MatchContains | Qt.MatchRecursive,2)
        self.itemcount = len(self.items)
        if self.itemcount == 0:
            QMessageBox.about(self,'MessageBox',"찾을 내용이 존재하지 않습니다")
            self.dlg.moreBtnEnabled(False)
            return
        elif self.itemcount==1:
            self.item = self.items[idx]
            self.menuTree.scrollToItem(self.item)
            self.item.setSelected(True)
            self.dlg.moreBtnEnabled(False)
        else:
            if idx >= self.itemcount: 
                QMessageBox.about(self,'MessageBox',"더이상 찾을 내용이 존재하지 않습니다")
                self.dlg.moreBtnEnabled(False)
                return
            else:
                self.item = self.items[idx]
                self.menuTree.scrollToItem(self.item)
                self.item.setSelected(True)
                self.dlg.itemcount = idx+1
                self.dlg.moreBtnEnabled(True)
                
    def getRowOfItem(self,item):
        return self.itemArray.index(item)

    def menuContextRightClick(self,event):
        self.menu_context = QMenu(self.menuTree)
        clickmenu_addfile = self.menu_context.addAction("자식 아이템 추가")
        clickmenu_addfolder = self.menu_context.addAction("자식 폴더 추가")
        clickmenu_delete = self.menu_context.addAction("메뉴 삭제")
        action2 = self.menu_context.exec_(self.menuTree.mapToGlobal(event))
        if action2 is not None :
            parent = self.menuTree.currentItem()
            childItem = QTreeWidgetItem()
            isFolder = self.isFolder(self.getRowOfItem(parent))
            #폴더가 아닌 파일은 자식 아이템을 만들수 없다.
            
            self.changableState = False

            if action2 == clickmenu_addfile:
                if not isFolder: return
                self.addChildItemToParent(parent, None, False)
                
            elif action2 == clickmenu_addfolder:
                if not isFolder: return
                self.addChildItemToParent(parent, None, True)

            elif action2 == clickmenu_delete:
                deleteItem = self.menuTree.currentItem()
                self.deleteItemFromParent(deleteItem)
                
    def moveSelectItemToTargetItem(self, targetItem, selectedItem):
        targetItemIndexOfParent, selectedItemIndexOfParent, targetItemParent, selectedItemParent= None,None,None,None
        
        if targetItem.parent() is None:
            targetItemParent = self.menuTree.invisibleRootItem()
            targetItemIndexOfParent = targetItemParent.indexOfChild(targetItem)
        else: 
            targetItemParent = targetItem.parent()
            targetItemIndexOfParent = targetItemParent.indexOfChild(targetItem)
            
        if selectedItem.parent() is None:
            selectedItemParent = self.menuTree.invisibleRootItem()
            selectedItemIndexOfParent = selectedItemParent.indexOfChild(selectedItem) 
        else: 
            selectedItemParent = selectedItem.parent()
            selectedItemIndexOfParent=selectedItemParent.indexOfChild(selectedItem)
        
        targetItemIndexOfTree = self.getRowOfItem(targetItem)
        selectedItemIndexOfTree = self.getRowOfItem(selectedItem)

        targetItemChildrenCount = self.getChildrenItemCount(targetItem, [])
        selectedItemChildrenCount = self.getChildrenItemCount(selectedItem,[])

        #itemArray 와 save_data 를 초기화하기 위함
        selectedChildren = self.itemArray[selectedItemIndexOfTree : selectedItemIndexOfTree+selectedItemChildrenCount+1]
        selectedChildren_save_data = self.save_data[selectedItemIndexOfTree : selectedItemIndexOfTree+selectedItemChildrenCount+1]

        if self.isFolder(targetItemIndexOfTree) : 
            targetItem.addChild(selectedItemParent.takeChild(selectedItemIndexOfParent))
            #selected 가 target의 자식이면 target의 맨 마지막 자식 뒤에 붙는다.

            for i in range(len(selectedChildren)):
                insertIndex = targetItemIndexOfTree+targetItemChildrenCount
                if selectedItemIndexOfTree>targetItemIndexOfTree:
                    if selectedItemIndexOfTree <= targetItemIndexOfTree + targetItemChildrenCount : #sel이 tar의 자식이면
                        self.itemArray.insert(insertIndex, self.itemArray.pop(selectedItemIndexOfTree))
                        self.save_data.insert(insertIndex, self.save_data.pop(selectedItemIndexOfTree))
                        self.makeDosiCbToItem(insertIndex)
                        if not self.isFolder(insertIndex):
                            self.makeScrCbToItem(insertIndex)
                    else:
                        insertIndex += (i+1)
                        self.itemArray.insert(insertIndex, self.itemArray.pop(selectedItemIndexOfTree+i))
                        self.save_data.insert(insertIndex, self.save_data.pop(selectedItemIndexOfTree+i))
                        self.makeDosiCbToItem(insertIndex)
                        if not self.isFolder(insertIndex):
                            self.makeScrCbToItem(insertIndex)
                        
                else:
                    self.itemArray.insert(insertIndex, self.itemArray.pop(selectedItemIndexOfTree))
                    self.save_data.insert(insertIndex, self.save_data.pop(selectedItemIndexOfTree))
                    self.makeDosiCbToItem(insertIndex)
                    if not self.isFolder(insertIndex):
                        self.makeScrCbToItem(insertIndex)


                self.resetLevelOfSaveData(insertIndex, targetItemIndexOfTree, True)

        else: 
            #같은 폴더에 있는 경우 요소가 takechild 가 먼저 되기 때문에 indexing에 오류가 생김. selected가 target 보다 index가 먼저이면 target의 index가 -1됨.
            if selectedItemIndexOfParent< targetItemIndexOfParent : 
                if selectedItemParent == targetItemParent:
                    targetItemIndexOfParent -=1
            #targetItem 이 폴더가 아니라면 같은 레벨로 이동한다.
            targetItemParent.insertChild(targetItemIndexOfParent,selectedItemParent.takeChild(selectedItemIndexOfParent))

            for i in range(len(selectedChildren)):
                insertIndex = targetItemIndexOfTree+i
                if selectedItemIndexOfTree>targetItemIndexOfTree:
                    self.itemArray.insert(insertIndex, self.itemArray.pop(selectedItemIndexOfTree+i))
                    self.save_data.insert(insertIndex, self.save_data.pop(selectedItemIndexOfTree+i))
                    self.makeDosiCbToItem(insertIndex)

                    if not self.isFolder(insertIndex):
                        self.makeScrCbToItem(insertIndex)
                else:
                    insertIndex = targetItemIndexOfTree-1
                    self.itemArray.insert(insertIndex, self.itemArray.pop(selectedItemIndexOfTree))
                    self.save_data.insert(insertIndex, self.save_data.pop(selectedItemIndexOfTree))
                    self.makeDosiCbToItem(insertIndex)
                    if not self.isFolder(insertIndex):
                        self.makeScrCbToItem(insertIndex)

       # self.statusLabel.setText(self.getMenuData())

    # case 1
    # sel : 3, children : 4
    # target : 1
    # -> sel: 2, children : 3

    # case 2
    # sel : 1, children : 2
    # target : 5
    # -> sel: 6, children : 7

    # folder : target+1
    # children : target-sel + 1

    # sel : 2, children : 3
    # target 1, 
    # ->sel : 1, children : 2
    # file : target
    # children : target - sel
    def resetLevelOfSaveData(self, insertIdx, targetIdx, isFolder):
        parentLevel = int(self.save_data[self.getRowOfItem(self.itemArray[insertIdx].parent())][0])
        self.save_data[insertIdx][0] = str(parentLevel+1)

    def makeDosiCbToItem(self,idxOfItem):
        dosi = self.makedosiCombo("예")
        self.menuTree.setItemWidget(self.itemArray[idxOfItem], 1, dosi)

    def makeScrCbToItem(self,idxOfItem):
        scrGubunCb = self.makeScrGubunCombo(0)
        scrGubunCb.currentIndexChanged.connect(self.on_combobox_changed_scrGubun)
        self.menuTree.setItemWidget(self.itemArray[idxOfItem], 4, scrGubunCb)

    def addChildItemToParent(self, targetItem, childItem, isTargetFolder):
        childItem = QTreeWidgetItem()
        default_dosi = '1100'
        targetItemRow = self.getRowOfItem(targetItem)
        if isTargetFolder == False:
            #화면구분 콤보박스
            scrGubunCb = self.makeScrGubunCombo(0)
            scrGubunCb.currentIndexChanged.connect(self.on_combobox_changed_scrGubun)
            default_dosi= '0100'
            childItem.setExpanded(False)

        #부모 아이템에 붙인다
        targetItem.insertChild(targetItem.childCount(), childItem)
        childItem.setFlags(childItem.flags() | QtCore.Qt.ItemIsEditable)
        
        if isTargetFolder == False : self.menuTree.setItemWidget(childItem, 4, scrGubunCb)
        else:
            self.setIconToItem(childItem)

        childItem.setText(6, "버튼이름")
        childItem.setText(7, "Z")
        childItem.setData(1, Qt.UserRole, int(targetItem.data(1, Qt.UserRole))+1)

        dosi = self.makedosiCombo("예")
        self.menuTree.setItemWidget(childItem, 1, dosi)

        #포커스를 새로 만들어진 아이템으로 이동한다.
        self.menuTree.scrollToItem(childItem)
        childItem.setSelected(True)

        #원본 데이터 배열에 끼워넣는다.
        #예시 
        # ['3', '0100', '00001', '     ', '                                        ', '버튼이름', 'Z                   ', '표준메뉴                                                    ', '01']
        self.save_data.insert(targetItemRow+self.getChildrenItemCount(targetItem,[]), [
            #부모 아이템의 레벨에 따라 레벨이 정해짐
            str(int(targetItem.data(1, Qt.UserRole))+1),
            default_dosi,
            '00000',
            '     ',
            '                                        ',
            '버튼이름',
            'Z                   ',
            '                                                            ',
            '                    '
        ])
        self.itemArray.insert(targetItemRow+self.getChildrenItemCount(targetItem,[]),childItem)
        #self.statusLabel.setText(self.getMenuData())
        
        

    def deleteItemFromParent(self, deleteItem):
        row = self.getRowOfItem(deleteItem)
        #save data 배열에서도 제거
        #folder 가 제거되면 하위 아이템도 다 제거해야한다.
        delCount = 1 + self.getChildrenItemCount(deleteItem, [])

        for i in range(delCount):
            del self.save_data[row]
            del self.itemArray[row]

        #deleteItem이 부모이면 self.menuTree 에서 부모를 지워줘야 한다.
        if deleteItem.parent() is None : 
            self.menuTree.takeTopLevelItem(self.menuTree.currentIndex().row())
        else: deleteItem.parent().removeChild(deleteItem)


    #item 의 하위 아이템 개수를 총합해주는 DFS 함수
    def getChildrenItemCount(self,node,child_count = []):
        child_count.append(node.childCount())
        if node.childCount() > 0:
            children = []
            for i in range(node.childCount()): children.append(node.child(i))
            for child in children:
                self.getChildrenItemCount(child, child_count)

        return sum(child_count)
    # def getLastChildItem(self, parent):
    #     return self.

    def isFolder(self, row):
        if self.save_data[row][1][:2] in ['11','10']: 
            return True
        else : return False

    def treeItemChanged(self,item,column):
        if self.changableState == False :return
        else:
            row = self.getRowOfItem(item)
            if self.isFolder(row) and column in [3,4,5]: 
                self.menuTree.currentItem().setText(column, "")
                return
            text = item.text(column)
            column_map = {0:7, 2: 2, 3:3, 5:4, 6:5, 7:6, 8:8}  #원본 데이터와 트리 컬럼 순서가 다르다.
            original_data = self.save_data[row][column_map[column]]
            #바꿀 내용이 없다면 return, 길이가 원본보다 크다면
            if self.before_changed_Item == text:
                return
            if len(text)>len(original_data): 
                QMessageBox.about(self,'MessageBox','정해진 길이를 초과합니다.')
                self.menuTree.currentItem().setText(column, self.before_changed_Item)
                return
            #원본 데이터의 길이만큼 바꿀단어와 공백으로 채워줘야 함.
            for i in range(len(text.encode('cp949')), len(original_data.encode('cp949'))):
                text += " "
            
            self.save_data[row][column_map[column]] = text
            #self.statusLabel.setText(self.getMenuData())

            
    def itemDoubleClicked(self,item, column):
        self.before_changed_Item = item.text(column)
        self.changableState = True
    
    def on_combobox_changed_dosi(self):
        combo = self.sender()
        row = self.getRowOfItem(self.menuTree.currentItem())
        changedText = combo.currentText()
        #combobox 가 있는 컬럼 1, 7 : 이 두개가 합쳐져서 한 코드 값을 만들기 때문에 하나만 바껴도 두개의 콤보박스 값을 조회해야 함. 하지만 dosi 값이 11, 10 은 폴더이기 때문에 뒤는 00
        if self.isFolder(row):
            if changedText == "예" :
                dosi = "11" 
            else : dosi = "10"
        else:
            if changedText == "예":
                dosi = "01"
            else : dosi = "00"
        
        self.save_data[row][1] = dosi + self.save_data[row][1][-2:]
    
    def on_combobox_changed_scrGubun(self):
        combo = self.sender()
        row = self.getRowOfItem(self.menuTree.currentItem())
        changedText = combo.currentText()
         
        for i in self.scrGubun_map:
            if self.scrGubun_map[i] == changedText:
                scrGubunCode = i
                break
        
        self.save_data[row][1] = self.save_data[row][1][:2] + scrGubunCode

    def makeTree(self,ndata):
        self.splited_data = ndata.split("\n")
        #데이터 초기화
        self.save_data = []
        self.itemArray = []
        #헤더( 2개 행) 은 고정된 값이므로
        self.save_data.append(self.splited_data[0])
        self.save_data.append(self.splited_data[1])
        self.itemArray.append(self.splited_data[0])
        self.itemArray.append(self.splited_data[1])
        root = self.menuTree.invisibleRootItem()
        for i in range(2 , len(self.splited_data)):
            data = self.preprocessData(self.splited_data[i])
            if len(data[0])==0 : continue
            self.save_data.append(data)
            level = data[0]
            
            self.scrGubun_map= {'00' : '일반화면', '01' : '종합화면', '02' : '웹화면', '03' : 'DLL화면','04':'Exe화면','05':'Function','06':'팝업화면', '07':'단독화면'}
            scrGubun = self.scrGubun_map[str(data[1][2:4])] if data[1]!='1100' else ""
            scrNum = data[2] if len(data[2].replace(" ",""))!=0 else ""
            topScr = data[3] if len(data[3].replace(" ",""))!=0 else ""
            fileName = data[4].rstrip() if len(data[4].replace(" ",""))!=0 else ""
            btnName = data[5] if len(data[5].replace(" ",""))!=0 else ""
            grade = data[6].rstrip() if len(data[6].replace(" ",""))!=0 else ""
            scrName = data[7].rstrip() if len(data[7].replace(" ",""))!=0 else ""
            menuGubun = data[8].rstrip() if len(data[8].replace(" ",""))!=0 else ""
            
            self.dosi_map = {"01": "예", "00": "아니오", "10": "아니오", "11":"예"}
            dosi = self.makedosiCombo(self.dosi_map[str(data[1][0:2])])

            if level == '1' :
                item1 = QTreeWidgetItem(root)
                item1.setFlags(item1.flags() | QtCore.Qt.ItemIsEditable)
                self.setIconToItem(item1)
                item1.setText(0, scrName)
                item1.setText(2, scrNum)
                item1.setText(3, topScr)
                #item1.setText(4, scrGubun) depth 가 1일때는 화면구분을 적지않음
                item1.setText(5, fileName)
                item1.setText(6, btnName)
                item1.setText(7, grade)
                item1.setText(8, menuGubun)
                item1.setData(1, Qt.UserRole, level)
                self.menuTree.setItemWidget(item1, 1, dosi)
                self.itemArray.append(item1)

                
            elif level >= '2' :
                parent = locals()['item{}'.format(int(level)-1)]
                child = locals()['item{}'.format(level)] = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | QtCore.Qt.ItemIsEditable)
                child.setData(1, Qt.UserRole, level)
                #dosi.currentIndexChanged.connect(lambda : self.on_combobox_changed(child))
                self.menuTree.setItemWidget(child, 1, dosi)
                self.addChildToParent(child, parent, data)

        self.changableState = True
        #self.statusLabel.setText(self.getMenuData())

    def preprocessData(self, splited_data):
        splited_data = splited_data.encode('cp949')
        nSplited_data = []
        nSplited_data.append(splited_data[0:1].decode('cp949')) #레벨 : 1
        nSplited_data.append(splited_data[2:6].decode('cp949'))#화면구분 및 도시여부: 4 (앞 두자리 00 : "아니오", 01 : "예", 뒷 두자리 00 : 일반화면, 01 : 종합화면, 02: 웹화면, 03 :DLL화면, 04 : Exe화면, 05: Function, 06: 팝업화면, 07: 단독화면)
        nSplited_data.append(splited_data[7:12].decode('cp949'))#화면번호 : 5_뒤에서부터 read
        nSplited_data.append(splited_data[13:18].decode('cp949'))#상위화면 : 5(5)
        nSplited_data.append(splited_data[19:59].decode('cp949'))#파일명 : 40(40)
        nSplited_data.append(splited_data[60:68].decode('cp949'))#버튼이름 : 4(8)
        nSplited_data.append(splited_data[69:89].decode('cp949'))#등급 : 20(20) (0123456789ABCDEFGXYZ)
        nSplited_data.append(splited_data[90:150].decode('cp949'))#화면이름 : 60
        nSplited_data.append(splited_data[151:171].decode('cp949'))#메뉴구분 : 20(20)
        return nSplited_data
        
        
    def addChildToParent(self, child, parent, data):
        #화면구분은 combobox
        if data[1][:2] not in ['11','10']:
            scrGubunCb = self.makeScrGubunCombo(data[1][2:4])
            child.setExpanded(False)
            
        else : 
            scrGubunCb = QLabel("")
            self.setIconToItem(child)

        scrNum = data[2] if len(data[2].replace(" ",""))!=0 else ""
        topScr = data[3] if len(data[3].replace(" ",""))!=0 else ""
        fileName = data[4].rstrip() if len(data[4].replace(" ",""))!=0 else ""
        btnName = data[5] if len(data[5].replace(" ",""))!=0 else ""
        grade = data[6].rstrip() if len(data[6].replace(" ",""))!=0 else ""
        scrName = data[7].rstrip() if len(data[7].replace(" ",""))!=0 else ""
        menuGubun = data[8].rstrip() if len(data[8].replace(" ",""))!=0 else ""
        child.setText(0, scrName)
        child.setText(2, scrNum)
        child.setText(3, topScr)
        child.setText(5, fileName)
        child.setText(6, btnName)
        child.setText(7, grade)
        child.setText(8, menuGubun)
        parent.addChild(child)
        self.menuTree.setItemWidget(child, 4, scrGubunCb)
        self.itemArray.append(child)
        if data[1]!='1100' : scrGubunCb.currentIndexChanged.connect(self.on_combobox_changed_scrGubun)

    def saveBtnClicked(self):
        if self.fileName is not None:
            file = open(self.fileName, 'w')
            text = self.getMenuData()
            file.write(text)
            file.close()
    def saveAsBtnClicked(self):
        fname = QFileDialog.getSaveFileName(self, 'Save File')
        if fname[0] :
            file = open(fname[0], 'w')
            text = self.getMenuData()
            file.write(text)
            file.close()

    def getMenuData(self):
        result = []
        result.append(self.save_data[0])
        result.append(self.save_data[1])
        for i in range(2,len(self.save_data)):
            result.append(" ".join(self.save_data[i])+ " |")
        
        join_str = "\n".join(result)
        return join_str

    def makeScrGubunCombo(self, currentindex):
        scrGubunCb = QComboBox()
        scrGubunCb.setStyleSheet("QComboBox{background-color : transparent;}")
        scrGubunValues = list(self.scrGubun_map.values())
        scrGubunCb.addItems(scrGubunValues)
        scrGubunCb.setCurrentIndex(int(currentindex))
        scrGubunCb.wheelEvent = lambda event : None
        return scrGubunCb

    def makedosiCombo(self, currenttext):
        dosi = QComboBox(self)
        dosi.addItems(['예','아니오'])
        dosi.setCurrentText(currenttext)
        dosi.setStyleSheet("QComboBox{background-color : transparent;}")
        dosi.activated.connect(self.on_combobox_changed_dosi)
        #마우스 휠 이벤트 방지
        dosi.wheelEvent = lambda event : None
        return dosi
    
    def setIconToItem(self,item):
        icon = QIcon('assets/folderIcon.png'.format("file_important"))
        item.setIcon(0, icon)