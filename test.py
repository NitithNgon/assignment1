import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm 
import statistics 
from scipy.signal import find_peaks

# print("current working directory:", os.getcwd())
# loop read event
# c:\users\eei-0\desktop\assignment1\to_Peiam\bad_events_dirtyAX\20240409_085745_4
# c:\users\eei-0\desktop\assignment1\to_Peiam\bad_events_raining\20240912_023357_1
# c:\users\eei-0\desktop\assignment1\to_Peiam\bad_events_raining\20240912_022716_2
event_path = "to_Peiam/bad_events_raining/20240912_022716_2/event.txt"
file = open(event_path, 'r')

# cut lines
lines = file.readlines()
usedline = lines[2:-1]

used_data = []
for i in usedline: used_data.append((i.strip()).split("\t"))
signal_array = np.array(used_data,dtype=float)


# input channel
full_u_v_exact_channel_list_dirty_ax = np.array([1, 2, 3, 4, 5, 6])     # bad_events_dirty_ax/20240409_085745_4
full_u_v_exact_channel_list_raining = np.array([1, 2, 9, 13, 14, 21])   # bad_events_raining/20240912_022716_2
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



# plot strain AX
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


# plot Axle
fig, axs = plt.subplots(4, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [1, 1, 1, 1]})
fig.tight_layout(pad=2)
flip_axle_cm = min_top_flatline_ax - axle_cm
topgraph_flip_axle_cm = max([ max(flip_axle_cm[:,i]) for i in range(2)])
axs[0].plot(flip_axle_cm)
axs[0].set_ylim(0, topgraph_flip_axle_cm )
axs[0].set_yticks(np.arange(0, topgraph_flip_axle_cm, step=250))
axs[0].legend(list(map(str, [1,2])),bbox_to_anchor=(1, 0.75), loc='upper right')
time_range= [range(0, flip_axle_cm.shape[0])]

# plot two Axle
# axs[1].scatter(np.full_like(flip_axle_cm, np.transpose(time_range)),flip_axle_cm)

# plot one AXle
selected_show_AX = 1
axs[1].set_title("Show AX"+str(selected_show_AX+1))
axs[1].scatter(np.transpose(time_range),flip_axle_cm[:,selected_show_AX])

# distribution curve
normal_distribution = np.sort(flip_axle_cm, axis=0)
a=normal_distribution[:,selected_show_AX]
mean = statistics.mean(a[a>5])  # no need to sort
sd = statistics.stdev(a[a>5])   # no need to sort
print("mean, SD =",mean,sd)
axs[2].plot(a[a>5] , norm.pdf(a[a>5], mean, sd)) 

# histogram
axs[3].hist(a[a>5], bins=25, density=True, alpha=0.6, color='b')

plt.show()





# plot peak
fig, axs = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [1, 1]})
fig.tight_layout(pad=2)



# plot peak Ax1
Ax1=flip_axle_cm[:,0]
axs[0].plot(Ax1, color = "C0")
axs[0].set_title("AX1")

# bad condition
bad_event_Ax1_peak, properties_bad_event_Ax1_peak = find_peaks(Ax1, prominence=(400, None))
axs[0].plot(bad_event_Ax1_peak, Ax1[bad_event_Ax1_peak], "x", color = "C2")

# wheel condition
wheel_Ax1_peaks, wheel_bad_event_Ax1_peak = find_peaks(Ax1, prominence=(100, None), width=20, distance=30)
axs[0].plot(wheel_Ax1_peaks, Ax1[wheel_Ax1_peaks], "x", color = "C1")
axs[0].vlines(x=wheel_Ax1_peaks, ymin=Ax1[wheel_Ax1_peaks] - wheel_bad_event_Ax1_peak["prominences"],
            ymax = Ax1[wheel_Ax1_peaks], color = "C1")
axs[0].hlines(y=wheel_bad_event_Ax1_peak["width_heights"], xmin=wheel_bad_event_Ax1_peak["left_ips"],
            xmax=wheel_bad_event_Ax1_peak["right_ips"], color = "C1")
try:
    axs[0].hlines(y=100, xmin=(wheel_bad_event_Ax1_peak["left_ips"])[0],
                xmax=(wheel_bad_event_Ax1_peak["right_ips"])[-1], color = "C3")
except Exception as e:
    print('Error = ', e)


# plot peak Ax2
Ax2=flip_axle_cm[:,1]
axs[1].plot(Ax2, color = "C0")
axs[1].set_title("AX2")

# bad condition
bad_event_Ax2_peak, properties_bad_event_Ax2_peak = find_peaks(Ax2, prominence=(400, None))
axs[1].plot(bad_event_Ax2_peak, Ax2[bad_event_Ax2_peak], "x", color = "C2")

# wheel condition
wheel_Ax2_peaks, wheel_bad_event_Ax2_peak = find_peaks(Ax2, prominence=(100, None), width=20, distance=30)
axs[1].plot(wheel_Ax2_peaks, Ax2[wheel_Ax2_peaks], "x", color = "C1")
axs[1].vlines(x=wheel_Ax2_peaks, ymin=Ax2[wheel_Ax2_peaks] - wheel_bad_event_Ax2_peak["prominences"],
            ymax = Ax2[wheel_Ax2_peaks], color = "C1")
axs[1].hlines(y=wheel_bad_event_Ax2_peak["width_heights"], xmin=wheel_bad_event_Ax2_peak["left_ips"],
            xmax=wheel_bad_event_Ax2_peak["right_ips"], color = "C1")
try:
    axs[1].hlines(y=100, xmin=(wheel_bad_event_Ax2_peak["left_ips"])[0],
                xmax=(wheel_bad_event_Ax2_peak["right_ips"])[-1], color = "C3")
except Exception as e:
    print('Error = ', e)


plt.show()
