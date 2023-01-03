import argparse
import os
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2,40).__str__()
import cv2
import math
import json
import numpy as np
import time
from multiprocessing import Pool


parser = argparse.ArgumentParser(description='test')
parser.add_argument('--fps',default="6000",type=int,help = "None")
parser.add_argument('--fps_real',default="600",type=int,help = "None")
parser.add_argument('--start',default="0",type=int,help = "None")
parser.add_argument('--color',default="yellow",type=str,help = "None")

args = parser.parse_args()


frame = args.fps#渲染帧率
real_frame = args.fps_real #输出帧率
params = []
w,h = [32768,24000] #原始画布大小 偶数 单位：像素
n1 = 0.2 #输出压缩率

x1,y1 = [0,0] #平移
w1,h1 = [3276,2400]#缩放图像分辨率

img4 = np.zeros((h1, w1,3), dtype=np.uint8)
img = cv2.imread("frames/canvas.jpg")

n = 10#成像放大率
cores = 2

count = args.start

with open("params.json",mode="r") as f:
    params = json.load(f)


def transform():#-3 -2 -1 0 1 2 3变换为0 1 -1 2 -2 3 -3
    orded_params = []
    for i in range(0,int((params.__len__()-1)/2+1)):
        orded_params.append(params[i + int((params.__len__() - 1) / 2)]) if i != 0 else orded_params.append(params[int((params.__len__()-1)/2)])
        orded_params.append(params[int((params.__len__() - 1) / 2) - i]) if i != 0 else None
    return orded_params
def relative_point(param,t):
    point_ = []
    for i in param:
        point_.append([math.floor(math.cos(i[0]+t*i[2]*2*math.pi)*i[1]),math.floor(math.sin(i[0]+t*i[2]*2*math.pi)*i[1]),i[1]])
    return point_
def absolute_point(param):
    #total_x = w/2
    #total_y = h/2
    total_x = x1
    total_y = y1
    point_ = []
    point_.append([total_x, total_y,param[0][2]])
    for i in range(0,param.__len__()-1):
        total_x += param[i][0] * n1#缩放
        total_y += param[i][1] * n1#缩放
        point_.append([total_x,total_y,math.fabs(param[i+1][2]*n1)])
    return point_
def scaled_point(param):

    total_x = w1/2
    total_y = h1/2
    point_ = []
    point_.append([total_x, total_y, 0])
    for i in range(param.__len__()-1,0,-1):
        if i != 0 and (param[i - 1][0] > 0 or param[i - 1][0] < w1) and (param[i - 1][1] > 0 or param[i - 1][1] < h1):
            total_x -= param[i][0] * n
            total_y -= param[i][1] * n
            point_.append([total_x,total_y,math.fabs(param[i][2] * n)])
    return point_
def scaled_line(i):
    loss_x = points[i-1][points[i-1].__len__()-1][0] * n - w1 / 2
    loss_y = points[i-1][points[i-1].__len__()-1][1] * n - h1 / 2
    point_ = []
    for j in range(1,i+1):
        a_x,a_y = [points[j-1][points[j-1].__len__()-1][0] * n - loss_x,points[j-1][points[j-1].__len__()-1][1] * n - loss_y]
        try:
            b_x,b_y = (points[j][points[j].__len__()-1][0] * n - loss_x,points[j][points[j].__len__()-1][1] * n - loss_y)
        except:
            b_x,b_y = [points[j-1][points[j-1].__len__()-1][0] * n - loss_x,points[j-1][points[j-1].__len__()-1][1] * n - loss_y]
        if (a_x > 0 or b_x > 0) and (a_y > 0 or b_y > 0) and (a_x < w1 or b_x < w1) and (a_y < h1 or b_y < h1):
            point_.append([a_x,a_y])
    return point_
def main_draw(i):

    count1 = count + i
    img2 = img.copy()
    img3 = img4.copy()
    for j in range(i+1,1,-1):
        point = points[j-1]
        try:
            cv2.line(img2, (p_x, p_y), (int(point[point.__len__() - 1][0]), int(point[point.__len__() - 1][1])),(0, 255, 255), thickness=7) if args.color == 'yellow' else cv2.line(img2, (p_x, p_y), (int(point[point.__len__() - 1][0]), int(point[point.__len__() - 1][1])), (0, 0, 255), thickness=7)
        except:
            None
        p_x, p_y = [int(point[point.__len__() - 1][0]), int(point[point.__len__() - 1][1])]
    if i == frame:
        print("ended")
        cv2.imwrite("frames/canvas.jpg",img2)
    point = points[i-1]
    point1 = points1[i-1]
    point2 = points2[i-1]
    for j in range(0, point.__len__() - 1):
        cv2.arrowedLine(img2, (int(point[j][0]), int(point[j][1])), (int(point[j + 1][0]), int(point[j + 1][1])),(255, 255, 255), thickness=8) if j <= 2 else cv2.arrowedLine(img2, (int(point[j][0]), int(point[j][1])), (int(point[j + 1][0]), int(point[j + 1][1])), (255, 255, 255),thickness=2)
        try:
            cv2.circle(img2, (int(point[j][0]), int(point[j][1])), int(point[j][2]), (169, 169, 169),thickness=1)
        except:
            None
    for j in range(0,point1.__len__()-1):
        cv2.arrowedLine(img3,(int(point1[j+1][0]),int(point1[j+1][1])),(int(point1[j][0]),int(point1[j][1])),(255,255,255),thickness = 4)
        try:
            cv2.circle(img3,(int(point1[j][0]),int(point1[j][1])),int(point1[j][2]),(169,169,169),thickness=1)
        except:
            None
    for j in range(0, point2.__len__()):
        try:
            cv2.line(img3, (p_x1, p_y1), (int(point2[j][0]), int(point2[j][1])), (0, 255, 255), thickness=10) if args.color == 'yellow' else cv2.line(img3, (int(point2[j][0]), int(point2[j][1])), (p_x1, p_y1), (0, 0, 255), thickness=7)
        except:
            None
        p_x1, p_y1 = [int(point2[j][0]), int(point2[j][1])]
    if count1 % (frame / (real_frame*2)) == 0:
        cv2.imwrite("frames_1/" + str(int(count1/(frame/(real_frame*2)))) + ".jpg", img3)
    if count1 % (frame / real_frame) == 0:
        cv2.imwrite("frames/" + str(int(count1 / (frame / real_frame))) + ".jpg", img2)
    print(i)

points = [absolute_point(relative_point(transform(), (1 / frame) * i)) for i in range(1, frame+1+int(frame/real_frame))]
points1 = [scaled_point(relative_point(transform(), (1 / frame) * i)) for i in range(1, frame+1+int(frame/real_frame))]
points2 = [scaled_line(i) for i in range(1, frame+1 + int(frame/real_frame))]
if __name__ == '__main__':
    p = Pool(cores)
    for i in range(1, frame+1+int(frame/real_frame)):
        p.apply_async(main_draw, args=(i,))
    p.close()
    p.join()
