import os
import numpy as np
import matplotlib.pyplot as plt

# print("Current Working Directory:", os.getcwd())

# loop read event
event_raining_path = "to Peiam/bad_events_raining/20240912_022716_2/event.txt"
file = open(event_raining_path, 'r')

# cut
lines = file.readlines()
usedline = lines[2:-1]

usedData = []
for i in usedline:
    usedData.append((i.strip()).split("\t"))
signalArray = np.array(usedData,dtype=float)


FULL_uV_Exact_Channel_list = [1, 2, 9, 13, 14, 21]
FULL_uV = np.stack( (signalArray[:, [i-1 for i in FULL_uV_Exact_Channel_list]] ) )
# print(FULL_uV.shape, FULL_uV)

Start_FULL_uV = np.full_like(FULL_uV, FULL_uV[0,:])
# print(Start_FULL_uV.shape, Start_FULL_uV)

Calibrate_FULL_uV = FULL_uV - Start_FULL_uV

Axle_cm = signalArray[:,-4:-2]
# print(Axle_cm.shape, Axle_cm)

fig, axs = plt.subplots(2, 1, figsize=(8, 7), gridspec_kw={'height_ratios': [2, 1]})
# fig.tight_layout(pad=3)
axs[0].plot(Calibrate_FULL_uV)
axs[0].set_title("Strain Event :2", fontweight="bold")
axs[0].set_ylabel('FULL_uV')
axs[0].set_xticklabels([])
axs[0].legend(list(map(str, FULL_uV_Exact_Channel_list)),bbox_to_anchor=(1.01, 0.75), loc='upper left')

axs[1].plot(Axle_cm)
axs[1].set_ylim(0,750)
axs[1].set_ylabel('Axle_cm')
axs[1].legend(list(map(str, [1,2])),bbox_to_anchor=(1.01, 0.75), loc='upper left')

plt.show()



