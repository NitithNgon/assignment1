import os
import json
import numpy as np
from numpy.typing import NDArray
from typing import (
    List,
    Dict,
    Optional,
    Any,
    Tuple,
)
from datetime import (
    datetime,
    # timedelta,
)

def read_event_data( file_path:str) -> Tuple[ NDArray[np.float64], List[str]]:

    signal_array = np.genfromtxt(file_path, delimiter='\t', skip_header=2, skip_footer=1)

    path_component = (file_path.split('\\'))
    event_type = path_component[1]
    event_number = path_component[-2]
    axle_cm_lane_key = event_number[-1]

    # print(axle_cm_lane_key)
    axle_cm_exact_channel_list = {'1':[-4,-3],'2':[-4,-3],'3':[-2,-1],'4':[-2,-1]}    # last 4 channels are [.. ax1 ax2 ax3 ax4]
    axle_cm = signal_array[:, axle_cm_exact_channel_list[axle_cm_lane_key]]
    min_top_flatline_ax = min(axle_cm.max(axis=0))                                      # minimum top flat line of all ax
    # print(axle_cm.shape, axle_cm)
    flip_axle_cm = min_top_flatline_ax - axle_cm
    path_component_list=[event_type, event_number, axle_cm_lane_key]

    return flip_axle_cm, path_component_list

def read_event_time( file_path:str ) -> float:
    with open(file_path, 'r') as f:

        lines = f.readlines()

        # first line = {event 1 : left lane outbound, event 2 : right lane outbound)
        event_number = int(lines[0].split('-')[-1])

        event_start_time = lines[1].split('=')[-1].strip()
        start = datetime.strptime(event_start_time, '%Y-%m-%d %H:%M:%S-%f')
  
        event_end_time = lines[-1].split('=')[-1].strip()
        stop = datetime.strptime(event_end_time, '%Y-%m-%d %H:%M:%S-%f')
        
   
    timedelta = stop - start
    raw_time = timedelta.seconds + timedelta.microseconds / 1000000
    return raw_time

def read_json(current_sub_event_location: str | os.PathLike) -> Optional[Dict]:
    data=None
    for file in os.listdir(current_sub_event_location):
        if file[:4]=='json':
            current_sub_event_location=os.path.join(current_sub_event_location, file)
            f=open(current_sub_event_location)
            data=dict(json.load(f))
            break
    return data