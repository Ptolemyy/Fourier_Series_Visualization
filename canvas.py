import numpy as np
import cv2

canvas = np.zeros((4800,6554), dtype=np.uint8)
cv2.imwrite("canvas.jpg",canvas)