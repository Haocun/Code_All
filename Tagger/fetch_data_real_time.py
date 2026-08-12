# -*- coding: utf-8 -*-
"""
Modified based on Doroteas' code on Mon Apr 22 2025

@author: tea
"""
import os
import numpy as np
import TimeTagger
from TimeTagger import TimeTaggerBase, Coincidence, Coincidences, CoincidenceTimestamp, FileReader, TimeTagStream, Correlation, Counter, DelayedChannel
import time
import csv 

#from qubib.devices.swabian_instruments.TimeTaggerSwabian import TimeTaggerSwabian

s_to_ps = lambda s: s*1e12
ps_to_s = lambda p: p*1e-12

#connect to network time tagger
#tagger = TimeTagger.createTimeTaggerNetwork('10.42.0.134')
tagger = TimeTagger.createTimeTagger()
tagger.setHardwareBufferSize(536870912) # was 67108864(536870912)

#frequency_channel = 1 
#PPS_channel = 2 
# Define the hardware settings here, such as trigger level or dead time. 
tagger.setTriggerLevel(channel=3, voltage=0.5)
tagger.setTriggerLevel(channel=4, voltage=0.5)
tagger.setTriggerLevel(channel=7, voltage=0.3)
tagger.setTriggerLevel(channel=8, voltage=0.3)
tagger.setTriggerLevel(channel=9, voltage=0.3)
tagger.setTriggerLevel(channel=10, voltage=0.3)
# Enable the ReferenceClock 
#tagger.setReferenceClock(clock_channel=frequency_channel, clock_frequency=10e6, time_constant = 1e-3, synchronization_channel=2, wait_until_locked=True)

#print(tagger.getHardwareBufferSize())

#cd = time.strftime("%d%m%Y") #today's date
#print(tagger.get_model())
#active channels for this measurement

#tagger.setDelayHardware(channel=3, delay=00)
#tagger.setDelayHardware(channel=4, delay=int(0000)) #3400
#tagger.setDelayHardware(channel=5, delay=int(0000))
#tagger.setDelayHardware(channel=6, delay=int(0000))


#tagger.setHardwareBufferSize(512)
#channels = [3,4,7,8,9,10]

#tagger.setInputDelay(3, 3900)
#for ch in [7,8,9,10]: 
#    tagger.setInputDelay(ch, 247151200)

#tagger.setConditionalFilter(trigger=[7], filtered=[8,9,10])

bw = 0.1
#cc_grp = [[3,7],[3,8],[3,9],[3,10],[4,7],[4,8],[4,9],[4,10]]
#cc_ch = Coincidences(tagger, cc_grp, coincidenceWindow=1000)

#tot_ch = [*channels, *cc_ch.getChannels()]


#tagger.setHardwareBufferSize(512)

ch3_delay = DelayedChannel(tagger, input_channel=3, delay = 3900)
ch7_delay = DelayedChannel(tagger, input_channel=7, delay = 247151200) #2.47153e8 for type2
ch8_delay = DelayedChannel(tagger, input_channel=8, delay = 247151200) #2.47153e8
ch9_delay = DelayedChannel(tagger, input_channel=9, delay = 247151200) #2.47153e8
ch10_delay = DelayedChannel(tagger, input_channel=10, delay = 247151200) #2.47153e8
ch3d = ch3_delay.getChannel()
ch7d = ch7_delay.getChannel()
ch8d = ch8_delay.getChannel()
ch9d = ch9_delay.getChannel()
ch10d = ch10_delay.getChannel()

#active channels for this measurement
ch =[3,4,7,8,9,10]
cc_grp = [[ch3d,ch7d],[ch3d,ch8d],[ch3d,ch9d],[ch3d,ch10d],[4,ch7d],[4,ch8d],[4,ch9d],[4,ch10d]]
cc_ch = Coincidences(tagger, cc_grp, coincidenceWindow=1500)
tot_ch = ch+list(cc_ch.getChannels())

bw = 0.1
counter = TimeTagger.Counter(tagger=tagger, channels=tot_ch, binwidth=s_to_ps(bw), n_values=100)

fname = f'type0_0.1s_0506.csv'
with open(fname, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["Time(s)", "CH3", "CH4", "CH7", "CH8", "CH9", "CH10", "CC3-7", "CC3-8","CC3-9","CC3-10","CC4-7", "CC4-8","CC4-9","CC4-10"])
time.sleep(2)
#n_cyl = 10*3600*10
#for  _ in range(n_cyl):

with open(fname, mode="a", newline="") as file:
    writer = csv.writer(file)

    while True:
        count_obj = counter.getDataObject(remove=True)
        t = (count_obj.getTime())*1e-12
        #counts = count_obj.getData()
        counts = count_obj.getDataNormalized()

        #save the new data
        arr = np.vstack([t, counts]).T
        writer.writerows(arr)
        file.flush() #Flush the buffer so Windows sees the update
            #os.fsync(file.fileno()) 
        #time.sleep(0.3)
        
        #tagger.getOverflowsAndClear()

