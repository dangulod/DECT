import pyspark as spark
import pandas as pd
import numpy as np

from pyspark.sql.types import *
from pyspark.sql.functions import udf
from pyspark.sql.functions import sqrt

# spark & SQL context

sc = spark.SparkContext()
sql = spark.SQLContext(sc)

# read data

cor_credit = pd.read_excel("/Users/n87557/Documents/Metodologia de capital/DECT/data/cor_credit_drivers.xlsx")
sensi = pd.read_excel("/Users/n87557/Documents/Metodologia de capital/DECT/data/TB_SENSIB_corr.xlsx")

cor_credit_rdd = sql.createDataFrame(cor_credit)
sensi_rdd = sql.createDataFrame(sensi)
  
class scenario_spark:
  
  def __init__(self, cor_credit, sensitivities):
    def __f(x):
      if (x.split("_")[0] == "SCF"):
        return x.split("_")[1]
      else:
        return x.split("_")[0]
  
    __f_udf = udf(__f, StringType())
    
    self.cor_credit = cor_credit
    
    self.n_simul = None
    
    self.rnd = None
  
    self.sensitivities = sensi_rdd.withColumn("equation", __f_udf(sensi_rdd['equation']))
    self.sensitivities = self.sensitivities.withColumn("IF", 
    sqrt(1- (self.sensitivities['GF'] ** 2 + self.sensitivities['LF'] ** 2)))


x = scenario_spark(cor_credit_rdd, sensi_rdd)
