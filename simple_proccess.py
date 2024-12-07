import xml.etree.ElementTree as ET
import argparse
import math
import matplotlib.pyplot as plt
from multiprocessing import Pool

parser = argparse.ArgumentParser(description='test')
parser.add_argument('--path',type=str,help = "None")
parser.add_argument('--t1',default="200",type=int,help = "None")
parser.add_argument('--t',default="2000000",type=int,help = "None")
args = parser.parse_args()




tree = ET.parse(args.path)
root = tree.getroot()

_data = str(root[1][1][0].attrib['d'])

t = args.t #图像分割的小点数量 精细度
real_point = []
#i[0]:命令
#i[1]:参数
#0:命令 1:参数 2:起点 3:分割点


t1 = args.t1 #实际项数为(2*t1)+1
n = 0.0625 #放大率

#print(data)

def _split(__data):
    list_data = list(__data)
    data = ""
    for i in list_data:         #分段
            if str(i).isalpha() == True:
                data += "|"
            data+=str(i)
    return data.split("|")

def transform():
    output = []
    total_x, total_y = [0, 0]
    melt = _split(_data)

    raw = ''
    for i in melt: #将l0 100 200 300化成l0 100 l200 300
        if ''.join(filter(str.isalpha,i)) == 'l':
            n = 0
            for j in i.split(" "):
                if n == 2:
                    raw += "l"
                    n = 0
                n += 1
                raw+=j+' '
        elif ''.join(filter(str.isalpha, i)) == 'c':
            n = 0
            for j in i.split(" "):
                if n == 3:
                    raw += "c"
                    n = 0
                n += 1
                raw += j + ' '
        else:
            raw += i
    melt = _split(raw)
    for i in melt:
        i = ''.join(list(i)[j] for j in range(0,list(i).__len__()-1)) if i != 'z' else i
        aplha_i = ''.join(filter(str.isalpha,i))
        num_i = (i.replace(aplha_i,"")).replace(" ",",") if aplha_i == 'l' or aplha_i == 'M' or aplha_i == 'z' or aplha_i == 'm' else i.replace(aplha_i,"")
        output.append([aplha_i, num_i]) if aplha_i != '' else None #去除空项

    #绝对坐标变换和起点坐标
    for i in range(0,output.__len__()):

        try:
            new_list = []
            for j in range(0,output[i][1].split(" ").__len__()):
                new_list += str(round(float(output[i-1][1].split(" ")[output[i-1][1].split(" ").__len__()-1].split(",")[0]) + float(output[i][1].split(" ")[j].split(",")[0]),2)) + "," + str(round(float(output[i-1][1].split(" ")[output[i-1][1].split(" ").__len__()-1].split(",")[1]) + float(output[i][1].split(" ")[j].split(",")[1]),2))+" "
            output[i][1] = ''.join(list(new_list)[k] for k in range(0,list(new_list).__len__()-1))
            end_i = output[i][1].split(" ")[output[i][1].split(" ").__len__() - 1]
            #print(end_i)
            output[i].append(end_i)
            #终点
        except:
            if output[i][0] == 'z':
                output[output.__len__() - 1][0] = 'l'
                output[output.__len__() - 1][1] = output[0][1] #M点坐标 绝对坐标
                output[i].append(output[0][1])
        try:
            output[i].append(output[i - 1][2])#起点
        except:
            output[i].append(output[i][1])

    return output

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
                f.append([x[j],y[j]])

        if i[0] == 'c':
            x, y = bezier(i[3], i[1], i[2])
            for j in range(0, i[3]):
                f.append([x[j], y[j]])
    return f

def proccess(i):
    print(i,"joined")
    c0 = 0
    for k in range(0, vec.__len__() - 1):
        c0 += vec[k] * (math.e ** (-i * 2 * math.pi * 1j * ((1 / vec.__len__()) * k))) * (1 / vec.__len__())  # 傅里叶级数
    return c0



for i in transform():#简单变换
    print(i)
_data = transform()

add_time()#svg坐标转换
f1 = output_()

vec = []
for i in range(0, f1.__len__() - 1):
    vec.append(f1[i][0] + f1[i][1] * 1j)  # 向量变换

if __name__ == '__main__':
    p = Pool(8)
    c = []
    for i in range(-t1, t1 + 1):
        res = p.apply_async(proccess, args=(i,))
        c.append([res, i])
    p.close()
    p.join()

    params = []  # 0:弧度 1:半径 2:角速度参数
    for i in c:
        params.append([math.atan(i[0].get().imag/i[0].get().real),i[0].get().real/math.cos(math.atan(i[0].get().imag/i[0].get().real))*n,i[1]])  # x=arctan(b/a);r=a/(cosx)

    with open("params.json",mode='w') as f:
        f.write(str(params))