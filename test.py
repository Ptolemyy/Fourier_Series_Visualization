import time
from multiprocessing import Pool
import random

print("wdnmd")
time.sleep(1)
print("1")

def sb():

    return 0

if __name__ == '__main__':

    p = Pool(4)
    for i in range(1,4):
        p.apply_async(sb, args=(i,))
    p.close()
    p.join()