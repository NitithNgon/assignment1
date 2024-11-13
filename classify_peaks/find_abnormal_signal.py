import numpy as np
from math import floor
from math import ceil
import numpy as np
from scipy.signal import find_peaks # type: ignore
from numpy.typing import NDArray
from typing import (
    List,
    Dict,
    Tuple,
    Optional,
)

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


def find_rain_drop(ax: np.ndarray) -> Tuple[np.ndarray, np.ndarray, Dict, int]:
    # bad peaks
    bad_event_ax_peak, properties_bad_event_ax_peak = find_peaks(
        ax,
        prominence=(MIN_RAIN_PROMINENCE, None),
        width=(None, MAX_RAIN_WIDTH),
    )
    y_bad_event_ax_peak = ax[bad_event_ax_peak] # Fancy indexing creates a copy of np array (no data dependency)
    num_of_bad_event_peaks = shift_down_bad_events(bad_event_ax_peak, properties_bad_event_ax_peak, ax)

    return  bad_event_ax_peak, y_bad_event_ax_peak, properties_bad_event_ax_peak, num_of_bad_event_peaks


def find_rain_over_wheels(ax: np.ndarray) -> Tuple[np.ndarray, np.ndarray, Dict, int]:
    # bad peaks above wheel
    bad_event_above_wheel_ax_peak, properties_bad_event_above_wheel_ax_peak = find_peaks(
        ax,
        prominence=(MIN_RAIN_ABOVE_WHEEL_PROMINENCE, None),
        width=(None, MAX_RAIN_WIDTH),
        rel_height=TOP_RAIN_PEAK,
    )
    y_bad_event_above_wheel_ax_peak = ax[bad_event_above_wheel_ax_peak] # Fancy indexing creates a copy of np array (no data dependency)
    num_of_bad_event_above_wheel_peaks = shift_down_bad_events(bad_event_above_wheel_ax_peak, properties_bad_event_above_wheel_ax_peak, ax)

    return  bad_event_above_wheel_ax_peak, y_bad_event_above_wheel_ax_peak, properties_bad_event_above_wheel_ax_peak, num_of_bad_event_above_wheel_peaks


def find_wheel_base(ax: np.ndarray, wheel_width_range: Optional[tuple[float, float]] ) -> Tuple[ NDArray[np.float64], NDArray[np.float64], Dict, Optional[float], Optional[float], Optional[List[float]]]:
    # wheel flat peaks
    wheel_width_range = (MIN_WHEEL_WIDTH, MAX_WHEEL_WIDTH) if wheel_width_range is None else wheel_width_range
    wheel_ax_peaks, properties_wheel_bad_event_ax_peak = find_peaks(
        ax,
        prominence=(MIN_WHEEL_PROMINENCE, MAX_WHEEL_PROMINENCE),
        width=wheel_width_range,
        distance=MIN_WHEEL_PEAK_DISTANCE,
    )
    min_widths_wheel, max_widths_wheel = None, None
    widths_wheel=None
    y_wheel_ax_peaks = ax[wheel_ax_peaks]
    if wheel_ax_peaks.size >0 :
        min_widths_wheel, max_widths_wheel = min(properties_wheel_bad_event_ax_peak["widths"]) , max(properties_wheel_bad_event_ax_peak["widths"])
        array = np.array(properties_wheel_bad_event_ax_peak["widths"])
        array.astype(float).tolist()
        widths_wheel=array.astype(float).tolist()
    return wheel_ax_peaks, y_wheel_ax_peaks, properties_wheel_bad_event_ax_peak ,min_widths_wheel, max_widths_wheel, widths_wheel




def shift_down_bad_events(bad_event_peak: NDArray[np.float64], properties_bad_event_peak: Dict[str, NDArray[np.float64]], ax: NDArray[np.float64]) -> int:
    num_of_bad_event_peaks=len(properties_bad_event_peak['width_heights'])
    for i in range(num_of_bad_event_peaks) :
            shift_down_range=ax[floor(properties_bad_event_peak['left_ips'][i]):ceil(properties_bad_event_peak['right_ips'][i])]
            if abs(ax[floor(properties_bad_event_peak['left_ips'][i])] -ax[ceil(properties_bad_event_peak['right_ips'][i])]) < MIN_RAIN_PROMINENCE :
                if ax[bad_event_peak][i]-min(shift_down_range) < properties_bad_event_peak['prominences'][i]:
                    shift_down_range[:]= min(shift_down_range)
                    # print('x')
                else:    
                    shift_down_range[:]= ax[bad_event_peak][i]-properties_bad_event_peak['prominences'][i]
                    # print('y')
            else:
                 shift_down_range[:]= max(ax[floor(properties_bad_event_peak['left_ips'][i])], ax[ceil(properties_bad_event_peak['right_ips'][i])])
                #  print('z')
    return num_of_bad_event_peaks

def error_signal_check( ax: np.ndarray) -> np.bool:
    return np.any(ax[ ax < -10000]) or np.any(ax[ ax > 10000])
