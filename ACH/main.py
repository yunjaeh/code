import ACH
import os 

dir_raw = './'
for f_input in os.listdir(dir_raw):
    if '.csv' in f_input:
        print(f_input)
        ACH_test = ACH.ACH()
        ACH_test.read_input(dir_raw+f_input)
        ACH_test.plot_data()
        for i in range(2,ACH_test.num_test+1):
            print(i)
            ACH_test.compute(i)
            ACH_test.plot_ACH(i)




# file_test = 'Data_O_46-47-48_20181015.csv'
# ACH_test = ACH_process()
# ACH_test.read_input(file_test)
# ACH_test.print_data_summary()
# ACH_test.plot_raw()


