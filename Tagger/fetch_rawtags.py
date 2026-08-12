import numpy as np
from Swabian import TimeTagger
from TimeTagger import Coincidence, CoincidenceTimestamp, FileWriter, TimeTagStream, Correlation, Counter
import time

#%% write raw time tags to a file on the local tagger machine
tagger = TimeTagger.createTimeTagger()


# Define the hardware settings here, such as trigger level or dead time. 
tagger.setTriggerLevel(channel=1, voltage=0.1)
tagger.setTriggerLevel(channel=2, voltage=0.1)
tagger.setTriggerLevel(channel=3, voltage=0.1)
tagger.setTriggerLevel(channel=4, voltage=0.1)

tagger.setDelayHardware(channel=1, delay=int(0000))
tagger.setDelayHardware(channel=2, delay=int(0000))
tagger.setDelayHardware(channel=3, delay=int(0000))
tagger.setDelayHardware(channel=4, delay=int(0000))

#Enable the software ReferenceClock 
tagger.setReferenceClock(clock_channel=3, clock_frequency=10e6, time_constant = 1e-3, wait_until_locked=True)


ch = [1,-1,2] # -1 means the falling edge

for c in ch:
    #initiate input delays to 0 for all channels 
    tagger.setInputDelay(c, int(0))
    
    
ct = time.strftime("%d%m%Y_%H%M%S")
f = "C:\\Users\\admin\\Documents\\code\\Tagger\\Data\\Displacement\\Rawtags\\timetags_07212026" #This gives the file title for data save as .ttbin format
filewriter = TimeTagger.FileWriter(tagger=tagger,
                                   filename=f,
                                   channels=ch)
filewriter.start()
while True:
    try: 
        pass
    except KeyboardInterrupt():
        filewriter.stop()
        TimeTagger.freeTimeTagger(tagger)

#can also use to run a timed measurement
#filewriter.startFor(int(30e12))
#filewriter.stop()
#TimeTagger.freeTimeTagger(tagger)

# %%
