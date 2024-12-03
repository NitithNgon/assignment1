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
)

# use recursive function.
def iterate_event_file(superfolder_path: str):
    
    # serching event.text directory
    for folder in os.listdir(superfolder_path):
        current_sub_event_location = os.path.join(superfolder_path, folder)
        if 'event.txt' in os.listdir(current_sub_event_location):

            json_data=read_json(current_sub_event_location)
            current_sub_event_location=os.path.join(current_sub_event_location, 'event.txt')
            raw_time_sec = read_event_time(current_sub_event_location)
            flip_axle_cm, path_component_list= read_event_data(current_sub_event_location)
            velocity = json_data['velocity'] if json_data else None          
            result_classify_peaks_bad_events = classify_peaks_bad_events(flip_axle_cm , velocity, raw_time_sec)
            save_and_plot_shifted_bad_event_result(path_component_list, current_sub_event_location, result_classify_peaks_bad_events)
        else:
            iterate_event_file(current_sub_event_location,)