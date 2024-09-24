import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm 
import statistics 
from scipy.signal import find_peaks

# print("current working directory:", os.getcwd())
# loop read event
# c:\users\eei-0\desktop\assignment1\to_peiam\bad_events_dirty_ax\20240409_085745_4
# c:\users\eei-0\desktop\assignment1\to_peiam\bad_events_raining\20240912_023357_1
# c:\users\eei-0\desktop\assignment1\to_peiam\bad_events_raining\20240912_022716_2
event_path = "to_peiam/bad_events_raining/20240912_022716_2/event.txt"
file = open(event_path, 'r')

# cut lines
lines = file.readlines()
usedline = lines[2:-1]

used_data = []
for i in usedline: used_data.append((i.strip()).split("\t"))
signal_array = np.array(used_data,dtype=float)


# input channel
full_u_v_exact_channel_list_dirty_ax = np.array([1, 2, 3, 4, 5, 6])       # bad_events_dirty_ax/20240409_085745_4
full_u_v_exact_channel_list_raining = np.array([1, 2, 9, 13, 14, 21])    # bad_events_raining/20240912_022716_2
full_u_v_exact_channel_list = full_u_v_exact_channel_list_raining
axle_cm_direction = 1                                                   # 0 or 1

# zero shift initial point
full_u_v = signal_array[:, full_u_v_exact_channel_list-1 ]
start_full_u_v = full_u_v[0,:]
calibrate_full_u_v = full_u_v - start_full_u_v

axle_cm_exact_channel_list = [[-2,-1],[-4,-3]]      # last 4 channels are ax
axle_cm = signal_array[:, axle_cm_exact_channel_list[axle_cm_direction] ]
min_top_flatline_ax = min(axle_cm.max(axis=0))      # minimum top flat line of all ax
print(calibrate_full_u_v.shape, calibrate_full_u_v)
print(axle_cm.shape, axle_cm)


fig, axs = plt.subplots(2, 1, figsize=(8, 7), gridspec_kw={'height_ratios': [2, 1]})
# fig.tight_layout(pad=3)
axs[0].plot(calibrate_full_u_v)
axs[0].set_title("strain event :2", fontweight="bold")
axs[0].set_ylabel('full_u_v')
axs[0].set_xticklabels([])
axs[0].legend(list(map(str, full_u_v_exact_channel_list)),bbox_to_anchor=(1.01, 0.75), loc='upper left')

axs[1].plot(axle_cm)
axs[1].set_ylim(0, min_top_flatline_ax )
axs[1].set_yticks(np.arange(0, min_top_flatline_ax, step=250))
axs[1].set_ylabel('axle_cm')
axs[1].legend(list(map(str, [1,2])),bbox_to_anchor=(1.01, 0.75), loc='upper left')
plt.show()



fig, axs = plt.subplots(4, 1, figsize=(16, 8), gridspec_kw={'height_ratios': [1, 1, 1, 1]})
fig.tight_layout(pad=1)
flip_axle_cm = min_top_flatline_ax - axle_cm
topgraph_flip_axle_cm = max([ max(flip_axle_cm[:,i]) for i in range(2)])
axs[0].plot(flip_axle_cm)
axs[0].set_ylim(0, topgraph_flip_axle_cm )
axs[0].set_yticks(np.arange(0, topgraph_flip_axle_cm, step=250))

time_range= [range(0, flip_axle_cm.shape[0])]
# plot two Axle
# axs[1].scatter(np.full_like(flip_axle_cm, np.transpose(time_range)),flip_axle_cm)
# plot one AXle
axs[1].scatter(np.transpose(time_range),flip_axle_cm[:,1])


# distribution curve
normal_distribution = np.sort(flip_axle_cm, axis=0)
a=normal_distribution[:,1]
mean = statistics.mean(a[a>5])  # no need to sort
sd = statistics.stdev(a[a>5])   # no need to sort
print(mean,sd)
axs[2].plot(a[a>5] , norm.pdf(a[a>5], mean, sd)) 

# histogram
# axs[3].hist(a[a>5], bins=25, density=True, alpha=0.6, color='b')

# plot peak
b=flip_axle_cm[:,1]
peaks, properties = find_peaks(b, prominence=(400, None))
axs[3].plot(b)
axs[3].plot(peaks, b[peaks], "x")
plt.show()