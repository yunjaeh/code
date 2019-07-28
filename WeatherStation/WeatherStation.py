mport numpy as np
import pandas as pd
from datetime import datetime

class Station():
    
    def __init__(self, fname):
        self.fname = fname
        self.Data = []
        self.Attributes = []
        
        self.Time = []
        self.Temperature = []
        self.WindSpd = []
        self.WindDir = []
        self.Solar = []
        self.RH = []
    
    def readData(self):
        self.Data = pd.read_csv(self.fname,parse_dates=[1],header=0)
        self.Data.columns = [c.replace(' ','_')for c in self.Data.columns]
        
        print(self.Data.columns)
        
        self.Time = self.Data.Data_Timestamp.tolist() # list
        self.Temperature = self.Data.TEMP_C
        self.WindSpd = self.Data.WS_AVG_MS
        self.WindDir = self.Data.WD_AVG_DEG
        
        print(len(self.Time),len(self.Temperature),len(self.WindSpd))
        print(type(self.Time))
        print(type(self.WindSpd))
        
        
        print(self.Time)
#         for x in self.Data.Data_Timestamp:
#             print(type(x))
            
            # self.Time.append(datetime.strptime(x, '%Y-%m-%d %h:%m:%s'))
        #             print(self.Data.Data_Timestamp[i])
#         print(self.Time[0])
        
        
        

    def time_average():
        self.Data = []
        
        #with open(self.fname) as fp:
         #   for line in fp:
          #      print(line.split())


Hazrat = Station('hazrat_test.csv')
Hazrat.readData()
