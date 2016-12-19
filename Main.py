import os
import sys
from matplotlib import pyplot as plt
import datetime
from mypkg import main_process as mp

def convert_time(time):
    #print time
    if len(time) != 17:
        print time
    rtime = datetime.datetime.strptime(time, "%m/%d/%y %H:%M:%S")
    anchor = datetime.datetime.fromtimestamp(0)
    sec = (rtime - anchor).total_seconds()
    #print sec
    return sec

plt.ion()
plt.draw()
x = []
y = []
xx = []
yy = []
with open(sys.path[0]+'/processed/testB.txt','r+') as testfile:
    for line in testfile:
        paras = line.split(' ')
        t = paras[5][:len(paras[5])-1]
        res = mp.main(1,[float(paras[1]),float(paras[2])],str(paras[4]+' '+t))
        rsec = convert_time(str(paras[4]+' '+t))
        #print [float(rsec),float(rsec)]
        #print [float(paras[0]),res[0]*7.0]
        x.append(res[0])
        y.append(float(rsec))
        xx.append(float(paras[0]))
        yy.append(float(rsec))
plt.scatter(yy,xx, color='b', s=2)
plt.scatter(y,x, color='r',s=1)
#plt.pause(10)
plt.savefig('resD.jpg')

#mp.main(2,[40.754974,-74.005203],'12/09/16 17:29:15')
#mp.main(2,[40.754974,-74.005203],'12/10/16 16:24:32')