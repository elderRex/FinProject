'''
Predict Current Price
Get Surge Through:
 1. price to current location where baseline is always $7.00
 2. Surge can be calculated from the price predicted
K-means prediction

Assign User to Block according to nearest neighbor
'''

import supportvec
import sys
import csv
import datetime

#global variable
all_windows_size = 1814400
windows_size = 604800
slide_size = 24

class window:

    def __init__(self,windowdata):
        self.windowmatrix = windowdata

def window_gen(alldata,cur_time):
    windows = [[],[]]
    time_t = get_time(cur_time)
    print time_t
    for item in alldata:
        return

def ba_slide_window():

    return

def ba_weight():
    return

def ba_vec_gen(supvecs,weathervec):
    for i in range(0,len(supvecs)):
        for j in range(0,len(weathervec)):
            #print supvecs[i].date
            #print str(weathervec[j][0])
            if supvecs[i].date == str(weathervec[j][0]):
                supvecs[i].weather = weathervec[j][1]
                print weathervec[j][1]
    for item in supvecs:
        print item
    return supvecs

def ba_similarity():
    return

'''
data format
price lat lng base price date time
7.0 40.709461 -73.998968 7.0 11/16/16 23:08:11
'''
def data_read(location,type):
    datarepo = []
    break_flag = 0
    #print sys.path
    if type == 'uber':
        with open(sys.path[0]+'/processed/uberx/uberx.csv', 'r+') as uberfile:
            for line in uberfile:
                paras = line.split(' ')
                dloc = [float(paras[1]),float(paras[2])]
                if dloc == location:
                    if break_flag == 0:
                        print dloc
                        print location
                    break_flag = 1
                    price = float(paras[0])
                    tmpvec = supportvec.supvec(price,location,paras[4],paras[5])
                    datarepo.append(tmpvec)
                else:
                    '''
                    break when first not equal
                    '''
                    if break_flag == 1:
                        break
        #for item in datarepo:
        #    print item
    if type == 'lyft':
        with open(sys.path[0]+'/processed/lyft/lyft.csv', 'r+') as uberfile:
            for line in uberfile:
                paras = line.split(' ')
                dloc = [float(paras[1]),float(paras[2])]
                if dloc == location:
                    if break_flag == 0:
                        print dloc
                        print location
                    break_flag = 1
                    price = float(paras[0])
                    rtime = convert_time(paras[4]+' '+paras[5])
                    print rtime
                    tmpvec = supportvec.supvec(price,location,float(rtime),paras[4])
                    datarepo.append(tmpvec)
                else:
                    '''
                    break when first not equal
                    '''
                    if break_flag == 1:
                        break
        #for item in datarepo:
        #    print item

    return datarepo

def weather_read():
    weather = []
    with open(sys.path[0]+'/processed/weather.csv','r+') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = row['date']
            #print date
            tmpvec = [row['date'],[row['maxt'],row['mint'],row['rain'],row['wind'],row['humidity']]]
            weather.append(tmpvec)
    return weather

def convert_time(time):
    rtime = datetime.datetime.strptime(time, "%m/%d/%y %H:%M:%S")
    anchor = datetime.datetime.fromtimestamp(0)
    sec = (rtime - anchor).total_seconds()
    return sec

def get_time(time):
    global all_windows_size
    global windows_size
    sec = convert_time(time)
    print sec
    start_time = sec - all_windows_size
    stime = datetime.datetime.fromtimestamp(start_time)
    print stime
    pre_time = sec - windows_size
    ptime = datetime.datetime.fromtimestamp(pre_time)
    print ptime
    return [start_time,pre_time]

def predict(location,time,type):
    datavecs = data_read(location,type)
    weather = weather_read()
    vecs = ba_vec_gen(datavecs,weather)
    windows = window_gen(vecs,time)
    #for item in vecs:
    #    print item
    preditive_center = location
    return