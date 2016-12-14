import json
import os
import processing_var as pv
import datetime
import time
import perf_print

month=['nov','dec']

with open('../processed/weather.csv','w+') as profile:
    profile.write('date,maxt,mint,rain,wind,humidity\n')
    for file in os.listdir('../DataRepo/Weather'):
        #print file
        dataline = []
        if file[0:3] == 'dec':
            dataline = '12/0'+file[3]+'/16'
        else:
            if len(file) == 8:
                dataline = '11/0' + file[3] + '/16'
            else:
                dataline = '11/' + file[3:5] + '/16'
        dataline += ','
        print dataline
        with open('../DataRepo/Weather/'+str(file),'r') as weatherfile:
            while True:
                line = weatherfile.readline()
                if not line:
                    break
                #print line
                nl = ' '.join(line.split())
                paras = nl.split(' ')
                #print paras
                if paras[0] == 'TEMPERATURE':
                    skip = weatherfile.readline()
                    #print 'TEMPERATURE'
                    for i in range(0,3):
                        nline = weatherfile.readline()
                        nl = ' '.join(nline.split())
                        paras = nl.split(' ')
                        if i <= 1:
                            dataline += paras[1]+','
                        #print paras[1]
                if paras[0] == 'PRECIPITATION':
                    #print 'PRECIPITATION'
                    nline = weatherfile.readline()
                    nl = ' '.join(nline.split())
                    paras = nl.split(' ')
                    dataline += paras[1] + ','
                    print paras[1]
                    for i in range(0, 3):
                        weatherfile.readline()
                if paras[0] == 'WIND':
                    #print 'WIND'
                    for i in range(0, 3):
                        nline = weatherfile.readline()
                        nl = ' '.join(nline.split())
                        paras = nl.split(' ')
                        if i == 2:
                            dataline += paras[3] + ','
                            print paras[3]
                if paras[0] == 'RELATIVE':
                    #print 'HUMIDITY'
                    for i in range(0, 3):
                        nline = weatherfile.readline()
                        nl = ' '.join(nline.split())
                        paras = nl.split(' ')
                        if i == 2:
                            dataline += paras[1] + '\n'
                            print paras[1]
        print dataline
        profile.write(dataline)