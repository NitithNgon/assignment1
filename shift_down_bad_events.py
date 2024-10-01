import numpy as np
from math import floor
from math import ceil

def shift_down_bad_events(bad_event_peak: dict, properties_bad_event_peak: dict, Ax: np.ndarray):
    for i in range(len(properties_bad_event_peak["left_ips"])) :
            shift_down_range=Ax[floor(properties_bad_event_peak["left_ips"][i]):ceil(properties_bad_event_peak["right_ips"][i])]
            if abs(Ax[floor(properties_bad_event_peak["left_ips"][i])] -Ax[ceil(properties_bad_event_peak["right_ips"][i])]) <50 :
                if Ax[bad_event_peak][i]-min(shift_down_range) < properties_bad_event_peak["prominences"][i]:
                    shift_down_range[:]= min(shift_down_range)
                    print("x")
                else:    
                    shift_down_range[:]= Ax[bad_event_peak][i]-properties_bad_event_peak["prominences"][i]
                    print("y")
            else:
                 shift_down_range[:]= max(Ax[floor(properties_bad_event_peak["left_ips"][i])], Ax[ceil(properties_bad_event_peak["right_ips"][i])])
                 print("z")
    return