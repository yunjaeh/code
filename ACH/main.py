import ACH
import os 

dir_raw = './data/'
dir_fig = './infiltration/'
fileListDict = {}

fileCount = 0
for f_input in os.listdir(dir_raw):
    if '.csv' in f_input:
        fileCount += 1
        fileListDict[fileCount] = f_input

        ACH_test = ACH.postProcess(f_input,dirData=dir_raw,dirFig=dir_fig)
        ACH_test.plotRaw()
        for i in range(2,ACH_test.numTest+1):
            ACH_test.compute(i)
            ACH_test.plot(i)
            ACH_range = ACH_test.getACH(i)
        print(ACH_test)
