import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView,QWebEnginePage
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from pyqt5_plugins.examplebutton import QtWidgets
from pyqt5_plugins.examplebuttonplugin import QtGui


class WebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        QWebEnginePage.__init__(self, *args, **kwargs)
        self.featurePermissionRequested.connect(self.onFeaturePermissionRequested)

    def onFeaturePermissionRequested(self, url, feature):
        if feature in (QWebEnginePage.MediaAudioCapture,
            QWebEnginePage.MediaVideoCapture,
            QWebEnginePage.MediaAudioVideoCapture):
            self.setFeaturePermission(url, feature, QWebEnginePage.PermissionGrantedByUser)
        else:
            self.setFeaturePermission(url, feature, QWebEnginePage.PermissionDeniedByUser)

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # self.setMouseTracking(True)
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏窗口边框
        # self.flag=False
        self.setGeometry(100, 100, 800, 800)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setStyleSheet("background:transparent")
        self.web_view = QWebEngineView()
        self.page=WebEnginePage()
        self.page.setBackgroundColor(Qt.transparent)
        self.web_view.setPage(self.page)
        self.web_view.load(QUrl("http://127.0.0.1:4800"))
        # self.web_view.load(QUrl("http://192.168.0.104:4800"))
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        self.setLayout(layout)

        # self.label = QLabel("这是一个标签", self)
        # self.label.setMouseTracking(True)
        # self.label.hide()
        # # 创建一个 QVBoxLayout 来垂直放置 QLabel 和 QWebEngineView
        # layout = QVBoxLayout()
        # layout.addWidget(self.label)
        # layout.addWidget(self.web_view)

        # # 创建一个 QWidget 并设置布局
        # main_widget = QWidget()
        # main_widget.setLayout(layout)

        # # 设置主窗口中的中心部件
        # self.setCentralWidget(main_widget)


    # def mouseMoveEvent(self, event):
    #     mouse_y = event.y()
    #     window_top = self.geometry().top()
    #     diff = mouse_y - window_top
    #     print(f"Mouse Y: {mouse_y}, Difference from top: {diff}")
    #     if mouse_y<15:
    #         self.setWindowFlags(Qt.Window)
    #         self.flag=True
    #         self.show()
    #
    #     elif self.flag is True :
    #         self.setWindowFlags(Qt.FramelessWindowHint)
    #         self.flag=False
    #         self.show()

def main():
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()