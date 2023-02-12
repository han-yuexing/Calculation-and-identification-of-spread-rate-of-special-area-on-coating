import cv2
import numpy as np
from skimage import morphology
import numpy as np

# 图像二值化
original = cv2.imread('3.tif', 0)
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

cv2.imwrite("skeleton3.tif", skeleton)
cv2.imshow("X", skeleton)
cv2.waitKey()
cv2.destroyAllWindows()