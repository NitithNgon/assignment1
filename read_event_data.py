import numpy as np
from typing import List

def read_event_data(event_address:List[str] =[], event_nd_data:List[str] =[], file_path:str ="" ) -> np.ndarray | List[str] | List[np.ndarray]:
    file = open(file_path, 'r')
    # cut lines
    lines = file.readlines()
    usedline = lines[2:-1]
    used_data = []
    for i in usedline: used_data.append((i.strip()).split("\t"))
    print(file_path)
    signal_array = np.array(used_data,dtype=float)
    axle_cm_lane_key = ((file_path.split("\\"))[-2])[-1]
    # print(axle_cm_lane_key)
    axle_cm_exact_channel_list = {'1':[-4,-3],'2':[-4,-3],'3':[-2,-1],'4':[-2,-1]}    # last 4 channels are ax
    axle_cm = signal_array[:, axle_cm_exact_channel_list[axle_cm_lane_key]]
    min_top_flatline_ax = min(axle_cm.max(axis=0))                                      # minimum top flat line of all ax
    # print(axle_cm.shape, axle_cm)
    flip_axle_cm = min_top_flatline_ax - axle_cm

    # no use
    event_address.append(file_path)
    event_nd_data.append(flip_axle_cm)
    return flip_axle_cm, event_address, event_nd_data
