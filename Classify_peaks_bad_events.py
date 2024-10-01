import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths
from math import floor
from math import ceil
from shift_down_bad_events import *

def classify_peaks_bad_events(flip_axle_cm: np.ndarray, file_path: str) :

    path_component = (file_path.split("\\"))
    date_tag = path_component[1]+" | "+path_component[-2]

    # plot peak
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [1, 1]})
    fig.canvas.manager.set_window_title(date_tag)
    fig.tight_layout(pad=2)

    # plot peak Ax1
    Ax1=flip_axle_cm[:,0]
    axs[0].set_title("AX1")
    axs[0].plot(Ax1, "+", color = "C3")

    # bad condition
    bad_event_Ax1_peak, properties_bad_event_Ax1_peak = find_peaks(Ax1, prominence=(50, None), width=(None, 15))
    axs[0].plot(bad_event_Ax1_peak, Ax1[bad_event_Ax1_peak], "x", color = "C2")
    print("shift_down_bad_events")
    shift_down_bad_events(bad_event_Ax1_peak, properties_bad_event_Ax1_peak, Ax1)

    bad_event_above_wheel_Ax1_peak, properties_bad_event_above_wheel_Ax1_peak = find_peaks(Ax1, prominence=(30, None), width=(None, 15), rel_height=0.1)
    axs[0].plot(bad_event_above_wheel_Ax1_peak, Ax1[bad_event_above_wheel_Ax1_peak], "x", color = "C4")
    axs[0].vlines(x=bad_event_above_wheel_Ax1_peak, ymin=Ax1[bad_event_above_wheel_Ax1_peak] - 1*properties_bad_event_above_wheel_Ax1_peak["prominences"],
                ymax = Ax1[bad_event_above_wheel_Ax1_peak], color = "C4")
    print("shift_down_bad_events_above_wheel")
    shift_down_bad_events(bad_event_above_wheel_Ax1_peak, properties_bad_event_above_wheel_Ax1_peak, Ax1)

    wheel_Ax1_peaks, properties_wheel_bad_event_Ax1_peak = find_peaks(Ax1, prominence=(100, 800), width=(30, 150), distance=20)
    axs[0].plot(wheel_Ax1_peaks, Ax1[wheel_Ax1_peaks], "x", color = "C1")
    axs[0].vlines(x=wheel_Ax1_peaks, ymin=Ax1[wheel_Ax1_peaks] - properties_wheel_bad_event_Ax1_peak["prominences"],
                ymax = Ax1[wheel_Ax1_peaks], color = "C1")
    axs[0].hlines(y=properties_wheel_bad_event_Ax1_peak["width_heights"], xmin=properties_wheel_bad_event_Ax1_peak["left_ips"],
                xmax=properties_wheel_bad_event_Ax1_peak["right_ips"], color = "C1")
    try:
        axs[0].hlines(y=properties_wheel_bad_event_Ax1_peak["width_heights"].mean() -15, xmin=(properties_wheel_bad_event_Ax1_peak["left_ips"])[0],
                    xmax=(properties_wheel_bad_event_Ax1_peak["right_ips"])[-1], color = "C3")
    except Exception as e:
        print('Error = ', e)
    axs[0].plot(Ax1, color = "C0")


    # plot peak Ax2
    Ax2=flip_axle_cm[:,1]
    axs[1].set_title("AX2")
    axs[1].plot(Ax2, "+", color = "C3")

    # bad condition
    bad_event_Ax2_peak, properties_bad_event_Ax2_peak = find_peaks(Ax2, prominence=(50, None), width=(None, 15))
    axs[1].plot(bad_event_Ax2_peak, Ax2[bad_event_Ax2_peak], "x", color = "C2")
    print("shift_down_bad_events")
    shift_down_bad_events(bad_event_Ax2_peak, properties_bad_event_Ax2_peak, Ax2)

    bad_event_above_wheel_Ax2_peak, properties_bad_event_above_wheel_Ax2_peak = find_peaks(Ax2, prominence=(30, None), width=(None, 15), rel_height=0.1)
    axs[1].plot(bad_event_above_wheel_Ax2_peak, Ax2[bad_event_above_wheel_Ax2_peak], "x", color = "C4")
    axs[1].vlines(x=bad_event_above_wheel_Ax2_peak, ymin=Ax2[bad_event_above_wheel_Ax2_peak] - 1*properties_bad_event_above_wheel_Ax2_peak["prominences"],
                ymax = Ax2[bad_event_above_wheel_Ax2_peak], color = "C4")
    print("shift_down_bad_events_above_wheel")
    shift_down_bad_events(bad_event_above_wheel_Ax2_peak, properties_bad_event_above_wheel_Ax2_peak, Ax2)

    wheel_Ax2_peaks, properties_wheel_bad_event_Ax2_peak = find_peaks(Ax2, prominence=(100, 800), width=(30, 150), distance=20)
    axs[1].plot(wheel_Ax2_peaks, Ax2[wheel_Ax2_peaks], "x", color = "C1")
    axs[1].vlines(x=wheel_Ax2_peaks, ymin=Ax2[wheel_Ax2_peaks] - properties_wheel_bad_event_Ax2_peak["prominences"],
                ymax = Ax2[wheel_Ax2_peaks], color = "C1")
    axs[1].hlines(y=properties_wheel_bad_event_Ax2_peak["width_heights"], xmin=properties_wheel_bad_event_Ax2_peak["left_ips"],
                xmax=properties_wheel_bad_event_Ax2_peak["right_ips"], color = "C1")
    try:
        axs[1].hlines(y=properties_wheel_bad_event_Ax2_peak["width_heights"].mean() -15, xmin=(properties_wheel_bad_event_Ax2_peak["left_ips"])[0],
                    xmax=(properties_wheel_bad_event_Ax2_peak["right_ips"])[-1], color = "C3")
    except Exception as e:
        print('Error = ', e)
    axs[1].plot(Ax2, color = "C0")
    plt.show()

    return


