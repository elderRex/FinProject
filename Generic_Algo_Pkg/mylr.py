from custom_algo_pkg.slide_algo import *

import os
import sys
from pyspc import *
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
    from pyspark.mllib.classification import LogisticRegressionWithLBFGS
    from pyspark.mllib.regression import LabeledPoint

    print ("Good riddance. Pyspark is now onboard.")

except ImportError as e:
    print ("Error importing Spark Modules", e)
    sys.exit(1)

import numpy as np
import math

def get_label(data):
    resdata = []
    min = 1000
    max = 0
    for i in range(0, len(data)):
        if data[i][0] < min:
            min = data[i][0]
        if data[i][0] > max:
            max = data[i][0]
    baseline = max - min
    for i in range(0,len(data)):
        tmp = []
        label = (data[i][0] - min)/ baseline
        label *= 100
        label = (label - label % 20) / 20
        if label == 5:
            label = 4
        tmp.append(label)
        t2 = []
        for j in range(0,len(data[i])):
            t2.append(data[i][j])
        resdata.append(LabeledPoint(label, t2))

    return resdata

def lr_predict(location,time,type='uber'):
    global sc
    datavecs = data_read(location, type)
    weather = weather_read()
    vecs = ba_vec_gen(datavecs, weather)
    windows = window_gen(vecs, time)

    pre_d = convert_window_to_cluster_data(windows[0])
    tra_d = convert_windows_to_cluster_data(windows[1])
    train_dat = get_label(tra_d)
    print pre_d
    print train_dat
    data = sc.parallelize(train_dat)
    model = LogisticRegressionWithLBFGS.train(sc.parallelize(train_dat), numClasses=5)

    cnt = 0
    res = model.predict(pre_d)

    print res

    return 0
