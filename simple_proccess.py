import xml.etree.ElementTree as ET
import json
import argparse


parser = argparse.ArgumentParser(description='test')
parser.add_argument('--path',type=str,help = "None")

args = parser.parse_args()


tree = ET.parse(args.path)
root = tree.getroot()

_data = str(root[1][1][0].attrib['d'])

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

for i in transform():
    print(i)

with open("order.json",mode="w") as f:
    f.write(json.dumps(transform()))