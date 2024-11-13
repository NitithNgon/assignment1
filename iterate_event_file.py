import os
from typing import (
    List, 
    Dict,
    Any,
)
from classify_peaks.plot_and_save import save_and_plot_shifted_bad_event_result
from read_data.read_event import (
    read_event_data,
    read_event_time,
    read_json,
)
from classify_peaks.classify_peaks_bad_events import (
    classify_peaks_bad_events,
    set_dict_and_append,
)

# use recursive function.
def iterate_event_file(superfolder_path: str, collect_peaks_results_dict: Dict[str, List[Any]] ={}) -> Dict[str, List[Any]]:
    
    # serching event.text directory
    for folder in os.listdir(superfolder_path):
        current_sub_event_location = os.path.join(superfolder_path, folder)
        if 'event.txt' in os.listdir(current_sub_event_location):

            json_data=read_json(current_sub_event_location)
            current_sub_event_location=os.path.join(current_sub_event_location, 'event.txt')
            raw_time_sec = read_event_time(current_sub_event_location)
            flip_axle_cm, path_component_list= read_event_data(current_sub_event_location)
            velocity = json_data['velocity'] if json_data else None          
            result_classify_peaks_bad_events, collect_peaks_results_dict = classify_peaks_bad_events(flip_axle_cm, current_sub_event_location, path_component_list ,collect_peaks_results_dict, velocity, raw_time_sec)
            save_and_plot_shifted_bad_event_result(path_component_list, current_sub_event_location, result_classify_peaks_bad_events)
            set_dict_and_append(collect_peaks_results_dict,'event_number',path_component_list[0]+'|'+path_component_list[1])
            
            if json_data is not None:
                for k in json_data.keys():
                    if k not in collect_peaks_results_dict:
                        collect_peaks_results_dict[k] = []  # Initialize an empty dict
                    else:
                        collect_peaks_results_dict[k].extend([None]*(len(collect_peaks_results_dict['event_number'])-len(collect_peaks_results_dict[k])-1))
                        collect_peaks_results_dict[k].append(json_data[k])
        else:
            iterate_event_file(current_sub_event_location, collect_peaks_results_dict)
    return collect_peaks_results_dict