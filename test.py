import os
import numpy as np
import matplotlib.pyplot as plt

# print("Current Working Directory:", os.getcwd())

# loop read event

# C:\Users\eei-0\Desktop\assignment1\to_Peiam\bad_events_dirtyAX\20240409_085745_4
# C:\Users\eei-0\Desktop\assignment1\to_Peiam\bad_events_raining\20240912_023357_1
# C:\Users\eei-0\Desktop\assignment1\to_Peiam\bad_events_raining\20240912_022716_2
event_path = "to_Peiam/bad_events_dirtyAX/20240409_085745_4/event.txt"
file = open(event_path, 'r')

# cut lines
lines = file.readlines()
usedline = lines[2:-1]

usedData = []
for i in usedline: usedData.append((i.strip()).split("\t"))
signalArray = np.array(usedData,dtype=float)
print(signalArray[:,-4:])

FULL_uV_Exact_Channel_list_dirtyAX = np.array([1, 2, 3, 4, 5, 6])
FULL_uV_Exact_Channel_list = FULL_uV_Exact_Channel_list_dirtyAX
# FULL_uV_Exact_Channel_list = [1, 2, 9, 13, 14, 21]
FULL_uV = signalArray[:, FULL_uV_Exact_Channel_list_dirtyAX-1]
# print(FULL_uV.shape, FULL_uV)
Start_FULL_uV = np.full_like(FULL_uV, FULL_uV[0,:])
# print(Start_FULL_uV.shape, Start_FULL_uV)
Calibrate_FULL_uV = FULL_uV - Start_FULL_uV

Axle_cm_direction = 0 # 0 or 1
Axle_cm_Exact_Channel_list = [[-2,None],[-4,-2]]
Axle_cm = signalArray[:, Axle_cm_Exact_Channel_list[Axle_cm_direction][0]:Axle_cm_Exact_Channel_list[Axle_cm_direction][1] ]
print(Axle_cm.shape, Axle_cm)
Min_Top_Flatline_Ax = min([ max(Axle_cm[:,i]) for i in range(2)]) # minimum top flat line of all AX


fig, axs = plt.subplots(2, 1, figsize=(8, 7), gridspec_kw={'height_ratios': [2, 1]})
# fig.tight_layout(pad=3)
axs[0].plot(Calibrate_FULL_uV)
axs[0].set_title("Strain Event :2", fontweight="bold")
axs[0].set_ylabel('FULL_uV')
axs[0].set_xticklabels([])
axs[0].legend(list(map(str, FULL_uV_Exact_Channel_list)),bbox_to_anchor=(1.01, 0.75), loc='upper left')

axs[1].plot(Axle_cm)
axs[1].set_ylim(0, Min_Top_Flatline_Ax )
axs[1].set_yticks(np.arange(0, Min_Top_Flatline_Ax, step=250))
axs[1].set_ylabel('Axle_cm')
axs[1].legend(list(map(str, [1,2])),bbox_to_anchor=(1.01, 0.75), loc='upper left')
plt.show()



fig, axs = plt.subplots(1, 2, figsize=(16, 4), gridspec_kw={'width_ratios': [1, 1]})
fig.tight_layout(pad=1)
Flip_Axle_cm = Min_Top_Flatline_Ax - Axle_cm
topgraph_Flip_Axle_cm = max([ max(Flip_Axle_cm[:,i]) for i in range(2)])
axs[0].plot(Flip_Axle_cm)
axs[0].set_ylim(0, topgraph_Flip_Axle_cm )
axs[0].set_yticks(np.arange(0, topgraph_Flip_Axle_cm, step=250))


Time_range= [range(0, Flip_Axle_cm.shape[0])]
axs[1].scatter(np.full_like(Flip_Axle_cm, np.transpose(Time_range)),Flip_Axle_cm)
plt.show()