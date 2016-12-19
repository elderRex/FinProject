from custom_algo_pkg.slide_algo import *

import os
import sys
import pyspc
# Set the path for spark installation
# this is the path where you have built spark using sbt/sbt assembly
os.environ['SPARK_HOME'] = "C:\Users\YuNick\Documents\spark-2.0.2-bin-hadoop2.7"
# os.environ['SPARK_HOME'] = "/home/jie/d2/spark-0.9.1"
# Append to PYTHONPATH so that pyspark could be found
sys.path.append("C:\Users\YuNick\Documents\spark-2.0.2-bin-hadoop2.7\python")
# sys.path.append("/home/jie/d2/spark-0.9.1/python")

# Now we are ready to import Spark Modules
try:
    from pyspark import SparkContext
    from pyspark.mllib.clustering import KMeans

    print ("Good riddance. Pyspark is now onboard.")

except ImportError as e:
    print ("Error importing Spark Modules", e)
    sys.exit(1)

from numpy import array
from math import sqrt
'''
sc = SparkContext()

# 4 data points (0.0, 0.0), (1.0, 1.0), (9.0, 8.0) (8.0, 9.0)
data = array([0.0, 0.0, 1.0, 1.0, 9.0, 8.0, 8.0, 9.0]).reshape(4, 2)
print data
# Generate K means
model = KMeans.train(sc.parallelize(data), 8, maxIterations=10, runs=30, initializationMode="random")

# Print out the cluster of each data point
print (model.predict(array([0.0, 0.0])))
'''

def kmeans_predict(location,time,type='uber'):
    global sc
    datavecs = data_read(location, type)
    weather = weather_read()
    vecs = ba_vec_gen(datavecs, weather)
    windows = window_gen(vecs, time)

    predict_dat = convert_window_to_cluster_data(windows[0])
    train_dat = convert_windows_to_cluster_data(windows[1])
    #print predict_dat
    #print train_dat
    model = KMeans.train(sc.parallelize(train_dat), 14, maxIterations=10, initializationMode="random")

    res = model.predict(predict_dat)
    t_i = day_to_day_mean(windows[0], time)
    t_i = getmean(t_i)
    meanAvg = [0, [0, 0, 0, 0, 0]]
    for i in range(0,len(t_i)):
        #print meanA[0]
        meanAvg[0] = t_i[0]
        for j in range(0,len(meanAvg[1])):
            meanAvg[1][j] = t_i[1][j]

    cluster_cnt = 1
    for i in range(0,len(train_dat)):
        if model.predict(train_dat[i]) == res:
            t_ii = day_to_day_mean(windows[1][i],time)
            t_ii = getmean(t_ii)
            cluster_cnt += 1
            for i in range(0, len(t_ii)):
                # print meanA[0]
                meanAvg[0] += t_ii[0]
                for j in range(0, len(meanAvg[1])):
                    meanAvg[1][j] += t_ii[1][j]

    meanAvg[0] /= cluster_cnt
    for i in range(0,5):
        meanAvg[1][i] /= cluster_cnt

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

    return surge
