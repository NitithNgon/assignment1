import numpy as np
import matplotlib.pyplot as plt
from error_signal_check import error_signal_check
from classify_peaks_bad_events_Ax import classify_peaks_bad_events_Ax
from fuzzy_inference_sys import fuzzy_inference_sys
from find_wheel_width_sample import find_wheel_width_sample
from typing import List
from typing import Optional
from itertools import chain

def classify_peaks_bad_events(flip_axle_cm: np.ndarray, file_path: str, path_component_list: List[str] , collect_peaks_results_dict: dict[str, List[any]] , velocity: Optional[int], raw_time_sec: float) -> dict[str, List[any]]:
    min_widths_wheel_Ax0, max_widths_wheel_Ax0, min_widths_wheel_Ax1, max_widths_wheel_Ax1, widths_wheel_Ax0, widths_wheel_Ax1 = None, None, None, None, None, None
    
    event_type = path_component_list[0]
    event_number = path_component_list[1]
    data_tag = event_type+' | '+event_number
    axle_cm_lane_key = path_component_list[-1]
    axle_cm_name_channel_list = {
        '1':['1','2'],
        '2':['1','2'],
        '3':['3','4'],
        '4':['3','4'],
    }

    # plot peak
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [1, 1]})
    fig.canvas.manager.set_window_title(data_tag)
    fig.tight_layout(pad=3)

    all_sample = flip_axle_cm.shape[0]
    wheel_width_sample_range = find_wheel_width_sample(velocity, raw_time_sec, all_sample)
    set_dict_and_append(collect_peaks_results_dict,'sensor_sampling_rate',all_sample / raw_time_sec)
    if wheel_width_sample_range != None:
        set_dict_and_append(collect_peaks_results_dict,'wheel_width_sample',wheel_width_sample_range[0]/0.85)
    else : set_dict_and_append(collect_peaks_results_dict,'wheel_width_sample',wheel_width_sample_range)

    Ax0=flip_axle_cm[:,0]
    if  error_signal_check(Ax0) :
        bad_event_peaks_density_Ax0=-10
        axs[0].set_title(f"Ax{axle_cm_name_channel_list[axle_cm_lane_key][0]} density: {round(bad_event_peaks_density_Ax0, 2)} E-4")
    else :
        # plot peak Ax0
        num_of_all_bad_event_peaks_Ax0, min_widths_wheel_Ax0, max_widths_wheel_Ax0, widths_wheel_Ax0 = classify_peaks_bad_events_Ax(Ax0, axs, 0, wheel_width_sample_range)
        bad_event_peaks_density_Ax0 = num_of_all_bad_event_peaks_Ax0*10000/all_sample
        axs[0].set_title(f"Ax{axle_cm_name_channel_list[axle_cm_lane_key][0]} density: {round(bad_event_peaks_density_Ax0, 2)} E-4")
        set_dict_and_append(collect_peaks_results_dict,event_type,bad_event_peaks_density_Ax0)

    
    Ax1=flip_axle_cm[:,1]
    if  error_signal_check(Ax1) :
        bad_event_peaks_density_Ax1=-10
        axs[1].set_title(f"Ax{axle_cm_name_channel_list[axle_cm_lane_key][1]} density: {round(bad_event_peaks_density_Ax1, 2)} E-4")
    else :
        # plot peak Ax1
        num_of_all_bad_event_peaks_Ax1, min_widths_wheel_Ax1, max_widths_wheel_Ax1, widths_wheel_Ax1 = classify_peaks_bad_events_Ax(Ax1, axs, 1, wheel_width_sample_range)
        bad_event_peaks_density_Ax1 = num_of_all_bad_event_peaks_Ax1*10000/all_sample
        axs[1].set_title(f"Ax{axle_cm_name_channel_list[axle_cm_lane_key][1]} density: {round(bad_event_peaks_density_Ax1, 2)} E-4")
        set_dict_and_append(collect_peaks_results_dict,event_type,bad_event_peaks_density_Ax1)

    set_dict_and_append(collect_peaks_results_dict,'event_type',event_type)
    set_dict_and_append(collect_peaks_results_dict,'min_widths_wheel_Ax0',min_widths_wheel_Ax0)
    set_dict_and_append(collect_peaks_results_dict,'max_widths_wheel_Ax0',max_widths_wheel_Ax0)
    set_dict_and_append(collect_peaks_results_dict,'min_widths_wheel_Ax1',min_widths_wheel_Ax1)
    set_dict_and_append(collect_peaks_results_dict,'max_widths_wheel_Ax1',max_widths_wheel_Ax1)
    set_dict_and_append(collect_peaks_results_dict,'widths_wheel',list(chain.from_iterable(filter(None, [widths_wheel_Ax0, widths_wheel_Ax1]))))

    # fuzzy inference sys
    defuzzified, Ax0_situation_dict, Ax1_situation_dict, output_layer_situation_dict = fuzzy_inference_sys(bad_event_peaks_density_Ax0, bad_event_peaks_density_Ax1)
    set_dict_and_append(collect_peaks_results_dict,'sensors_durability',defuzzified)
    set_dict_and_append(collect_peaks_results_dict,'Ax0_situation_dict',Ax0_situation_dict)
    set_dict_and_append(collect_peaks_results_dict,'Ax1_situation_dict',Ax1_situation_dict)
    set_dict_and_append(collect_peaks_results_dict,'output_layer_situation_dict',output_layer_situation_dict)

    textstr = '\n'.join((
        f"Axle_sensors_durability={defuzzified:.2f}%",
        f"  Ax{axle_cm_name_channel_list[axle_cm_lane_key][0]} situation={Ax0_situation_dict}%",
        f"  Ax{axle_cm_name_channel_list[axle_cm_lane_key][1]} situation={Ax1_situation_dict}%",
        f"  output situation={output_layer_situation_dict}%"
    ))
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    axs[0].text(0.05 , 0.45, textstr, transform=axs[0].transAxes, bbox=props)
    # plt.show()
    new_fig_name = f'plotclassif_{event_number}.png'
    fig.savefig(file_path.replace('event.txt',new_fig_name))
    fig.savefig(f'classify_peaks_bad_events_Ax_results/{event_type}/{new_fig_name}')
    plt.close(fig) 
    return collect_peaks_results_dict


def set_dict_and_append(collect_peaks_results_dict: dict[str, List[any]], key: str, value: any):
    collect_peaks_results_dict.setdefault(key, []).append(value)

    