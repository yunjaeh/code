import os
import numpy as np
import math
import matplotlib.pyplot as plt
from datetime import datetime


class postProcess():
    def __init__(self,fname,dirInput='./',dirOutput='./'):
        self.fname = fname
        self.dirInput = dirInput
        self.dirOutput = dirOutput
        self.time = []
        self.cRaw = []
        self.c = np.empty(0)
        self.ACH = {}
        self.ACH_target = {}
        self.range = range(600, 1200)
        self.numTest = 0
        self.dataIdx = []
        self.cRawMinMax = []

        if(dirOutput != './'):
            if not os.path.exists(dirOutput):
                os.mkdirs(dirOutput)
            
        self.readData()

    def __repr__(self):
        # print summary of raw data
        # the number of experiments in the file
        # minimum and maximum concentration of  each experiment
        message = []
        message.append(self.fname+', # test:'+str(self.numTest))
        # print('idx data:', self.dataIdx)
        for i in range(self.numTest):
            message.append(' * Test '+str(i+1) )
            message.append('  PM \t (min, max): '+str(self.cRawMinMax[i]))
            if (i+1) in self.ACH_target.keys():
                tempACH = self.ACH_target[i+1]
                message.append('  ACH \t (min, max): ' \
                    + str((round(tempACH.min(),2), round(tempACH.max(),2))))
                message.append(' \t Mean: '+str(round(tempACH.mean(),2)) + \
                ',\t Std:  '+str(round(tempACH.std(),2)) )
            message.append('')
       
        return '\n'.join(message)    

    def readData(self):
        with open(self.dirInput + self.fname) as fp:
            idx_temp = 0
            for line in fp:
                line_split = line.split(',')
                # print(line_split)
                try :
                    if(line_split[0]=='MM/dd/yyyy'):
                        self.numTest+=1
                        self.dataIdx.append(idx_temp)
                        self.ACH.append([])
                    ts = datetime.strptime(' '.join(line_split[0:2]),'%m/%d/%Y %H:%M:%S')
                    self.time.append(ts)
                    self.cRaw.append(float(line_split[2].replace('\n','')))
                    idx_temp += 1
                except:
                    continue
            self.dataIdx.append(idx_temp+1)
#             print(self.ACH)
            span_smooth = 61
            self.c = np.convolve(np.log(self.cRaw), np.ones((span_smooth,))/span_smooth, mode='same')
        
        for i in range(self.numTest):
            self.cRawMinMax.append( (min(self.cRaw[self.dataIdx[i]:self.dataIdx[i+1]]), \
                max(self.cRaw[self.dataIdx[i]:self.dataIdx[i+1]])))

    def plotRaw(self):
        plt.plot(range(len(self.c)),np.log(self.cRaw))
        plt.plot(range(len(self.c)),self.c)
        plt.xlabel('Time [sec]')
        plt.ylabel('log(Concentration)')
        plt.title('Raw and smoothed data')
        plt.savefig(self.dirOutput + self.fname.replace('.csv','.png'))
        plt.cla()
#         plt.show()
    
    def compute(self, testIdx):
        if(testIdx > self.numTest):
            raise Exception('Test number not valid')
        else:
            tt = self.time[self.dataIdx[testIdx-1]:self.dataIdx[testIdx]]
            cc = self.c[self.dataIdx[testIdx-1]:self.dataIdx[testIdx]]
        # print(len(tt),len(cc))
        id_max = np.argmax(cc)
        c_max = max(cc)
        len_data = len(cc)
        t_target = np.arange(1, len_data-id_max)
        c_target = cc[id_max+1:len_data+1]
        self.ACH[testIdx]=(c_target - c_max)/t_target * -3600

    def plot(self,testIdx,markRange=False):
        if(testIdx > self.numTest):
            raise Exception('Test number not valid')
        plt.plot(range(len(self.ACH[testIdx])),self.ACH[testIdx])
        plt.plot(self.range,self.ACH[testIdx][self.range],'x')
        plt.xlabel('Time [sec]')
        plt.ylabel('ACH [1/hr]')
        # plt.show()
        plt.savefig(self.dirOutput + self.fname.replace('.csv','') \
            +'_'+str(testIdx)+'.png')
        plt.cla()

    def getACH(self,testIdx,period=(600,1200)):
        self.range = range(period[0],period[1])
        self.ACH_target[testIdx] = self.ACH[testIdx][self.range]
        return self.ACH_target[testIdx]
        # [range(period[0],period[2])]
        


        
    def minute_avg(self):
        self.time_avg = []
        self.c_avg = []
        self.ACH_avg = []
        raise Exception('Not implemented yet')

    def compute_time_avg(self,numTest):
        raise Exception('Not implemented yet')
    
    def plot_ACH_time_avg(self,numTest):
        raise Exception('Not implemented yet')
