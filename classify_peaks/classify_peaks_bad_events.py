import numpy as np
from classify_peaks.find_abnormal_signal import error_signal_check
from classify_peaks.calculate_wheel import find_wheel_width_sample
from classify_peaks.classify_peaks_bad_events_ax import classify_peaks_bad_events_ax
from classify_peaks.Result_classify_peaks_bad_events_ax import Result_classify_peaks_bad_events_ax
from classify_peaks.Result_classify_peaks_bad_events import Result_classify_peaks_bad_events
from fuzzy_inference_sys import fuzzy_inference_sys

from typing import List,Dict
from typing import Optional
from itertools import chain

def classify_peaks_bad_events(flip_axle_cm: np.ndarray, file_path: str, path_component_list: List[str] , collect_peaks_results_dict: Dict[str, List[any]] , velocity: Optional[int], raw_time_sec: float) -> Result_classify_peaks_bad_events | Dict[str, List[any]]:

    event_type = path_component_list[0]

    all_sample = flip_axle_cm.shape[0]
    sensor_sampling_rate = all_sample / raw_time_sec
    wheel_width_sample_range = find_wheel_width_sample(velocity, sensor_sampling_rate)
    set_dict_and_append(collect_peaks_results_dict,'sensor_sampling_rate',sensor_sampling_rate)
    if wheel_width_sample_range != None:
        set_dict_and_append(collect_peaks_results_dict,'wheel_width_sample',wheel_width_sample_range[0]/0.85)
    else : set_dict_and_append(collect_peaks_results_dict,'wheel_width_sample',wheel_width_sample_range)

    ax0=flip_axle_cm[:,0]
    if  error_signal_check(ax0) :
        result_classify_peaks_bad_events_ax0 = Result_classify_peaks_bad_events_ax()
        bad_event_peaks_density_ax0 = result_classify_peaks_bad_events_ax0.bad_event_peaks_density # = -10
    else :
        # plot peak ax0
        result_classify_peaks_bad_events_ax0 = classify_peaks_bad_events_ax(ax0, wheel_width_sample_range, all_sample)
        bad_event_peaks_density_ax0 = result_classify_peaks_bad_events_ax0.bad_event_peaks_density
        set_dict_and_append(collect_peaks_results_dict,event_type,bad_event_peaks_density_ax0)

    
    ax1=flip_axle_cm[:,1]
    if  error_signal_check(ax1) :
        result_classify_peaks_bad_events_ax1 = Result_classify_peaks_bad_events_ax()
        bad_event_peaks_density_ax1 = result_classify_peaks_bad_events_ax1.bad_event_peaks_density
    else :
        # plot peak ax1
        result_classify_peaks_bad_events_ax1 = classify_peaks_bad_events_ax(ax1, wheel_width_sample_range, all_sample)
        bad_event_peaks_density_ax1 = result_classify_peaks_bad_events_ax1.bad_event_peaks_density
        set_dict_and_append(collect_peaks_results_dict,event_type,bad_event_peaks_density_ax1)

    set_dict_and_append(collect_peaks_results_dict,'event_type',event_type)
    set_dict_and_append(collect_peaks_results_dict,'min_widths_wheel_ax0',result_classify_peaks_bad_events_ax0.min_widths_wheel)
    set_dict_and_append(collect_peaks_results_dict,'max_widths_wheel_ax0',result_classify_peaks_bad_events_ax0.max_widths_wheel)
    set_dict_and_append(collect_peaks_results_dict,'min_widths_wheel_ax1',result_classify_peaks_bad_events_ax1.min_widths_wheel)
    set_dict_and_append(collect_peaks_results_dict,'max_widths_wheel_ax1',result_classify_peaks_bad_events_ax1.max_widths_wheel)
    set_dict_and_append(collect_peaks_results_dict,'widths_wheel',list(chain.from_iterable(filter(None, [result_classify_peaks_bad_events_ax0.widths_wheel, result_classify_peaks_bad_events_ax1.widths_wheel]))))

    # fuzzy inference sys
    defuzzified, ax0_situation_dict, ax1_situation_dict, output_layer_situation_dict = fuzzy_inference_sys(bad_event_peaks_density_ax0, bad_event_peaks_density_ax1)
    set_dict_and_append(collect_peaks_results_dict,'sensors_durability',defuzzified)
    set_dict_and_append(collect_peaks_results_dict,'ax0_situation_dict',ax0_situation_dict)
    set_dict_and_append(collect_peaks_results_dict,'ax1_situation_dict',ax1_situation_dict)
    set_dict_and_append(collect_peaks_results_dict,'output_layer_situation_dict',output_layer_situation_dict)

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

    return result_classify_peaks_bad_events, collect_peaks_results_dict


def set_dict_and_append(collect_peaks_results_dict: dict[str, List[any]], key: str, value: any):
    collect_peaks_results_dict.setdefault(key, []).append(value)
    