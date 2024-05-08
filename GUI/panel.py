import json
import math
import os
import sys
import time
from functools import partial

from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QUrl, QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QGridLayout, QTableWidget, QScrollArea, QComboBox
import GUI.Start as Start
from GUI.untitled import Ui_MainWindow

class LocalModels():
    def __init__(self):
        self.local=os.path.join('.\GUI','default.json')
        with open(self.local, 'r') as file:
            self.data = json.load(file)
    def getModelAddress(self,index):
        return self.data["modellist"][index]['modelAddresss']
    def getModelIcon(self,index):
        return self.data["modellist"][index]['modelIcon']
    def getlen(self):
        return len(self.data["modellist"])
class NewWindow(QWidget):
    buttonClicked = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('所有模型')
        self.resize(500, 500)
        modellist = LocalModels()

        widget = QWidget()
        layout = QGridLayout(widget)
        # self.layout = QGridLayout()
        for i in range(modellist.getlen()):
            # 创建一个 QPushButton 实例，并设置其图标
            # print(modellist.getlen())
            row = math.floor(i / 4)
            col = i % 4
            Icon=modellist.getModelIcon(i)
            Address=modellist.getModelAddress(i)
            name=Address.split('/')[0]
            button = QPushButton()
            
            button.clicked.connect(partial(self.buttonClicked.emit, Address))
            # print(f"Connected button {i} to address {Address}")
            button.setFixedSize(QSize(50, 50))
            if Icon=="None":
                button.setText(name)
            else:
                button.setIcon(QIcon(Icon))

            # 将按钮添加到布局中
            layout.addWidget(button, row, col)

        # 设置窗口的布局
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
    # def send(self,address):
    #     self.buttonClicked.emit(str(address))

# class WebEnginePage(QWebEnginePage):
#     def __init__(self, *args, **kwargs):
#         QWebEnginePage.__init__(self, *args, **kwargs)
#         self.featurePermissionRequested.connect(self.onFeaturePermissionRequested)
#
#     # setMediaAccessPermission(QWebEnginePage.MediaAudioCapture, QWebEnginePage.MediaPermissionGranted)
#     # setMediaAccessPermission(QWebEnginePage.MediaVideoCapture, QWebEnginePage.MediaPermissionGranted)
#     def onFeaturePermissionRequested(self, url, feature):
#         if feature in (QWebEnginePage.MediaAudioCapture,
#             QWebEnginePage.MediaVideoCapture,
#             QWebEnginePage.MediaAudioVideoCapture):
#             self.setFeaturePermission(url, feature, QWebEnginePage.PermissionGrantedByUser)
#         else:
#             self.setFeaturePermission(url, feature, QWebEnginePage.PermissionDeniedByUser)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.modellistWin = NewWindow()
        self.modellistWin.buttonClicked.connect(self.SetModel)
        #   --------------- start ---------------------

        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.frame)
        # self.page = WebEnginePage()
        # self.webEngineView.setPage(self.page)
        url = '\GUI\dex.html'
        self.webEngineView.load(QUrl.fromLocalFile(url))
        self.webEngineView.setGeometry(0,0,self.frame.width(),self.frame.height())
        # 设置缩放
        self.webEngineView.setZoomFactor(0.7)

        # print(self.frame.width(), self.frame.height())
        # self.webEngineView.setGeometry(0, 0, 1063, 682)
        # text=self.readJ()
        # # print(text)
        # self.label = QLabel(json.dumps(text, indent=4), self.frame_2)
        
        self.layout2 = QGridLayout(self.frame_2)
        self.layout4 = QGridLayout(self.frame_4)
        self.layout5 = QVBoxLayout(self.frame_5)
        self.layout3 = QVBoxLayout(self.frame_3)

        self.button = QPushButton('面部追随', self.frame_3)
        self.layout3.addWidget(self.button)
        # self.button.clicked.connect(self.on_click)
        self.triggerButton = QPushButton('选择模型', self.frame_3)
        self.triggerButton.clicked.connect(self.modellistWin.show)
        # self.triggerButton.clicked.connect(self.triggerFunction)
        self.layout3.addWidget(self.triggerButton)
        self.frame_3.setLayout(self.layout3)
    # def triggerButton(self):

    def SetModel(self, address):
        self.resetFrame2()
        self.resetFrame5()
        print("here")
        self.webEngineView.page().runJavaScript(f"InitiateModel('{address}');")
        self.setStageModel(address)
        self.readJ(address)
    def setStageModel(self, address):
        default_model = {
            "modelNum": 0,
            "modelAddresss": address
        }
        with open('./GUI/stageModel.json', 'w', encoding='utf-8') as f:
            json_data = json.dumps(default_model, indent=4)
            f.write(json_data)

    def SetElection(self,Mlist,address):
        labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        self.comboBoxes = []
        # print(len(Mlist))
        settingJson=os.path.join('./dist/assets/', address.split('/')[0]+'/settiing.json')
        if len(Mlist)==0:
            self.saveSetting(address,Mlist)
            self.settingLable = QLabel('无Motions')
            self.layout5.addWidget(self.settingLable)
        else:
            for i in range(6):
                label = QLabel(f'{labels[i]}', self)
                comboBox = QComboBox(self)
                # 添加选项到下拉框
                for j in range(len(Mlist)):
                    comboBox.addItem(Mlist[j])
                # comboBox.currentIndexChanged.connect(lambda index, l=label,a=address,I=i: self.on_combobox_changed(index, l, a,I))
                self.comboBoxes.append(comboBox)

                # 将label和下拉框添加到布局
                self.layout5.addWidget(label)
                self.layout5.addWidget(comboBox)


            self.settingButton = QPushButton('保存设置')
            self.settingButton.clicked.connect(lambda index,a=address,m=Mlist: self.saveSetting(a,m))
            self.layout5.addWidget(self.settingButton)
            if os.path.exists(settingJson):
                # 读取 JSON 文件
                with open(settingJson, 'r') as f:
                    data = json.load(f)
                for i in range(5):
                    self.comboBoxes[i].setCurrentText(data["settings"][labels[i]])


    def saveSetting(self, address, Mlist):
        if len(Mlist)>0:
            self.allow="yes"
            settinglist = {
                "Angry": self.comboBoxes[0].currentText(),
                "Disgust": self.comboBoxes[1].currentText(),
                "Fear": self.comboBoxes[2].currentText(),
                "Happy": self.comboBoxes[3].currentText(),
                "Sad": self.comboBoxes[4].currentText(),
                "Surprise": self.comboBoxes[5].currentText(),
                "allow": self.allow
            }
        else:
            self.allow="no"
            settinglist = {
                "Angry": 0,
                "Disgust": 0,
                "Fear": 0,
                "Happy": 0,
                "Sad": 0,
                "Surprise": 0,
                "allow": self.allow
            }
        settingJson=os.path.join('./dist/assets/', address.split('/')[0]+'/settiing.json')
        data = {
            "settings": settinglist
        }
        with open(settingJson, 'w') as f:
        # 使用 json.dump() 函数将数据写入文件
            json.dump(data, f, indent=4)
    def SetMotion(self,group,num):
        # print({group},{num})
        self.webEngineView.page().runJavaScript(f"Motion('{group}','{num}');")
    def SetExp(self,name):
        self.webEngineView.page().runJavaScript(f"Exp('{name}');")

    def resetFrame2(self):
        while self.layout2.count():
            child = self.layout2.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    def resetFrame4(self):
        while self.layout4.count():
            child = self.layout4.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    def resetFrame5(self):
        while self.layout5.count():
            child = self.layout5.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


    def readJ (self,address):
        local=os.path.join(".\dist", "assets", address)
        with open(local, 'r') as file:
            data = json.load(file)
        if "Motions" in data['FileReferences']:
            Mlist=self.traverse_jsonM(data['FileReferences']['Motions'],"情绪动作")
        # if "Expressions" in data['FileReferences']:
        #     Elist=self.traverse_jsonE(data['FileReferences']['Expressions'],"表情动作")
        else:
            Mlist=[]
        self.SetElection(Mlist,address)





    def traverse_jsonM(self,json_data,name):
        # label = QLabel(name)
        # self.layout2.addWidget(label,0,0)
        Mlist=[]
        if isinstance(json_data, dict):
            # valuelist=[]
            row=0
            for key, value in json_data.items():
                col=0
                if isinstance(value, dict) or isinstance(value, list):
                    # print(f"Key: {key}")
                    for index in range(len(value)):
                        button = QPushButton()
                        button.setText(key+":"+str(index))
                        button.clicked.connect(lambda checked, group=key, num=index:self.SetMotion(group,num))
                        Mlist.append(key+":"+str(index))
                        self.layout2.addWidget(button, row, col)
                        col+=1
                        if(col==5):
                            row +=1
                            col=0 
                row +=1       
            self.frame_2.setLayout(self.layout2)
                #     self.traverse_json(value)
                # else:
                #     print(f"Key: {key}, Value: {value}")
        # elif isinstance(json_data, list):
        #     for item in json_data:
        #         self.traverse_jsonM(item,name)
        return Mlist


    # def traverse_jsonE(self,json_data,name):
    #     # label = QLabel(name)
    #     # self.layout2.addWidget(label,0,0)
    #     Elist=[]
    #     if isinstance(json_data, list):
    #         # valuelist=[]
    #         for i in range(len(json_data)):
    #             row = math.floor(i / 4)
    #             col = i % 4
    #             for key, value in json_data[i].items():
    #                 if(key=="Name"):
    #                     button = QPushButton()
    #                     button.setText(value)
    #                     button.clicked.connect(lambda checked, name=value:self.SetExp(name))
    #                     Elist.append(value)
    #                     self.layout4.addWidget(button,row,col)
    #     self.frame_2.setLayout(self.layout2)
    #     return Elist



def start_in_thread2():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    
    FaceWin = Start.MyWidget()
    mainWindow.button.clicked.connect(FaceWin.show)

    sys.exit(app.exec_())

# if __name__ == "__main__":
#     start_in_thread2()
