#sharpen some images:

import cv2
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

BIN_image = cv2.imread("resized_depthview_hot.jpg")
RGB_image = cv2.imread("image_1721277769_resized.jpg")

plt.subplot(1,2,1)
plt.title("Original")
plt.imshow(RGB_image)

kernel = np.array([[-1,-1,-1], [-1,5,-1], [-1,-1,-1]])

filtered_image = cv2.medianBlur(RGB_image, 11)
for i in range(2):
    filtered_image = cv2.medianBlur(filtered_image,11)

cv2.imwrite('resized_RGB_smoothed.jpg', filtered_image)

plt.subplot(1,2,2)
plt.title("filtering")
plt.imshow(filtered_image)
plt.show()
