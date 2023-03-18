import json
import math
import argparse
from multiprocessing import Pool
import multiprocessing


parser = argparse.ArgumentParser(description='test')
parser.add_argument('--t1',default="200",type=int,help = "None")

args = parser.parse_args()

f1 = []
t1 = args.t1 #实际项数为(2*t1)+1
n = 0.0625 #放大率

with open("f(x).json",mode='r') as f:
    f1=json.load(f)

def proccess(i):
    print(i,"joined")
    c0 = 0
    for k in range(0, vec.__len__() - 1):
        c0 += vec[k] * (math.e ** (-i * 2 * math.pi * 1j * ((1 / vec.__len__()) * k))) * (1 / vec.__len__())  # 傅里叶级数
    return c0

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