import numpy as np
import matplotlib.pyplot as plt
from typing import Optional
from typing import List

from classify_peaks.find_abnormal_signal import (
    find_rain_drop,
    find_rain_over_wheels,
    find_wheel_base,
)
from classify_peaks.Result_classify_peaks_bad_events_ax import Result_classify_peaks_bad_events_ax


def classify_peaks_bad_events_ax( ax: np.ndarray, wheel_width_range: Optional[tuple[float, float]], all_sample: int) -> Result_classify_peaks_bad_events_ax:

    ax_original = np.copy(ax)

    # bad peaks
    bad_event_peak, y_bad_event_peak, properties_bad_event_peak, num_of_bad_event_peaks =find_rain_drop(ax)
    
    # bad peaks above wheel
    bad_event_above_wheel_peak, y_bad_event_above_wheel_peak, properties_bad_event_above_wheel_peak, num_of_bad_event_above_wheel_peaks = find_rain_over_wheels(ax)

    # wheel flat peaks
    wheel_peaks, y_wheel_peaks, properties_wheel_bad_event_peak ,min_widths_wheel, max_widths_wheel, widths_wheel = find_wheel_base(ax, wheel_width_range= wheel_width_range)
    
    num_of_all_bad_event_peaks = num_of_bad_event_above_wheel_peaks + num_of_bad_event_peaks
    bad_event_peaks_density = num_of_all_bad_event_peaks*10000/all_sample

    result_classify_peaks_bad_events_ax = Result_classify_peaks_bad_events_ax(
        ax_original = ax_original,
        ax_final = ax,
        bad_event_peak = bad_event_peak,
        y_bad_event_peak = y_bad_event_peak,
        properties_bad_event_peak = properties_bad_event_peak,
        num_of_bad_event_peaks = num_of_bad_event_peaks,
        bad_event_above_wheel_peak = bad_event_above_wheel_peak,
        y_bad_event_above_wheel_peak = y_bad_event_above_wheel_peak,
        properties_bad_event_above_wheel_peak = properties_bad_event_above_wheel_peak,
        num_of_bad_event_above_wheel_peaks = num_of_bad_event_above_wheel_peaks,
        bad_event_peaks_density = bad_event_peaks_density,
        wheel_peaks = wheel_peaks,
        y_wheel_peaks = y_wheel_peaks,
        properties_wheel_bad_event_peak = properties_wheel_bad_event_peak,
        min_widths_wheel = min_widths_wheel, 
        max_widths_wheel = max_widths_wheel,
        widths_wheel = widths_wheel,
    )

    return result_classify_peaks_bad_events_ax


