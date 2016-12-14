import json
import os
import datavec as dv
import datetime
import time
import perf_print

#query_cnt = input('query_cnt:')

def custom_dict_insert(lng,lat,dat,time,dict):
    for i in range(0,len(dict)):
        if dict[i].loc[0] == lat and dict[i].loc[1] == lng:
            #print dict[i]
            dict[i].insert(dat,time)
            return
    tmpvec = dv.myvec(lat,lng)
    tmpvec.insert(data,time)
    dict.append(tmpvec)
    return

loc_data = []

dat_cnt = 0
start = datetime.datetime.now()

with open('../processed/lyft/lyft.csv','w+') as profile:
    with open('../processed/lyft/blocklist.csv', 'w+') as blockfile:
        for file in os.listdir('../DataRepo/lyft'):
            '''
            query_cnt += 1
            if query_cnt >= 2:
                break
            '''
            print file
            with open('../DataRepo/lyft/'+str(file),'r') as jsonfile:
                for line in jsonfile:
                    data = json.loads(line)
                    low_price = float(data["Low"]["s"])
                    if low_price < 800.0:
                        continue
                    surge = (float(data["Prime"]["n"])+100)/100
                    lng = float(data["Lng"]["s"])
                    lat = float(data["Lat"]["s"])
                    #print low_price
                    #print data["Prime"]["n"]
                    low_price = low_price * surge
                    time = data["Time"]["s"]
                    rtime = datetime.datetime.fromtimestamp(float(time)).strftime('%c')
                    #print rtime
                    #print data["Low"]["s"]
                    #print data["High"]["s"]
                    #print low_price
                    dat = str(low_price)+' '+str(lat)+' '+str(lng)+' '+str(800.0)
                    custom_dict_insert(float(data["Lng"]["s"]),float(data["Lat"]["s"]),dat,rtime,loc_data)
                    dat_cnt += 1

        for i in range(0,len(loc_data)):
            loc_data[i].data.sort(key=lambda item: item[1])
            blockfile.write(str(loc_data[i].loc[0]) + ' ' + str(loc_data[i].loc[1]) + '\n')
            for j in range(0,len(loc_data[i].data)):
                profile.write(str(loc_data[i].data[j][0]) + ' ' + str(loc_data[i].data[j][1]) + '\n')
        end = datetime.datetime.now()
        ct = end-start
        perf_print.print_perf(str(ct.microseconds),'lyft.csv','microsecond',dat_cnt,'Lyft data Parsed')