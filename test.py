from custom_algo_pkg import slide_algo as sa

import os
import sys
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
    from numpy import array
    from math import sqrt

    print ("Good riddance. Pyspark is now onboard.")

except ImportError as e:
    print ("Error importing Spark Modules", e)
    sys.exit(1)

sc = SparkContext()

# 4 data points (0.0, 0.0), (1.0, 1.0), (9.0, 8.0) (8.0, 9.0)
data = array([0.0, 0.0, 1.0, 1.0, 9.0, 8.0, 8.0, 9.0]).reshape(4, 2)
print data
# Generate K means
model = KMeans.train(sc.parallelize(data), 2, maxIterations=10)

# Print out the cluster of each data point
print (model.predict(array([0.0, 0.0])))
print (model.predict(array([1.0, 1.0])))
print (model.predict(array([9.0, 8.0])))
print (model.predict(array([8.0, 9.0])))