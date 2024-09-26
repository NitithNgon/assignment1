import os
import numpy as np
import matplotlib.pyplot as plt
from typing import List

def read_event_data(event_address:List[str] =[], event_nd_data:List[str] =[], file_path:str ="" ) -> List[str] | List[np.ndarray]:
    event_address.append(file_path)
    file = open(file_path, 'r')
    # cut lines
    lines = file.readlines()
    usedline = lines[2:-1]
    used_data = []
    for i in usedline: used_data.append((i.strip()).split("\t"))
    # print(file_path)
    signal_array = np.array(used_data,dtype=float)
    axle_cm_lane_key = ((file_path.split("\\"))[-2])[-1]
    # print(axle_cm_lane_key)
    axle_cm_exact_channel_list = {'1':[-4,-3],'2':[-4,-3],'3':[-2,-1],'4':[-2,-1]}    # last 4 channels are ax
    axle_cm = signal_array[:, axle_cm_exact_channel_list[axle_cm_lane_key]]
    min_top_flatline_ax = min(axle_cm.max(axis=0))      # minimum top flat line of all ax
    # print(axle_cm.shape, axle_cm)
    flip_axle_cm = min_top_flatline_ax - axle_cm
    event_nd_data.append(flip_axle_cm)
    return event_address, event_nd_data



# use recursive function.
def iterate_event_file(superfolder_path: str, event_address:List[str] =[], event_nd_data:List[np.ndarray] =[]) -> List[str] | List[np.ndarray]:
    # serching event.text directory

    for folder in os.listdir(superfolder_path):
        current_sub_event_location = os.path.join(superfolder_path, folder)
        if "event.txt" in os.listdir(current_sub_event_location):
            print(current_sub_event_location)
            current_sub_event_location=os.path.join(current_sub_event_location, "event.txt")
            event_address, event_nd_data=read_event_data(event_address, event_nd_data, current_sub_event_location)
        else:
            iterate_event_file(current_sub_event_location, event_address, event_nd_data)

    return event_address, event_nd_data
# event_address, event_nd_data = iterate_event_file("to_Peiam")
# print(event_nd_data)

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


