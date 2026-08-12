#%%
import numpy as np
import TimeTagger
from TimeTagger import Coincidences, Counter
import csv 
from datetime import timedelta
import time

#create save file with header
save_file = "..\\Timetagger\\type0_source\\dt0613\\data_680ps_cc_1.csv"
header_row = [f'CH3, CH4, CH7, CH8, CH9, CH10, CC37, CC38, CC39, CC310, CC47, CC48, CC49, CC410']
with open(save_file, 'w') as file:
    writer = csv.writer(file)

    writer.writerow(header_row)
del file

#%%
s_to_ps = lambda s: s*1e12
ps_to_s = lambda p: p*1e-12

# common variables
output_channels = [3, 4]
herald_channels = [7, 8, 9, 10]
cc_grp = [[3,7],[3,8],[3,9],[3,10],[4,7],[4,8],[4,9],[4,10]]

cc_binw = s_to_ps(.1) # how long to integrate over 
cc_bins = 8000 # number of bins that can be stored in the counter at a time 


#%%
tt_file = "..\\Timetagger\\type0_source\\dt0613\\0613tags.1.ttbin" #base filename

tagger = TimeTagger.createTimeTaggerVirtual(tt_file, begin=0e12, duration=-1)

# for 0613
tagger.setInputDelay(3, 4013)
tagger.setInputDelay(4, 00)
tagger.setInputDelay(7, 247165581)
tagger.setInputDelay(8, 247165541)
tagger.setInputDelay(9, 247165545)
tagger.setInputDelay(10, 247165620)

cc_ch = Coincidences(tagger, cc_grp, coincidenceWindow=680)
coinc_channels =  list(cc_ch.getChannels())
meas_channels = output_channels + herald_channels + coinc_channels

tstart = time.time()

#create the counter measurement 
counter = Counter(tagger, meas_channels, cc_binw, cc_bins)

tagger.run(speed=-1.0)
#tagger.waitUntilFinished(timeout=-1)

#save data while replaying 
print('replaying')
start_time = time.time()
ii=1
while not tagger.waitForCompletion(timeout=0):
    count_obj = counter.getDataObject()
    if count_obj.size > 600:
        #get data from buffer and write to file
        count_obj = counter.getDataObject(remove=True)
        times = count_obj.getTime()*1e-12
        counts = count_obj.getDataNormalized()
        arr = np.vstack([times, counts]).T  

        with open(save_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(arr)

        elapsed = time.time() - start_time
        print(f"{time.strftime('%H:%M:%S', time.gmtime(elapsed))} — 1min saving -{ii} ")
        ii+=1
    else:
        pass
#once done write the last few rows of data 
times = count_obj.getTime()*1e-12
counts = count_obj.getDataNormalized()
arr = np.vstack([times, counts]).T  

with open(save_file, mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(arr)

total_time = str(timedelta(seconds = times[-1]))
print(f"Done reading file. Length of data collected: {total_time} ")

tend = time.time()

print(tend-tstart)

TimeTagger.freeTimeTagger(tagger)

# %%
