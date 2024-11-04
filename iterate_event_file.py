import os
import numpy as np
from typing import List
from read_event_data import read_event_data
from classify_peaks_bad_events import classify_peaks_bad_events
from read_json import read_json

initial_collect_peaks_results_dict ={"event_number":[],"bad_events":[],"bad_events_dirtyAX":[],"bad_events_raining":[],"good_events":[],"min_widths_wheel_Ax0":[], "max_widths_wheel_Ax0":[], "min_widths_wheel_Ax1":[], "max_widths_wheel_Ax1":[], "widths_wheel":[], "event_type":[],"sensors_durability":[],"Ax0_situation_dict":[],"Ax1_situation_dict":[],"output_layer_situation_dict":[]}
initial_collect_json_keys=[
   "event_tag",
   "bridge_name",
   "date_time",
   "gross_vehicle_weight",
   "confident",
   "velocity",
   "lane",
   "vehicle_type",
   "axle_weight",
   "axle_spacing",
   "overweight",
   "overweight_amount",
   "esal",
   "lpr_number",
   "axle_count",
   "gvw_strain_are",
   "direction",
   "type_weight_limit",
]

# use recursive function.
def iterate_event_file(superfolder_path: str, collect_peaks_results_dict: dict[str, List[float]] =initial_collect_peaks_results_dict) -> dict[str, List[float]]:
    # serching event.text directory
    for folder in os.listdir(superfolder_path):
        current_sub_event_location = os.path.join(superfolder_path, folder)
        if "event.txt" in os.listdir(current_sub_event_location):
            # print(current_sub_event_location)
            json_data=read_json(current_sub_event_location)
            current_sub_event_location=os.path.join(current_sub_event_location, "event.txt")
            flip_axle_cm, path_component_list= read_event_data(current_sub_event_location)
            
            if json_data != None : velocity=json_data["velocity"]
            else: velocity=None
            collect_peaks_results_dict = classify_peaks_bad_events(flip_axle_cm, current_sub_event_location, path_component_list ,collect_peaks_results_dict, velocity)

            collect_peaks_results_dict["event_number"].append(path_component_list[0]+"|"+path_component_list[1])
            for k in initial_collect_json_keys:
                if k not in collect_peaks_results_dict:
                        collect_peaks_results_dict[k] = []  # Initialize an empty dict
                if json_data != None and k in json_data:
                    collect_peaks_results_dict[k].append(json_data[k])
                else:
                    collect_peaks_results_dict[k].append(None)
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


