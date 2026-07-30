#%%
import os
import numpy as np
from Swabian import TimeTagger
from TimeTagger import TimeTaggerBase, Coincidence, Coincidences, CoincidenceTimestamp, FileReader, TimeTagStream, Correlation, Counter, DelayedChannel
import time
import csv 

id = "2"

s_to_ps = lambda s: s*1e12
ps_to_s = lambda p: p*1e-12

bw = 0.1

#connect to network time tagger
tagger = TimeTagger.createTimeTagger()
tagger.setHardwareBufferSize(536870912) # was 67108864(536870912)

#frequency_channel = 1 
#PPS_channel = 2 
# Define the hardware settings here, such as trigger level or dead time. 

tagger.setTriggerLevel(channel=1, voltage=0.02)
tagger.setTriggerLevel(channel=2, voltage=0.1)
tagger.setTriggerLevel(channel=3, voltage=0.1)
tagger.setTriggerLevel(channel=4, voltage=0.1)

tagger.setDelayHardware(channel=1, delay=int(0000))
tagger.setDelayHardware(channel=2, delay=int(0000))
tagger.setDelayHardware(channel=3, delay=int(0000))
tagger.setDelayHardware(channel=4, delay=int(0000))

#Enable the software ReferenceClock 
tagger.setReferenceClock(clock_channel=3, clock_frequency=10e6, time_constant = 1e-3, wait_until_locked=True)
# Active channels for this measurement
ch =[1, 2]
n_gates_max = 1_000_000

counter = TimeTagger.Counter(tagger=tagger, channels=ch, binwidth=s_to_ps(bw), n_values=100)
gate_counter = TimeTagger.CountBetweenMarkers(
    tagger=tagger,
    click_channel=2,    # count photons on Channel 2
    begin_channel=1,    # Ch1 rising edge opens gate
    end_channel=-1,     # Ch1 falling edge closes gate
    n_values=n_gates_max,
)

fname = f'test_0730.csv'
with open(fname, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["Gate start time (ps)", "Gate width (ps)", "Count" ])
time.sleep(2)

with open(fname, mode="a", newline="") as file:
    writer = csv.writer(file)

    start_time = time.time()
    while True:

        gate_counts = gate_counter.getData()
        gate_start_ps = np.asarray(gate_counter.getIndex())
        gate_width_ps = np.asarray(gate_counter.getBinWidths())

        #save the new data
        arr = np.vstack([gate_start_ps, gate_width_ps, gate_counts]).T
        writer.writerows(arr)
        file.flush() #Flush the buffer so Windows sees the update
        #time.sleep(0.3)
        
        dt = time.time() - start_time

        print(dt)
        if dt >= 1:
            break
        #tagger.getOverflowsAndClear()




# %%
