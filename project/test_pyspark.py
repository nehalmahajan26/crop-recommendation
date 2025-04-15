from pyspark import SparkContext

sc = SparkContext(appName="TestPySpark")
data = [1, 2, 3, 4, 5]
rdd = sc.parallelize(data)
print(rdd.count())  # Should print 5
sc.stop()  # Stop the SparkContext
