


dat_temp    = readtable('data/night_WV_2.csv');
data.time   = datetime(dat_temp.Var2);
data.c      = dat_temp.Var3;

input_opt.minute_average = true;
ACH1 = ACH_concentration_decay(data, input_opt);