#!/public/spark-0.9.1/bin/pyspark

import os
import sys

# Set the path for spark installation
# this is the path where you have built spark using sbt/sbt assembly
os.environ['SPARK_HOME'] = "D:\Personal\US\Columbia\Fall 2016\EECS 6893\FinProject\spark-2.0.2-bin-hadoop2.7"
# os.environ['SPARK_HOME'] = "/home/jie/d2/spark-0.9.1"
# Append to PYTHONPATH so that pyspark could be found
sys.path.append("D:\Personal\US\Columbia\Fall 2016\EECS 6893\FinProject\spark-2.0.2-bin-hadoop2.7\python")
# sys.path.append("/home/jie/d2/spark-0.9.1/python")

# Now we are ready to import Spark Modules
try:
    from pyspark import SparkContext
    from pyspark import SparkConf

    print ("Good riddance. Pyspark is now onboard.")

except ImportError as e:
    print ("Error importing Spark Modules", e)
    sys.exit(1)

import datetime
from mypkg import main_process as mp

mp.main(0,[40.809395,-73.989300],datetime.datetime.now())