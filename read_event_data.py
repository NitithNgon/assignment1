import numpy as np
from typing import List

def read_event_data( file_path:str ="" ) -> np.ndarray | List[str]:

    signal_array = np.genfromtxt(file_path, delimiter="\t", skip_header=2, skip_footer=1)

    path_component = (file_path.split("\\"))
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
