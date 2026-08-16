# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 10:41:54 2025

@author: tea
"""

import numpy as np
import matplotlib.pyplot as plt 
import TimeTagger
from TimeTagger import Coincidence, CoincidenceTimestamp, FileWriter, TimeTagStream, Correlation, Counter
import time
import scipy as sci

#%% write time tags to a file on the local tagger machine
ch = [3,4,7,8,9,10]
tagger = TimeTagger.createTimeTagger()

for c in ch:
    #initiate input delays to 0 for all channels 
    tagger.setInputDelay(c, int(0))
    
    
ct = time.strftime("%d%m%Y_%H%M%S")
f = "D:\\0511_2\\timetags_11052025_2"
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
#can also use 
#filewriter.startFor(int(30e12))
 #trun a timed measurement 
#filewriter.stop()
#TimeTagger.freeTimeTagger(tagger2)
