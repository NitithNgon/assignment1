import numpy as np
from math import floor
from math import ceil
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from typing import Optional
from typing import List

# depend on distance 
MIN_RAIN_PROMINENCE = 50
MIN_RAIN_ABOVE_WHEEL_PROMINENCE = 30
MIN_WHEEL_PROMINENCE = 100
MAX_WHEEL_PROMINENCE = 800
TOP_RAIN_PEAK = 0.05
# depend on rain speed, rain direction and sensor speed
MAX_RAIN_WIDTH = 15
# depend on vehicle speed, vehicle direction and sensor speed
MIN_WHEEL_WIDTH = 30
MAX_WHEEL_WIDTH = 200
# depend on wheel peak noise
MIN_WHEEL_PEAK_DISTANCE = 20
MAX_WHEEL_PEAK_DISTANCE = 100


def find_rain_drop(Ax: np.ndarray) -> np.ndarray|dict|int:
    # bad peaks
    bad_event_Ax_peak, properties_bad_event_Ax_peak = find_peaks(
        Ax,
        prominence=(MIN_RAIN_PROMINENCE, None),
        width=(None, MAX_RAIN_WIDTH),
    )
    num_of_bad_event_peaks = shift_down_bad_events(bad_event_Ax_peak, properties_bad_event_Ax_peak, Ax)
    return  bad_event_Ax_peak, properties_bad_event_Ax_peak, num_of_bad_event_peaks


def find_rain_over_wheels(Ax: np.ndarray) -> np.ndarray|dict|int:
    # bad peaks above wheel
    bad_event_above_wheel_Ax_peak, properties_bad_event_above_wheel_Ax_peak = find_peaks(
        Ax,
        prominence=(MIN_RAIN_ABOVE_WHEEL_PROMINENCE, None),
        width=(None, MAX_RAIN_WIDTH),
        rel_height=TOP_RAIN_PEAK,
    )
    num_of_bad_event_above_wheel_peaks = shift_down_bad_events(bad_event_above_wheel_Ax_peak, properties_bad_event_above_wheel_Ax_peak, Ax)
    return  bad_event_above_wheel_Ax_peak, properties_bad_event_above_wheel_Ax_peak, num_of_bad_event_above_wheel_peaks


def find_wheel_base(Ax: np.ndarray, wheel_width_range: Optional[tuple[float]] ) -> np.ndarray|dict|Optional[float]|Optional[float]|Optional[List[float]]:
    # wheel flat peaks
    wheel_width_range = (MIN_WHEEL_WIDTH, MAX_WHEEL_WIDTH) if wheel_width_range is None else wheel_width_range
    wheel_Ax_peaks, properties_wheel_bad_event_Ax_peak = find_peaks(
        Ax,
        prominence=(MIN_WHEEL_PROMINENCE, MAX_WHEEL_PROMINENCE),
        width=wheel_width_range,
        distance=MIN_WHEEL_PEAK_DISTANCE,
    )
    min_widths_wheel, max_widths_wheel = None, None
    widths_wheel=None
    if wheel_Ax_peaks.size >0 :
        min_widths_wheel, max_widths_wheel = min(properties_wheel_bad_event_Ax_peak["widths"]) , max(properties_wheel_bad_event_Ax_peak["widths"])
        array = np.array(properties_wheel_bad_event_Ax_peak["widths"])
        array.astype(float).tolist()
        widths_wheel=array.astype(float).tolist()
    return wheel_Ax_peaks, properties_wheel_bad_event_Ax_peak ,min_widths_wheel, max_widths_wheel, widths_wheel




def shift_down_bad_events(bad_event_peak: dict, properties_bad_event_peak: dict, Ax: np.ndarray) -> int:
    num_of_bad_event_peaks=len(properties_bad_event_peak['width_heights'])
    for i in range(num_of_bad_event_peaks) :
            shift_down_range=Ax[floor(properties_bad_event_peak['left_ips'][i]):ceil(properties_bad_event_peak['right_ips'][i])]
            if abs(Ax[floor(properties_bad_event_peak['left_ips'][i])] -Ax[ceil(properties_bad_event_peak['right_ips'][i])]) < MIN_RAIN_PROMINENCE :
                if Ax[bad_event_peak][i]-min(shift_down_range) < properties_bad_event_peak['prominences'][i]:
                    shift_down_range[:]= min(shift_down_range)
                    # print('x')
                else:    
                    shift_down_range[:]= Ax[bad_event_peak][i]-properties_bad_event_peak['prominences'][i]
                    # print('y')
            else:
                 shift_down_range[:]= max(Ax[floor(properties_bad_event_peak['left_ips'][i])], Ax[ceil(properties_bad_event_peak['right_ips'][i])])
                #  print('z')
    return num_of_bad_event_peaks

def error_signal_check( Ax: np.ndarray) -> bool:
    return np.any(Ax[ Ax < -10000]) or np.any(Ax[ Ax > 10000])
