import numpy as np
import cv2

canvas = np.zeros((24000,32768), dtype=np.uint8)
cv2.imwrite("canvas.jpg",canvas)