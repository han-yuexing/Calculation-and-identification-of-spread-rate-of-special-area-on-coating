# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detect.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import cv2
import numpy as np
import ctypes
import os
import time


font = cv2.FONT_HERSHEY_SIMPLEX
imgPath = ''

# 定义信号
class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # 自定义输出
    def write(self, text):
        #if text != '\n':
            #text = time.strftime("[%Y%m%d %H:%M:%S] ", time.localtime()) + text
        self.textWritten.emit(str(text))

class myQGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(myQGraphicsView, self).__init__(*args, **kwargs)
        self.image = None

    def get_img(self,image):
        self.image = image

    def loadImage(self):
        self.scene = QGraphicsScene()  # 创建一个图片元素的对象
        item = QGraphicsPixmapItem(self.image)  # 创建一个变量用于承载加载后的图片
        self.scene.addItem(item)  # 将加载后的图片传递给scene对象
        self.setScene(self.graphicsView.scene)  # 将scene显示在graphicsview中

    def reloadImage(self):
        #self.fitInView(0,0,self.width(),self.height())
        #print(self.items())
        self.image = QPixmap(imgPath).scaled(self.width(), self.height())
        self.scene = QGraphicsScene()  # 创建一个图片元素的对象
        item = QGraphicsPixmapItem(self.image)  # 创建一个变量用于承载加载后的图片
        self.scene.addItem(item)  # 将加载后的图片传递给scene对象
        self.setScene(self.scene)  # 将scene显示在graphicsview中

    def resizeEvent(self, event: QtGui.QResizeEvent):
        self.reloadImage()

class SplatGUI(object):
    def __init__(self):
        # 修改系统的print命令
        sys.stdout = EmittingStream(textWritten=self.outputWritten)
        sys.stderr = EmittingStream(textWritten=self.outputWritten)

    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(351, 250)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setContentsMargins(-1, 9, 9, 9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn1 = QtWidgets.QPushButton(Form)
        self.btn1.setObjectName("btn1")
        self.horizontalLayout.addWidget(self.btn1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn2 = QtWidgets.QPushButton(Form)
        self.btn2.setObjectName("btn2")
        self.horizontalLayout.addWidget(self.btn2)
        # =============================================================================
        #         spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #         self.horizontalLayout.addItem(spacerItem1)
        #         self.btn3 = QtWidgets.QPushButton(Form)
        #         self.btn3.setObjectName("btn3")
        #         self.horizontalLayout.addWidget(self.btn3)
        # =============================================================================
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(Form)
        self.line.setStyleSheet("line\n"
                                "{\n"
                                "    color:rgb(0, 0, 0);\n"
                                "}")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(-1, 30, -1, 60)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.graphicsView = myQGraphicsView(Form)
        self.graphicsView.setObjectName("graphicsView")

        self.horizontalLayout_2.addWidget(self.graphicsView)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_2.addWidget(self.textBrowser)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn1.setText(_translate("Form", "选择图片"))
        self.btn1.clicked.connect(self.openImage)
        self.btn2.setText(_translate("Form", "检测片层"))
        self.btn2.clicked.connect(self.detect)


    def openImage(self):
        #print(222222)
        global imgPath
        imgPath, imgType =QFileDialog.getOpenFileName(None, "打开图片", "", "*.tif;;*.jpg;;*.png;;All Files(*)")
        self.image = QPixmap(imgPath).scaled(self.graphicsView.width(), self.graphicsView.height())
        self.loadImage()


    def loadImage(self):
        self.graphicsView.scene = QGraphicsScene()  # 创建一个图片元素的对象
        item = QGraphicsPixmapItem(self.image)  # 创建一个变量用于承载加载后的图片
        self.graphicsView.scene.addItem(item)  # 将加载后的图片传递给scene对象
        self.graphicsView.setScene(self.graphicsView.scene)  # 将scene显示在graphicsview中
        # self.graphicsView.get_img(self.image)

    def detect(self):
        global imgPath
        self.textBrowser.clear()
        #img = cv2.imread(self.imgPath)
        img = cv2.imdecode(np.fromfile(imgPath, dtype=np.uint8),-1)
        width = img.shape[0]
        length = img.shape[1]
        #orginal = cv2.imread(self.imgPath, 0)
        orginal = cv2.imdecode(np.fromfile(imgPath, dtype=np.uint8),0)
        # =============================================================================
        #         cv2.namedWindow('orginal',0)
        #         cv2.resizeWindow('orginal',640, 480)
        #         cv2.imshow('orginal',orginal)
        # =============================================================================

        # 图像二值化
        # ret,binary=cv2.threshold(orginal,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        ret, binary = cv2.threshold(orginal, 127, 255, cv2.THRESH_BINARY)
        # =============================================================================
        #         cv2.namedWindow("threshold",0)
        #         cv2.resizeWindow("threshold", 640, 480)
        #         cv2.imshow("threshold",binary)
        # =============================================================================

        # 腐蚀和膨胀
        kernel = np.ones((5, 5), np.uint8)
        dilation1 = cv2.dilate(binary, kernel, iterations=1)
        # =============================================================================
        #         cv2.namedWindow("dilation1",0)
        #         cv2.resizeWindow("dilation1", 640, 480)
        #         cv2.imshow("dilation1",dilation1)
        # =============================================================================
        kernel = np.ones((16, 16), np.uint8)
        erosion = cv2.erode(dilation1, kernel, iterations=1)
        # =============================================================================
        #         cv2.namedWindow("Erosion",0)
        #         cv2.resizeWindow("Erosion", 640, 480)
        #         cv2.imshow("Erosion",erosion)
        # =============================================================================

        kernel = np.ones((31, 31), np.uint8)
        dilation2 = cv2.dilate(erosion, kernel, iterations=1)

        # =============================================================================
        #         cv2.namedWindow("dilation",0)
        #         cv2.resizeWindow("dilation", 640, 480)
        #         cv2.imshow("dilation",dilation2)
        # =============================================================================


        anded = cv2.bitwise_and(dilation2, binary, dst=None, mask=None)
        # =============================================================================
        #         cv2.namedWindow("Anded",0)
        #         cv2.resizeWindow("Anded", 640, 480)
        #         cv2.imshow("Anded",anded)
        # =============================================================================

        kernel = np.ones((10, 10), np.uint8)

        kernel = np.ones((2, 2), np.uint8)
        dilation3 = cv2.dilate(anded, kernel, iterations=1)

        # 均值滤波
        median = cv2.medianBlur(dilation3, 5)

        kernel = np.ones((2, 2), np.uint8)
        dilation4 = cv2.dilate(median, kernel, iterations=1)

        # 提取膨胀之后图像的不规则轮廓
        image, contours, hierarchy = cv2.findContours(dilation4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(img, contours, -1, (0, 0, 255), 2)  # 最后一个参数，线宽（-1为填充）

        flag = 0
        for i in range(len(contours)):
            cnt = contours[i]
            c_min = []
            black = generate_black(width, length)
            c_min.append(cnt)
            cv2.drawContours(black, c_min, -1, 255, cv2.FILLED)
            anded2 = cv2.bitwise_and(black, anded, dst=None, mask=None)
            obj_area = len(np.where(anded2 == 255)[0])
            (X, Y), R = cv2.minEnclosingCircle(cnt)
            X = int(X)
            Y = int(Y)
            R = int(R)
            box_area = R ** 2 * np.pi
            if box_area > 200:
                flag = flag + 1
                cv2.circle(img, (X, Y), R, (255, 0, 0), 2)
                img = cv2.putText(img, str(flag), (X, Y), font, 0.8, (0, 0, 0), 2)
                sodility = obj_area / box_area
                print("第", flag, "个区域：")
                print("obj_area", obj_area)
                print("box_area", box_area)
                print("sodility", sodility)
            cv2.imwrite('result.tif', img)

            imgPath = os.path.abspath('') + r'\result.tif'
            self.graphicsView.reloadImage()


def generate_black(width, length):
    # create a black use numpy,size is:512*512
    black = np.zeros((width, length), np.uint8)
    return black


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    desktop = QApplication.desktop()
    MainWindow = QtWidgets.QWidget()
    ui = SplatGUI()
    ui.setupUi(MainWindow)
    #MainWindow.setFixedSize(0.85*desktop.width(), 0.75*desktop.height())
    MainWindow.show()
    sys.exit(app.exec_())
