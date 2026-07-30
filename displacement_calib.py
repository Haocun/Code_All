#%%
from Swabian import TimeTagger
from TimeTagger import TimeTaggerBase, Coincidence, Coincidences, CoincidenceTimestamp, FileReader, TimeTagStream, Correlation, Counter, DelayedChannel
import numpy as np
import time
import csv 


s_to_ps = lambda s: s*1e12
ps_to_s = lambda p: p*1e-12


tt_file = "C:\\Users\\admin\\Documents\\code\\Tagger\\Data\\Displacement\\Rawtags\\timetags_07212026.ttbin" #base filename

tagger = TimeTagger.createTimeTaggerVirtual(tt_file, begin=0, duration=-1)

tagger.setInputDelay(1, 0)
tagger.setInputDelay(2, 0)

n_gates_max = 1_000_000

gate_counter = TimeTagger.CountBetweenMarkers(
    tagger=tagger,
    click_channel=2,    # count photons on Channel 2
    begin_channel=1,    # Ch1 rising edge opens gate
    end_channel=-1,     # Ch1 falling edge closes gate
    n_values=n_gates_max,
)

tagger.run(speed=-1.0)
tagger.waitUntilFinished()

photon_counts = np.asarray(gate_counter.getData())
gate_start_ps = np.asarray(gate_counter.getIndex())
gate_width_ps = np.asarray(gate_counter.getBinWidths())

valid = gate_width_ps > 0

counts = photon_counts[valid]
gate_start_ps = gate_start_ps[valid]
gate_width_ps = gate_width_ps[valid]

print(counts)

#%%create save file with header
save_file = "C:\\Users\\admin\\Documents\\code\\Tagger\\Data\\Displacement\\data.csv" #This gives the file title for data save as .ttbin format
header_row = [
            f"gate_index",
            "gate_start_ps",
            "gate_start_s",
            "gate_width_ps",
            "gate_width_s",
            "ch2_photon_number",
        ])
with open(save_file, 'w') as file:
    writer = csv.writer(file)

    writer.writerow(header_row)
del file



    

    
TimeTagger.freeTimeTagger(tagger)
# %%
