import json
import math
import matplotlib.pyplot as plt

import argparse


parser = argparse.ArgumentParser(description='test')
parser.add_argument('--t',default="2000000",type=int,help = "None")

args = parser.parse_args()

t = args.t #图像分割的小点数量 精细度

with open("order.json",mode="r") as f:
    _data = json.load(f)

real_point = []



#i[0]:命令
#i[1]:参数
#0:命令 1:参数 2:起点 3:分割点

def line(t1,order,start_point):#描直线线上的点
    #print("sb")
    x1,y1=[float(order.split(",")[0]),float(order.split(",")[1])]
    x2,y2=[float(start_point.split(",")[0]),float(start_point.split(",")[1])]
    x3 = [x2-(x2-x1)/(t1+2)*i for i in range(1,t1+1)]
    y3 = [y2-(y2-y1)/(t1+2)*i for i in range(1,t1+1)]
    return (x3,y3)

def bezier(t1,order,start_point):#描贝塞尔曲线上的点
    x1,y1 = [float(start_point.split(",")[0]),float(start_point.split(",")[1])]
    x2,y2 = [float(order.split(" ")[0].split(",")[0]),float(order.split(" ")[0].split(",")[1])]
    x3, y3 = [float(order.split(" ")[1].split(",")[0]),float(order.split(" ")[1].split(",")[1])]
    x4, y4 = [float(order.split(" ")[2].split(",")[0]),float(order.split(" ")[2].split(",")[1])]
    x5 = [x1*(1-(1/t1)*i) ** 3 + 3 * x2 * (1/t1)*i * (1-(1/t1)*i) ** 2 + 3 * x3 * (((1/t1)*i)**2)*(1-(1/t1)*i) + x4 * (((1/t1)*i) ** 3) for i in range(1,t1+1)] #P0(1-t)^3+3P1t(1-t)^2+3P2t^2(1-t)+P3t^3
    y5 = [y1*(1-(1/t1)*i) ** 3 + 3 * y2 * (1/t1)*i * (1-(1/t1)*i) ** 2 + 3 * y3 * (((1/t1)*i)**2)*(1-(1/t1)*i) + y4 * (((1/t1)*i) ** 3) for i in range(1,t1+1)]
    return x5,y5

def real_count():
    global count
    count = 0

    for i in _data:
        if i[0] != 'z' and i[0] != 'm' and i[0]!='M':
            count += 1
            try:
                real_point.append([i[0],i[1],i[3]])
            except:
                print(i[0])
    return count

def add_time():
    per_time = math.floor(t / real_count())
    for i in range(0,count):
        add = per_time+1 if i<t-(per_time*count) else per_time
        real_point[i].append(add)
    #print(real_point)

def show_point():
    plt.title("double number", fontsize=24)
    plt.xlabel("x", fontsize=14)
    plt.ylabel("y", fontsize=14)

    plt.axis([-600000, 600000, -600000,600000 ])

    for i in f:
        plt.scatter(i[0], i[1], s=10)
    plt.show()

def output_():
    global f
    f = []  # f(t)
    for i in real_point:
        if i[0] == 'l':
            x,y = line(i[3],i[1],i[2])
            for j in range(0,i[3]):
                f.append([x[j],y[j]])#沿x轴翻折

        if i[0] == 'c':
            x, y = bezier(i[3], i[1], i[2])
            for j in range(0, i[3]):
                f.append([x[j], y[j]])#沿x轴翻折
    return f

add_time()
#output_()
with open("f(x).json",mode="w") as f:
    f.write(json.dumps(output_(),indent=4))
#show_point()
