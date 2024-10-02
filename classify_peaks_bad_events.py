import numpy as np
import matplotlib.pyplot as plt
from shift_down_bad_events import *
from classify_peaks_bad_events_Ax import *
from typing import List

def classify_peaks_bad_events(flip_axle_cm: np.ndarray, file_path: str, path_component_list: List[str]):
    event_type = path_component_list[0]
    event_number =path_component_list[1]
    data_tag = path_component_list[0]+" | "+path_component_list[1]
    axle_cm_lane_key=path_component_list[-1]
    axle_cm_name_channel_list = {'1':'12','2':'12','3':'34','4':'34'}

    # plot peak
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [1, 1]})
    fig.canvas.manager.set_window_title(data_tag)
    fig.tight_layout(pad=3)

    # plot peak Ax0
    Ax0=flip_axle_cm[:,0]
    axs[0].set_title("Ax"+axle_cm_name_channel_list[axle_cm_lane_key][0])
    num_of_all_bad_event_peaks_Ax0 = classify_peaks_bad_events_Ax(Ax0, axs, 0)
    # plot peak Ax1
    Ax1=flip_axle_cm[:,1]
    axs[1].set_title("Ax"+axle_cm_name_channel_list[axle_cm_lane_key][1])
    num_of_all_bad_event_peaks_Ax1 = classify_peaks_bad_events_Ax(Ax1, axs, 1)

    # plt.show()
    new_fig_name = f'ploteventclassify_{event_number}.png'
    fig.savefig(file_path.replace("event.txt",new_fig_name))
    print(file_path.replace("event.txt",new_fig_name))
    fig.savefig(f'classify_peaks_bad_events_Ax_results/{event_type}/{new_fig_name}')
    plt.close(fig) 
    return


    