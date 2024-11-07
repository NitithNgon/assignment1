import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from typing import Optional
from typing import List

from shift_down_bad_events import (
    shift_down_bad_events,
    MIN_RAIN_PROMINENCE
)
# depend on distance 
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

def classify_peaks_bad_events_Ax( Ax: np.ndarray,
                                 axs: np.ndarray[plt.Axes],
                                 axs_num: int,
                                 wheel_width_range: tuple[float],
    ) -> tuple[int, Optional[float], Optional[float], Optional[List[float]]]:

    wheel_width_range = (MIN_WHEEL_WIDTH, MAX_WHEEL_WIDTH) if wheel_width_range is None else wheel_width_range

    # plot peak Ax
    axs[axs_num].set_xlabel('time-ms.')
    axs[axs_num].set_ylabel('Axle-cm.')
    axs[axs_num].plot(Ax, "+", color = "C3")


    # bad peaks
    bad_event_Ax_peak, properties_bad_event_Ax_peak = find_peaks(
        Ax,
        prominence=(MIN_RAIN_PROMINENCE, None),
        width=(None, MAX_RAIN_WIDTH),
    )
    axs[axs_num].plot(bad_event_Ax_peak, Ax[bad_event_Ax_peak], "x", color = "C2")
    num_of_bad_event_peaks = shift_down_bad_events(bad_event_Ax_peak, properties_bad_event_Ax_peak, Ax)


    # bad peaks above wheel
    bad_event_above_wheel_Ax_peak, properties_bad_event_above_wheel_Ax_peak = find_peaks(
        Ax,
        prominence=(MIN_RAIN_ABOVE_WHEEL_PROMINENCE, None),
        width=(None, MAX_RAIN_WIDTH),
        rel_height=TOP_RAIN_PEAK,
    )
    axs[axs_num].plot(bad_event_above_wheel_Ax_peak, Ax[bad_event_above_wheel_Ax_peak], "x", color = "C4")
    axs[axs_num].vlines(    
        x=bad_event_above_wheel_Ax_peak,
        ymin=Ax[bad_event_above_wheel_Ax_peak] - 1*properties_bad_event_above_wheel_Ax_peak["prominences"],
        ymax=Ax[bad_event_above_wheel_Ax_peak],
        color="C4",
    )
    num_of_bad_event_above_wheel_peaks = shift_down_bad_events(bad_event_above_wheel_Ax_peak, properties_bad_event_above_wheel_Ax_peak, Ax)


    # wheel flat peaks
    wheel_Ax_peaks, properties_wheel_bad_event_Ax_peak = find_peaks(
        Ax,
        prominence=(MIN_WHEEL_PROMINENCE, MAX_WHEEL_PROMINENCE),
        width=wheel_width_range,
        distance=MIN_WHEEL_PEAK_DISTANCE,
    )
    axs[axs_num].plot(wheel_Ax_peaks, Ax[wheel_Ax_peaks], "x", color = "C1")
    axs[axs_num].vlines(
        x=wheel_Ax_peaks,
        ymin=Ax[wheel_Ax_peaks] - properties_wheel_bad_event_Ax_peak["prominences"],
        ymax=Ax[wheel_Ax_peaks],
        color="C1",
    )
    axs[axs_num].hlines(
        y=properties_wheel_bad_event_Ax_peak["width_heights"],
        xmin=properties_wheel_bad_event_Ax_peak["left_ips"],
        xmax=properties_wheel_bad_event_Ax_peak["right_ips"],
        color="C1",
    )
    min_widths_wheel, max_widths_wheel = None, None
    widths_wheel=None
    if wheel_Ax_peaks.size >0 :
        axs[axs_num].hlines(
            y=properties_wheel_bad_event_Ax_peak["width_heights"].mean() -15,
            xmin=(properties_wheel_bad_event_Ax_peak["left_ips"])[0],
            xmax=(properties_wheel_bad_event_Ax_peak["right_ips"])[-1],
            color = "C3",
        )
        min_widths_wheel, max_widths_wheel = min(properties_wheel_bad_event_Ax_peak["widths"]) , max(properties_wheel_bad_event_Ax_peak["widths"])
        array = np.array(properties_wheel_bad_event_Ax_peak["widths"])
        array.astype(float).tolist()
        widths_wheel=array.astype(float).tolist()

    # shifted down result
    axs[axs_num].plot(Ax, color = "C0")
    return num_of_bad_event_peaks + num_of_bad_event_above_wheel_peaks ,min_widths_wheel, max_widths_wheel,widths_wheel


