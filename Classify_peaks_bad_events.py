import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm 
import statistics 
from scipy.signal import find_peaks
from math import floor
from math import ceil

def classify_peaks_bad_events(flip_axle_cm: np.ndarray, file_path: str) :
    
    path_component = (file_path.split("\\"))
    date_tag = path_component[1]+" | "+path_component[-2]

    print(flip_axle_cm)
    # # plot Axle
    # fig, axs = plt.subplots(4, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [1, 1, 1, 1]})
    # fig.canvas.manager.set_window_title(date_tag)
    # fig.tight_layout(pad=2)
    # topgraph_flip_axle_cm = max([ max(flip_axle_cm[:,i]) for i in range(2)])
    # axs[0].plot(flip_axle_cm)
    # # axs[0].set_ylim(0, topgraph_flip_axle_cm )
    # # axs[0].set_yticks(np.arange(0, topgraph_flip_axle_cm, step=250))
    # axs[0].legend(list(map(str, [1,2])),bbox_to_anchor=(1, 0.75), loc='upper right')
    # time_range= [range(0, flip_axle_cm.shape[0])]

    # # scatter plot
    # axs[1].set_title("scatter plot Ax")
    # c=["C0", "C1"]*flip_axle_cm.shape[0]
    # axs[1].scatter(np.full_like(flip_axle_cm, np.transpose(time_range)),flip_axle_cm , c=c)

    # try:
    #     # distribution curve
    #     normal_distribution = np.sort(flip_axle_cm, axis=0)
    #     a0=normal_distribution[:,0]
    #     a1=normal_distribution[:,1]
    #     mean0 = statistics.mean(a0[a0>5])  # no need to sort
    #     sd0 = statistics.stdev(a0[a0>5])   # no need to sort
    #     mean1 = statistics.mean(a1[a1>5])  # no need to sort
    #     sd1 = statistics.stdev(a1[a1>5])   # no need to sort
    #     axs[2].plot(a0[a0>5] , norm.pdf(a0[a0>5], mean0, sd0), color='C0') 
    #     axs[2].plot(a1[a1>5] , norm.pdf(a1[a1>5], mean1, sd1), color='C1') 
    #     # histogram
    #     axs[3].hist(a0[a0>5], bins=25, density=True, alpha=0.6, color='C0')
    #     axs[3].hist(a1[a1>5], bins=25, density=True, alpha=0.6, color='C1')
    #     plt.show()
    # except Exception as e:
    #     print('Error = ', e)


    # plot peak
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [1, 1]})
    fig.canvas.manager.set_window_title(date_tag)
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
    # axs[1].plot(Ax2, color = "C0")
    axs[1].set_title("AX2")
    axs[1].plot(Ax2, "+", color = "C3")
    # bad condition
    bad_event_Ax2_peak, properties_bad_event_Ax2_peak = find_peaks(Ax2, prominence=(400, None),width=(None, 15))
    print(properties_bad_event_Ax2_peak)
    axs[1].plot(bad_event_Ax2_peak, Ax2[bad_event_Ax2_peak], "x", color = "C2")
    # Ax2[bad_event_Ax2_peak]=False
    
    # Ax2[bad_event_Ax2_peak]=Ax2[bad_event_Ax2_peak]-properties_bad_event_Ax2_peak["prominences"]
    for i in range(len(properties_bad_event_Ax2_peak["left_ips"])) :
        shift_down_range=Ax2[(floor(properties_bad_event_Ax2_peak["left_ips"][i])):ceil(properties_bad_event_Ax2_peak["right_ips"][i])]
        if Ax2[bad_event_Ax2_peak][i]-min(shift_down_range) < properties_bad_event_Ax2_peak["prominences"][i]:
            shift_down_range[:]=  min(shift_down_range)
        else :    
            shift_down_range[:]= Ax2[bad_event_Ax2_peak][i]-properties_bad_event_Ax2_peak["prominences"][i]


    # bad_event_Ax2_peak, properties_bad_event_Ax2_peak = find_peaks(Ax2, prominence=(400, None),width=(None, 7))
    # Ax2[bad_event_Ax2_peak]=False

    # wheel condition
    wheel_Ax2_peaks, wheel_bad_event_Ax2_peak = find_peaks(Ax2, prominence=(100, 600), width=20, distance=30)
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
    axs[1].plot(Ax2, color = "C0")

    plt.show()
    return


