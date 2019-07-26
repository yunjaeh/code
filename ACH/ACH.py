import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime


class ACH():
    def __init__(self):
        self.fname = ''
        self.time = []
        self.c_raw = []
        self.c = np.empty(0)
        self.ACH = []
        
        self.time_avg = []
        self.c_avg = []
        self.ACH_avg = []
        
        self.num_test = 0
        self.data_idx = []

    def read_input(self,fname):
        self.fname=fname
        with open(fname) as fp:
            idx_temp = 0
            for line in fp:
                line_split = line.split(',')
                # print(line_split)
                try :
                    if(line_split[0]=='MM/dd/yyyy'):
                        self.num_test+=1
                        self.data_idx.append(idx_temp)
                        self.ACH.append([])
                    ts = datetime.strptime(' '.join(line_split[0:2]),'%m/%d/%Y %H:%M:%S')
                    self.time.append(ts)
                    self.c_raw.append(float(line_split[2].replace('\n','')))
                    idx_temp += 1
                except:
                    continue
            self.data_idx.append(idx_temp+1)
#             print(self.ACH)
            span_smooth = 61
            self.c = np.convolve(np.log(self.c_raw), np.ones((span_smooth,))/span_smooth, mode='same')
                    
    def print_data_summary(self):
        # print summary of raw data
        # the number of experiments in the file
        # minimum and maximum concentration of  each experiment
        print('# of test:', self.num_test)
        print('idx data:', self.data_idx)
        for i in range(self.num_test):
            print('  Test #: ',i+1)
            print('Min PM:', min(self.c_raw[self.data_idx[i]:self.data_idx[i+1]]))
            print('Max PM:', max(self.c_raw[self.data_idx[i]:self.data_idx[i+1]]))
            
    def plot_data(self):
        plt.plot(range(len(self.c)),np.log(self.c_raw))
        plt.plot(range(len(self.c)),self.c)
        plt.xlabel('Time [sec]')
        plt.ylabel('log(Concentration)')
        plt.title('Raw and smoothed data')
        plt.savefig(self.fname.replace('.csv','.png'))
        plt.cla()
#         plt.show()
        
        
    def minute_avg(self):
        raise Exception('Not implemented yet')
    
    def compute(self, target_test):
        if(target_test > self.num_test):
            raise Exception('Test number not valid')
        else:
            tt = self.time[self.data_idx[target_test-1]:self.data_idx[target_test]]
            cc = self.c[self.data_idx[target_test-1]:self.data_idx[target_test]]
        # print(len(tt),len(cc))
        id_max = np.argmax(cc)
        c_max = max(cc)
        len_data = len(cc)
        t_target = np.arange(1, len_data-id_max)
        c_target = cc[id_max+1:len_data+1]

        self.ACH[target_test-1]=(c_target - c_max)/t_target * -3600

    def plot_ACH(self,target_test):
        if(target_test > self.num_test):
            raise Exception('Test number not valid')
        
#             print(len(self.ACH[target_test-1]))
#             print(range(len(self.ACH[target_test-1])))
        plt.plot(range(len(self.ACH[target_test-1])),self.ACH[target_test-1])
        plt.xlabel('Time [sec]')
        plt.ylabel('ACH [1/hr]')
        # plt.show()
        plt.savefig(self.fname.replace('.csv','')+'_'+str(target_test)+'.png')
        plt.cla()
    
def compute_time_avg(self,num_test):
    raise Exception('Not implemented yet')
    
def plot_ACH_time_avg(self,num_test):
    raise Exception('Not implemented yet')
