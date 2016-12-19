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
import math
from mypkg import debug

#global variable
all_windows_size = 1814400
windows_size = 604800

class window:

    def __init__(self,windowdata):
        self.windowmatrix = windowdata

    def printw(self):
        for item in self.windowmatrix:
            print item

class day:

    def __init__(self,daydata):
        self.daymatrix = daydata

    def printw(self):
        for item in self.daymatrix:
            print item

def window_gen(alldata,me_time):
    global all_windows_size

    tot_day = all_windows_size/3600/24
    windows = [[],[]]
    days = []
    #print me_time
    ntime = convert_time(me_time)
    nsec = datetime.datetime.fromtimestamp(ntime)
    n_dtime = [nsec.hour, nsec.minute, nsec.second]
    rsec = n_dtime[0]*3600 + n_dtime[1]*60+n_dtime[2]
    cur_time = datetime.datetime.fromtimestamp(ntime-rsec).strftime('%c')
    #print cur_time
    time_t = get_time(cur_time)
    #print convert_time(cur_time)
    rec = 0

    for i in range(0,tot_day):
        wvec = []
        j = rec
        for j in range(0,len(alldata)):
            #print alldata[j].time
            #print time_t[0]+3600*24*i
            if alldata[j].time < time_t[0]+3600*24*i:
                continue
            elif alldata[j].time >= time_t[0]+3600*24*(i+1):
                rec = j - 1
                break
            else:
                #print 'found'
                wvec.append(alldata[j])
        #print wvec
        iday = day(wvec)
        days.append(iday)
    #print len(days)
    tmpvec = []
    for i in range(len(days)-7,len(days)):
        #for item in days[i].daymatrix:
        #    print item
        tmpvec.append(days[i])
    windows[0] = window(tmpvec)
    '''
    for i in windows[0].windowmatrix:
        for j in i.daymatrix:
            print j
    print len(days)
    '''
    #windows[0].printw()
    for i in range(0,len(days)-7):
        tmpvec = []
        for j in range(i,i+7):
            tmpvec.append(days[j])
        windows[1].append(window(tmpvec))
    #print windows
    return windows

def convert_windows_to_cluster_data(windows):
    data = []
    for wins in windows:
        tmp = [0,0,0,0,0,0]
        cnt = 0
        for i in wins.windowmatrix:
            for j in i.daymatrix:
                cnt += 1
                tmp[0] += j.price
                for p in range(0,5):
                    tmp[p+1] += j.weather[p]
        #print tmp[0]
        #print cnt
        tmp[0] /= cnt
        print tmp[0]
        for i in range(0,5):
            tmp[i+1] /= cnt
        data.append(tmp)
    return data

def convert_window_to_cluster_data(window):
    tmp = [0,0,0,0,0,0]
    cnt = 0
    for i in window.windowmatrix:
        for j in i.daymatrix:
            cnt += 1
            tmp[0] += j.price
            for p in range(0,5):
                tmp[p+1] += j.weather[p]
    print tmp[0]
    print cnt
    tmp[0] /= cnt
    for i in range(0,5):
        tmp[i+1] /= cnt
    return tmp

def ba_weight(wA,wB):
    '''
    vec type ['40', '30', '0.00', '3.8', '37'] 7.0 12/09/16 1481305066.0
    :param windowA:
    :param windowB:
    :return:
    '''
    windowA = wA
    windowB = wB
    cnt = 0
    avgA = [0,[0,0,0,0,0]]
    avgB = [0,[0,0,0,0,0]]
    #print windowA
    for i in windowA.windowmatrix:
        for j in i.daymatrix:
            avgA[0] += j.price
            for p in range(0, len(avgA[1])):
                avgA[1][p] += j.weather[p]
            cnt += 1
    avgA[0] /= cnt
    for i in range(0, len(avgA[1])):
        avgA[1][i] /= cnt
    cnt = 0
    for i in windowB.windowmatrix:
        for j in i.daymatrix:
            avgA[0] += j.price
            for p in range(0, len(avgA[1])):
                avgA[1][p] += j.weather[p]
            cnt += 1
    avgB[0] /= cnt
    for i in range(0, len(avgB[1])):
        avgB[1][i] /= cnt
    dist = get_dist(avgA,avgB)
    #print dist
    return dist

def get_dist(A,B):
    dist = pow(A[0] - B[0], 2)
    for i in range(0, len(A[1])):
        dist += pow(A[1][i] - B[1][i], 2)
    dist = math.sqrt(dist)
    return dist

def ba_vec_gen(supvecs,weathervec):
    for i in range(0,len(supvecs)):
        for j in range(0,len(weathervec)):
            #print supvecs[i].date
            #print str(weathervec[j][0])
            if supvecs[i].date == str(weathervec[j][0]):
                supvecs[i].weather = weathervec[j][1]
                #print weathervec[j][1]
    #for item in supvecs:
    #    print item
    return supvecs

def ba_similarity(tar_win,win_list):
    dist = sys.maxsize
    res = []
    for wins in win_list:
        tmpd = ba_weight(tar_win,wins)
        if tmpd < dist:
            dist = tmpd
            res = wins
    return res

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
                    #if break_flag == 0:
                        #print dloc
                        #print location
                    break_flag = 1
                    price = float(paras[0])
                    ntime = paras[5][0:(len(paras[5])-1)]
                    rtime = convert_time(paras[4] + ' ' + ntime)
                    #print rtime
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
    if type == 'lyft':
        with open(sys.path[0]+'/processed/lyft/lyft.csv', 'r+') as uberfile:
            for line in uberfile:
                paras = line.split(' ')
                dloc = [float(paras[1]),float(paras[2])]
                if dloc == location:
                    if break_flag == 0:
                    #    print dloc
                        print location
                    break_flag = 1
                    price = float(paras[0])
                    ntime = paras[5][0:(len(paras[5]) - 1)]
                    rtime = convert_time(paras[4] + ' ' + ntime)
                    #print rtime
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
            tmpvec = [row['date'],[float(row['maxt']),float(row['mint']),float(row['rain']),float(row['wind']),float(row['humidity'])]]
            weather.append(tmpvec)
    return weather

def convert_time(time):
    #print time
    if len(time) != 17:
        print time
    rtime = datetime.datetime.strptime(time, "%m/%d/%y %H:%M:%S")
    anchor = datetime.datetime.fromtimestamp(0)
    sec = (rtime - anchor).total_seconds()
    #print sec
    return sec

def get_time(time):
    global all_windows_size
    global windows_size
    sec = convert_time(time)
    #print sec
    start_time = sec - all_windows_size
    stime = datetime.datetime.fromtimestamp(start_time)
    #print stime
    pre_time = sec - windows_size
    ptime = datetime.datetime.fromtimestamp(pre_time)
    #print ptime
    return [start_time,pre_time]

def time_in(time,rag):
    rtime = datetime.datetime.fromtimestamp(time)
    Ltime = datetime.datetime.fromtimestamp(rag[0])
    Utime = datetime.datetime.fromtimestamp(rag[1])
    r_dtime = [rtime.hour,rtime.minute,rtime.second]
    l_dtime = [Ltime.hour,Ltime.minute,Ltime.second]
    u_dtime = [Utime.hour,Utime.minute,Utime.second]
    day_sec_C = r_dtime[0]*3600+r_dtime[1]*60+r_dtime[2]
    day_sec_L = l_dtime[0]*3600+l_dtime[1]*60+l_dtime[2]
    day_sec_U = u_dtime[0]*3600+u_dtime[1]*60+u_dtime[2]
    #print [Ltime.strftime('%c'),rtime.strftime('%c'),Utime.strftime('%c')]
    if day_sec_L <= day_sec_C and day_sec_C <= day_sec_U:
        return True
    return False

def day_to_day_mean(windows,time):
    day_vec = []
    meanvec = []
    rtime = convert_time(time)
    #print rtime
    timeframe = [rtime - 600, rtime + 600]
    for i in windows.windowmatrix:
        '''
        Do the following for each day:
            1. get the average of price for the given time frame
                in this case +- 300s from the provided the time point
            2. calculate the 24hr-variation of the seven days
                resulting in a 6 by 1 vector
                <v21,v32,v43,v54,v65,76>
        '''
        avgD = [0, [0, 0, 0, 0, 0]]
        cnt = 0
        for j in i.daymatrix:
            if time_in(j.time,timeframe):
                #print 'found'
                avgD[0] += j.price
                for p in range(0, len(avgD[1])):
                    avgD[1][p] += j.weather[p]
                cnt += 1
        if cnt != 0:
            avgD[0] /= cnt
            for p in range(0,len(avgD[1])):
                avgD[1][p] /= cnt
            day_vec.append(avgD)

    #print len(day_vec)

    for i in range(0,len(day_vec)-1):
        tmp = [0, [0, 0, 0, 0, 0]]
        tmp[0] = day_vec[i+1][0]-day_vec[i][0]
        for j in range(0,len(day_vec[i][1])):
            tmp[1][j] = day_vec[i+1][1][j]-day_vec[i][1][j]
        meanvec.append(tmp)
    #print len(meanvec)
    return meanvec

def get_surge(mean,windows,time):
    tcnt = 0
    avgD = [0, [0, 0, 0, 0, 0]]
    rtime = convert_time(time)
    # print rtime
    timeframe = [rtime - 600, rtime + 600]
    #print [datetime.datetime.fromtimestamp(timeframe[0]),datetime.datetime.fromtimestamp(timeframe[1])]
    #print len(windows.windowmatrix)
    for i in windows.windowmatrix:
        '''
        add the variation to the previous day
        windows has seven days
        only extract data from the last day, which is 24 hr prior the time we are trying to predict
        '''
        if tcnt <= 5:
            tcnt += 1
            continue
        else:
            cnt = 0
            #print len(i.daymatrix)
            itcnt = 0
            for j in i.daymatrix:
                itcnt += 1
                #print datetime.datetime.fromtimestamp(j.time)
                if time_in(j.time,timeframe):
                    #print 'found'
                    avgD[0] += j.price
                    for p in range(0, len(avgD[1])):
                        avgD[1][p] += j.weather[p]
                    cnt += 1
            #print itcnt
            if cnt != 0:
                avgD[0] /= cnt
                for p in range(0,len(avgD[1])):
                    avgD[1][p] /= cnt
                break
            else:
                avgD[0] = 7.0
                for p in range(0, len(avgD[1])):
                    avgD[1][p] /= 1
                break
    res = avgD[0] + mean[0]

    return res

def getmean(meanvec):
    #print meanvec
    avgD = [0, [0, 0, 0, 0, 0]]
    for i in range(0,len(meanvec)):
        avgD[0] += meanvec[i][0]
        for p in range(0, len(avgD[1])):
            avgD[1][p] += meanvec[i][1][p]
    return avgD

def predict(location,time,type):

    datavecs = data_read(location,type)
    weather = weather_read()
    vecs = ba_vec_gen(datavecs,weather)
    windows = window_gen(vecs,time)
    similar_window = ba_similarity(windows[0],windows[1])
    #debug.debug_window(windows[0],similar_window)
    ta = day_to_day_mean(windows[0],time)
    #print 'ta'+str(ta)
    meanA = getmean(ta)
    meanB = day_to_day_mean(similar_window,time)
    meanB = getmean(meanB)
    meanAvg = [0, [0, 0, 0, 0, 0]]
    #print len(meanA)
    #print meanA
    #print meanB
    for i in range(0,len(meanA)):
        #print meanA[0]
        meanAvg[0] = (meanA[0]+meanB[0])/2
        for j in range(0,len(meanAvg[1])):
            meanAvg[1][j] = (meanA[1][j]+meanB[1][j])/2
    #print meanAvg
    #print meanA
    #print meanB
    surge = get_surge(meanAvg,windows[0],time)

    if type == 'uber':
        if surge <= 7.0:
            return 7.0
        else:
            return surge
    if type == 'lyft':
        if surge <= 800:
            return 0
        else:
            return surge/800

    return -1