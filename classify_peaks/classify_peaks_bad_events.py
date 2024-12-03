import numpy as np
from classify_peaks.find_abnormal_signal import error_signal_check # type: ignore
from classify_peaks.calculate_wheel import find_wheel_width_sample # type: ignore
from classify_peaks.classify_peaks_bad_events_ax import classify_peaks_bad_events_ax # type: ignore
from classify_peaks.Result_classify_peaks_bad_events_ax import Result_classify_peaks_bad_events_ax # type: ignore
from classify_peaks.Result_classify_peaks_bad_events import Result_classify_peaks_bad_events # type: ignore
from classify_peaks.fuzzy_inference_sys import fuzzy_inference_sys # type: ignore
from typing import (
    List,
    Dict,
    Tuple,
    Optional,
    Any,
)
from itertools import chain

def classify_peaks_bad_events(flip_axle_cm: np.ndarray, velocity: Optional[int], raw_time_sec: float) -> Result_classify_peaks_bad_events:

    all_sample = flip_axle_cm.shape[0]
    sensor_sampling_rate = all_sample / raw_time_sec
    wheel_width_sample_range = find_wheel_width_sample(velocity, sensor_sampling_rate)

    ax0=flip_axle_cm[:,0]
    if  error_signal_check(ax0) :
        result_classify_peaks_bad_events_ax0 = Result_classify_peaks_bad_events_ax()
        bad_event_peaks_density_ax0 = result_classify_peaks_bad_events_ax0.bad_event_peaks_density # = -10
    else :
        # plot peak ax0
        result_classify_peaks_bad_events_ax0 = classify_peaks_bad_events_ax(ax0, wheel_width_sample_range, all_sample)
        bad_event_peaks_density_ax0 = result_classify_peaks_bad_events_ax0.bad_event_peaks_density
    ax1=flip_axle_cm[:,1]
    if  error_signal_check(ax1) :
        result_classify_peaks_bad_events_ax1 = Result_classify_peaks_bad_events_ax()
        bad_event_peaks_density_ax1 = result_classify_peaks_bad_events_ax1.bad_event_peaks_density
    else :
        # plot peak ax1
        result_classify_peaks_bad_events_ax1 = classify_peaks_bad_events_ax(ax1, wheel_width_sample_range, all_sample)
        bad_event_peaks_density_ax1 = result_classify_peaks_bad_events_ax1.bad_event_peaks_density


    # fuzzy inference sys
    defuzzified, ax0_situation_dict, ax1_situation_dict, output_layer_situation_dict = fuzzy_inference_sys(bad_event_peaks_density_ax0, bad_event_peaks_density_ax1)

    result_classify_peaks_bad_events = Result_classify_peaks_bad_events(
        result_classify_peaks_bad_events_ax0= result_classify_peaks_bad_events_ax0,
        result_classify_peaks_bad_events_ax1= result_classify_peaks_bad_events_ax1,
        sensor_sampling_rate= sensor_sampling_rate,
        velocity= velocity,
        wheel_width_sample_range = wheel_width_sample_range,
        defuzzified = defuzzified,
        ax0_situation_dict =ax0_situation_dict,
        ax1_situation_dict =ax1_situation_dict,
        output_layer_situation_dict = output_layer_situation_dict,
    )

    return result_classify_peaks_bad_events
    