import ACH
import os 

dir_in = './data/'
dir_out = './infiltration/'
if not os.path.exists(dir_out):
    os.mkdirs(dir_out)

fFileList = open(dir_out+'fileList.csv','w')
fFileList.write('FileNo., FileName \n')

fACHsummary = open(dir_out+'ACHsummary.csv','w')
fACHsummary.write('FileNo., TestNo., PM min, PM max, ACH min, ACH max, ACH mean, ACH std\n')

fileCount = 0
fileListDict = {}
for f_input in os.listdir(dir_in):
    if '.csv' in f_input:
        fileCount += 1
        fileListDict[fileCount] = f_input
        fFileList.write(str(fileCount)+', '+str(f_input)+'\n')

        ACH_test = ACH.postProcess(f_input,dirInput=dir_in,dirOutput=dir_out)
        ACH_test.plotRaw()

        fACHsummary.write('%7d, %7d, %6.2f, %6.2f \n' \
            %(fileCount,1,ACH_test.cRawMinMax[0][0], ACH_test.cRawMinMax[0][1]) )
        
        # actual tests
        for i in range(2,ACH_test.numTest+1):
            ACH_test.compute(i)
            ACH_test.plot(i)
            ACH_range = ACH_test.getACH(i)
            fACHsummary.write('%7d, %7d, %6.2f, %6.2f,' \
                %(fileCount,i,ACH_test.cRawMinMax[i-1][0], ACH_test.cRawMinMax[i-1][1]) )
            fACHsummary.write('%7.2f, %7.2f, %8.2f, %7.2f \n' \
                %(ACH_range.min(),ACH_range.max(),ACH_range.mean(),ACH_range.std() ))
            
            
        # print(ACH_test)


fFileList.close()
fACHsummary.close()