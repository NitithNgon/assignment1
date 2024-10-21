import numpy as np
from math import floor
from math import ceil

MIN_RAIN_PROMINENCE = 50

def shift_down_bad_events(bad_event_peak: dict, properties_bad_event_peak: dict, Ax: np.ndarray) -> int:
    num_of_bad_event_peaks=len(properties_bad_event_peak["width_heights"])
    for i in range(num_of_bad_event_peaks) :
            shift_down_range=Ax[floor(properties_bad_event_peak["left_ips"][i]):ceil(properties_bad_event_peak["right_ips"][i])]
            if abs(Ax[floor(properties_bad_event_peak["left_ips"][i])] -Ax[ceil(properties_bad_event_peak["right_ips"][i])]) < MIN_RAIN_PROMINENCE :
                if Ax[bad_event_peak][i]-min(shift_down_range) < properties_bad_event_peak["prominences"][i]:
                    shift_down_range[:]= min(shift_down_range)
                    # print("x")
                else:    
                    shift_down_range[:]= Ax[bad_event_peak][i]-properties_bad_event_peak["prominences"][i]
                    # print("y")
            else:
                 shift_down_range[:]= max(Ax[floor(properties_bad_event_peak["left_ips"][i])], Ax[ceil(properties_bad_event_peak["right_ips"][i])])
                #  print("z")
    return num_of_bad_event_peaks