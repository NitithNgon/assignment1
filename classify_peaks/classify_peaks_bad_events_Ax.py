import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from typing import Optional
from typing import List

from classify_peaks.find_abnormal_signal import (
    find_rain_drop,
    find_rain_over_wheels,
    find_wheel_base,
    shift_down_bad_events,
)
from classify_peaks.Result_classify_peaks_bad_events_Ax import Result_classify_peaks_bad_events_Ax


def classify_peaks_bad_events_Ax( Ax: np.ndarray, wheel_width_range: Optional[tuple[float]] ) -> Result_classify_peaks_bad_events_Ax:

    Ax_original = np.copy(Ax)

    # bad peaks
    bad_event_Ax_peak, properties_bad_event_Ax_peak, num_of_bad_event_peaks =find_rain_drop(Ax)
    
    # bad peaks above wheel
    bad_event_above_wheel_Ax_peak, properties_bad_event_above_wheel_Ax_peak, num_of_bad_event_above_wheel_peaks = find_rain_over_wheels(Ax)

    # wheel flat peaks
    wheel_Ax_peaks, properties_wheel_bad_event_Ax_peak ,min_widths_wheel, max_widths_wheel, widths_wheel = find_wheel_base(Ax, wheel_width_range= wheel_width_range)
    
    result_classify_peaks_bad_events_Ax = Result_classify_peaks_bad_events_Ax(
        Ax_original = Ax_original,
        Ax_final = Ax,
        bad_event_Ax_peak = bad_event_Ax_peak,
        properties_bad_event_Ax_peak = properties_bad_event_Ax_peak,
        num_of_bad_event_peaks = num_of_bad_event_peaks,
        bad_event_above_wheel_Ax_peak = bad_event_above_wheel_Ax_peak,
        properties_bad_event_above_wheel_Ax_peak = properties_bad_event_above_wheel_Ax_peak,
        num_of_bad_event_above_wheel_peaks = num_of_bad_event_above_wheel_peaks,
        wheel_Ax_peaks = wheel_Ax_peaks,
        properties_wheel_bad_event_Ax_peak = properties_wheel_bad_event_Ax_peak,
        min_widths_wheel = min_widths_wheel, 
        max_widths_wheel = max_widths_wheel,
        widths_wheel = widths_wheel,
    )

    return result_classify_peaks_bad_events_Ax


