import numpy as np
import matplotlib.pyplot as plt
from classify_peaks.find_abnormal_signal import error_signal_check
from classify_peaks.calculate_wheel import find_wheel_width_sample
from classify_peaks.classify_peaks_bad_events_Ax import classify_peaks_bad_events_Ax
from classify_peaks.Result_classify_peaks_bad_events_Ax import Result_classify_peaks_bad_events_Ax
from fuzzy_inference_sys import fuzzy_inference_sys

from typing import List
from typing import Optional
from itertools import chain

def classify_peaks_bad_events(flip_axle_cm: np.ndarray, file_path: str, path_component_list: List[str] , collect_peaks_results_dict: dict[str, List[any]] , velocity: Optional[int], raw_time_sec: float) -> dict[str, any] | dict[str, List[any]]:
    min_widths_wheel_Ax0, max_widths_wheel_Ax0, min_widths_wheel_Ax1, max_widths_wheel_Ax1, widths_wheel_Ax0, widths_wheel_Ax1 = None, None, None, None, None, None
    result_classify_peaks_bad_events_Ax0 = Result_classify_peaks_bad_events_Ax()
    result_classify_peaks_bad_events_Ax1 = Result_classify_peaks_bad_events_Ax()
    
    event_type = path_component_list[0]

    all_sample = flip_axle_cm.shape[0]
    wheel_width_sample_range = find_wheel_width_sample(velocity, raw_time_sec, all_sample)
    set_dict_and_append(collect_peaks_results_dict,'sensor_sampling_rate',all_sample / raw_time_sec)
    if wheel_width_sample_range != None:
        set_dict_and_append(collect_peaks_results_dict,'wheel_width_sample',wheel_width_sample_range[0]/0.85)
    else : set_dict_and_append(collect_peaks_results_dict,'wheel_width_sample',wheel_width_sample_range)

    Ax0=flip_axle_cm[:,0]
    if  error_signal_check(Ax0) :
        bad_event_peaks_density_Ax0=-10
    else :
        # plot peak Ax0
        result_classify_peaks_bad_events_Ax0 = classify_peaks_bad_events_Ax(Ax0, wheel_width_sample_range)
        num_of_all_bad_event_peaks = result_classify_peaks_bad_events_Ax0.num_of_bad_event_above_wheel_peaks + result_classify_peaks_bad_events_Ax0.num_of_bad_event_peaks
        bad_event_peaks_density_Ax0 = num_of_all_bad_event_peaks*10000/all_sample
        set_dict_and_append(collect_peaks_results_dict,event_type,bad_event_peaks_density_Ax0)

    
    Ax1=flip_axle_cm[:,1]
    if  error_signal_check(Ax1) :
        bad_event_peaks_density_Ax1=-10
    else :
        # plot peak Ax1
        result_classify_peaks_bad_events_Ax1 = classify_peaks_bad_events_Ax(Ax1, wheel_width_sample_range)
        num_of_all_bad_event_peaks = result_classify_peaks_bad_events_Ax1.num_of_bad_event_above_wheel_peaks + result_classify_peaks_bad_events_Ax1.num_of_bad_event_peaks
        bad_event_peaks_density_Ax1 = num_of_all_bad_event_peaks*10000/all_sample
        set_dict_and_append(collect_peaks_results_dict,event_type,bad_event_peaks_density_Ax1)

    set_dict_and_append(collect_peaks_results_dict,'event_type',event_type)
    set_dict_and_append(collect_peaks_results_dict,'min_widths_wheel_Ax0',result_classify_peaks_bad_events_Ax0.min_widths_wheel)
    set_dict_and_append(collect_peaks_results_dict,'max_widths_wheel_Ax0',result_classify_peaks_bad_events_Ax0.max_widths_wheel)
    set_dict_and_append(collect_peaks_results_dict,'min_widths_wheel_Ax1',result_classify_peaks_bad_events_Ax1.min_widths_wheel)
    set_dict_and_append(collect_peaks_results_dict,'max_widths_wheel_Ax1',result_classify_peaks_bad_events_Ax1.max_widths_wheel)
    set_dict_and_append(collect_peaks_results_dict,'widths_wheel',list(chain.from_iterable(filter(None, [result_classify_peaks_bad_events_Ax0.widths_wheel, result_classify_peaks_bad_events_Ax1.widths_wheel]))))

    # fuzzy inference sys
    defuzzified, Ax0_situation_dict, Ax1_situation_dict, output_layer_situation_dict = fuzzy_inference_sys(bad_event_peaks_density_Ax0, bad_event_peaks_density_Ax1)
    set_dict_and_append(collect_peaks_results_dict,'sensors_durability',defuzzified)
    set_dict_and_append(collect_peaks_results_dict,'Ax0_situation_dict',Ax0_situation_dict)
    set_dict_and_append(collect_peaks_results_dict,'Ax1_situation_dict',Ax1_situation_dict)
    set_dict_and_append(collect_peaks_results_dict,'output_layer_situation_dict',output_layer_situation_dict)

    return result, collect_peaks_results_dict


def set_dict_and_append(collect_peaks_results_dict: dict[str, List[any]], key: str, value: any):
    collect_peaks_results_dict.setdefault(key, []).append(value)
    