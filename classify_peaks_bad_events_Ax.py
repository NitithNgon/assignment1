import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from shift_down_bad_events import *

def classify_peaks_bad_events_Ax( Ax: np.ndarray, axs: np.ndarray[plt.Axes], axs_num: int) -> int:

    # plot peak Ax
    axs[axs_num].set_xlabel('time-ms.')
    axs[axs_num].set_ylabel('Axle-cm.')
    axs[axs_num].plot(Ax, "+", color = "C3")

    # bad condition
    bad_event_Ax_peak, properties_bad_event_Ax_peak = find_peaks(Ax, prominence=(50, None), width=(None, 15))
    axs[axs_num].plot(bad_event_Ax_peak, Ax[bad_event_Ax_peak], "x", color = "C2")

    # print("shift_down_bad_events")
    num_of_bad_event_peaks = shift_down_bad_events(bad_event_Ax_peak, properties_bad_event_Ax_peak, Ax)

    bad_event_above_wheel_Ax_peak, properties_bad_event_above_wheel_Ax_peak = find_peaks(Ax, prominence=(30, None), width=(None, 15), rel_height=0.05)
    axs[axs_num].plot(bad_event_above_wheel_Ax_peak, Ax[bad_event_above_wheel_Ax_peak], "x", color = "C4")
    axs[axs_num].vlines(x=bad_event_above_wheel_Ax_peak, ymin=Ax[bad_event_above_wheel_Ax_peak] - 1*properties_bad_event_above_wheel_Ax_peak["prominences"],
                ymax = Ax[bad_event_above_wheel_Ax_peak], color = "C4")
    
    # print("shift_down_bad_events_above_wheel")
    num_of_bad_event_above_wheel_peaks = shift_down_bad_events(bad_event_above_wheel_Ax_peak, properties_bad_event_above_wheel_Ax_peak, Ax)

    wheel_Ax_peaks, properties_wheel_bad_event_Ax_peak = find_peaks(Ax, prominence=(100, 800), width=(30, 200), distance=20)
    axs[axs_num].plot(wheel_Ax_peaks, Ax[wheel_Ax_peaks], "x", color = "C1")
    axs[axs_num].vlines(x=wheel_Ax_peaks, ymin=Ax[wheel_Ax_peaks] - properties_wheel_bad_event_Ax_peak["prominences"],
                ymax = Ax[wheel_Ax_peaks], color = "C1")
    axs[axs_num].hlines(y=properties_wheel_bad_event_Ax_peak["width_heights"], xmin=properties_wheel_bad_event_Ax_peak["left_ips"],
                xmax=properties_wheel_bad_event_Ax_peak["right_ips"], color = "C1")
    try:
        axs[axs_num].hlines(y=properties_wheel_bad_event_Ax_peak["width_heights"].mean() -15, xmin=(properties_wheel_bad_event_Ax_peak["left_ips"])[0],
                    xmax=(properties_wheel_bad_event_Ax_peak["right_ips"])[-1], color = "C3")
    except Exception as e:
        print('Error = ', e)
    axs[axs_num].plot(Ax, color = "C0")

    return num_of_bad_event_peaks + num_of_bad_event_above_wheel_peaks


