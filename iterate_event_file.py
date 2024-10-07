import os
import numpy as np
from typing import List
from read_event_data import *
from classify_peaks_bad_events import *
from animation import *

initial_collect_peaks_results_dict ={"bad_events":[],"bad_events_dirtyAX":[],"bad_events_raining":[],"good_events":[]}

# use recursive function.
def iterate_event_file(superfolder_path: str, collect_peaks_results_dict: dict[str, List[int]] =initial_collect_peaks_results_dict) -> dict[str, List[int]]:
    # serching event.text directory
    animate()
    for folder in os.listdir(superfolder_path):
        current_sub_event_location = os.path.join(superfolder_path, folder)
        if "event.txt" in os.listdir(current_sub_event_location):
            # print(current_sub_event_location)
            current_sub_event_location=os.path.join(current_sub_event_location, "event.txt")
            flip_axle_cm, path_component_list= read_event_data(current_sub_event_location)
            collect_peaks_results_dict = classify_peaks_bad_events(flip_axle_cm, current_sub_event_location, path_component_list ,collect_peaks_results_dict)
        else:
            iterate_event_file(current_sub_event_location, collect_peaks_results_dict)
    
    # no use return event_address, event_nd_data
    return collect_peaks_results_dict








# use loop down structure.
# def iterate_event_file(superfolder_path: str) -> List[str] | List[np.ndarray]:
#     event_address:List[str] =[]
#     event_nd_data:List[np.ndarray] =[]
#     # loop event.text directory
#     for main_event in os.listdir(superfolder_path):
#         current_main_event_location = os.path.join(superfolder_path, main_event)
#         for sub_event in os.listdir(current_main_event_location):
#             current_sub_event_location = os.path.join(current_main_event_location, sub_event)
     
#             if main_event=="good_events":
#                 for sub_sub_event in os.listdir(current_sub_event_location):
#                     current_sub_sub_event_location = os.path.join(current_sub_event_location, sub_sub_event)
#                     current_sub_sub_event_location = os.path.join(current_sub_sub_event_location, "event.txt")

#                     event_address, event_nd_data=read_event_data(event_address, event_nd_data, current_sub_sub_event_location)
#                 continue  # avoid repeat opendata    
#             current_sub_event_location=os.path.join(current_sub_event_location, "event.txt")
#             event_address, event_nd_data=read_event_data(event_address, event_nd_data, current_sub_event_location)
#     return event_address, event_nd_data


