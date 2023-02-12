import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import numpy as np
from skimage import morphology
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class picture(QWidget):
    def __init__(self):
        super(picture, self).__init__()

        self.resize(2600, 1000)
        self.setWindowTitle("初始操作")

        self.label = QLabel(self)
        self.label.setText("   初始图片")
        self.label.setFixedSize(1200, 450)
        self.label.move(300, 40)

        self.label.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:30px;font-weight:bold;font-family:宋体;}"
                                 )
        self.label2 = QLabel(self)
        self.label2.setText("   处理图片")
        self.label2.setFixedSize(1200, 450)
        self.label2.move(300, 510)

        self.label2.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:30px;font-weight:bold;font-family:宋体;}"
                                 )
        btn = QPushButton(self)
        btn.setText("打开图片")
        btn.move(10, 30)
        btn.clicked.connect(self.openimage)

    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)

        original = cv2.imread(imgName, 0)
        ret, binary = cv2.threshold(original, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        # 腐蚀和膨胀
        kernel = np.ones((5, 5), np.uint8)
        dilation1 = cv2.dilate(binary, kernel, iterations=1)

        kernel = np.ones((16, 16), np.uint8)
        erosion = cv2.erode(dilation1, kernel, iterations=1)

        kernel = np.ones((31, 31), np.uint8)
        dilation2 = cv2.dilate(erosion, kernel, iterations=1)

        anded = cv2.bitwise_and(dilation2, binary, dst=None, mask=None)

        kernel = np.ones((10, 10), np.uint8)

        kernel = np.ones((2, 2), np.uint8)
        dilation3 = cv2.dilate(anded, kernel, iterations=1)

        # 中值滤波
        median = cv2.medianBlur(dilation3, 5)

        kernel = np.ones((2, 2), np.uint8)
        dilation4 = cv2.dilate(median, kernel, iterations=1)

        # 图片做差
        sub1 = cv2.subtract(binary, dilation4, dst=None, mask=None)

        # 闭运算
        kernel = np.ones((5, 5), np.uint8)
        closing = cv2.morphologyEx(sub1, cv2.MORPH_CLOSE, kernel)

        # 骨骼化
        # clo = cv2.cvtColor(closing, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(closing, 127, 255, cv2.THRESH_BINARY)
        binary[binary == 255] = 1
        skeleton0 = morphology.skeletonize(binary)
        skeleton = skeleton0.astype(np.uint8) * 255
        imgPath = os.path.dirname(imgName) + r'\result.tif'
        cv2.imwrite(imgPath, skeleton)
        pix = QPixmap(imgPath).scaled(self.label.width(), self.label.height())
        self.label2.setPixmap(pix)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = picture()
    my.show()
    sys.exit(app.exec_())