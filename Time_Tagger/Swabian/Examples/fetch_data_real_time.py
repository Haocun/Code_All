# -*- coding: utf-8 -*-
"""
Modified based on Doroteas' code on Mon Apr 22 2025

@author: tea
"""
import os
import numpy as np
from Swabian import TimeTagger
from TimeTagger import TimeTaggerBase, Coincidence, Coincidences, CoincidenceTimestamp, FileReader, TimeTagStream, Correlation, Counter, DelayedChannel
import time
import csv 

s_to_ps = lambda s: s*1e12
ps_to_s = lambda p: p*1e-12

bw = 0.1

#connect to network time tagger
tagger = TimeTagger.createTimeTagger()
tagger.setHardwareBufferSize(536870912) # was 67108864(536870912)

#frequency_channel = 1 
#PPS_channel = 2 
# Define the hardware settings here, such as trigger level or dead time. 

tagger.setTriggerLevel(channel=1, voltage=0.1)
tagger.setTriggerLevel(channel=2, voltage=0.1)
tagger.setTriggerLevel(channel=3, voltage=0.1)
tagger.setTriggerLevel(channel=4, voltage=0.1)

tagger.setDelayHardware(channel=1, delay=int(0000))
tagger.setDelayHardware(channel=2, delay=int(0000))
tagger.setDelayHardware(channel=3, delay=int(0000))
tagger.setDelayHardware(channel=4, delay=int(0000))
# Enable the ReferenceClock 
# tagger.setReferenceClock(clock_channel=frequency_channel, clock_frequency=10e6, time_constant = 1e-3, synchronization_channel=2, wait_until_locked=True)

# Active channels for this measurement
ch =[1, 2]

counter = TimeTagger.Counter(tagger=tagger, channels=ch, binwidth=s_to_ps(bw), n_values=100)

fname = f'type0_0.1s_0506.csv'
with open(fname, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["Time(s)", "CH1", "CH2"])
time.sleep(2)

with open(fname, mode="a", newline="") as file:
    writer = csv.writer(file)

    start_time = time.time()
    while True:
        count_obj = counter.getDataObject(remove=True)
        t = (count_obj.getTime())*1e-12
        #counts = count_obj.getData()
        counts = count_obj.getDataNormalized()

        #save the new data
        arr = np.vstack([t, counts]).T
        writer.writerows(arr)
        file.flush() #Flush the buffer so Windows sees the update

        dt = (time.time() - start_time)
        print(dt)

        if dt >= 3:
            break
        #time.sleep(0.3)
        
        #tagger.getOverflowsAndClear()

