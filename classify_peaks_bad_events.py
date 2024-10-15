import numpy as np
import matplotlib.pyplot as plt
from error_signal_check import *
from classify_peaks_bad_events_Ax import *

from typing import List

def classify_peaks_bad_events(flip_axle_cm: np.ndarray, file_path: str, path_component_list: List[str] , collect_peaks_results_dict: dict[str, List[float]]) -> dict[str, List[float]]:
    event_type = path_component_list[0]
    event_number =path_component_list[1]
    data_tag = path_component_list[0]+" | "+path_component_list[1]
    axle_cm_lane_key=path_component_list[-1]
    axle_cm_name_channel_list = {'1':'12','2':'12','3':'34','4':'34'}

    # plot peak
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [1, 1]})
    fig.canvas.manager.set_window_title(data_tag)
    fig.tight_layout(pad=3)

    Ax0=flip_axle_cm[:,0]
    if  error_signal_check(Ax0) : Ax0_classified_type = "bad_events_signal_error"
    else :
        # plot peak Ax0
        num_of_all_bad_event_peaks_Ax0 = classify_peaks_bad_events_Ax(Ax0, axs, 0)
        bad_event_peaks_density_Ax0 = num_of_all_bad_event_peaks_Ax0/len(Ax0)
        axs[0].set_title("Ax"+axle_cm_name_channel_list[axle_cm_lane_key][0]+" density:"+str(round(bad_event_peaks_density_Ax0*10000, 2))+" E-4")
        collect_peaks_results_dict[event_type].append(bad_event_peaks_density_Ax0)

    
    Ax1=flip_axle_cm[:,1]
    if  error_signal_check(Ax1) : Ax1_classified_type = "bad_events_signal_error"
    else :
        # plot peak Ax1
        num_of_all_bad_event_peaks_Ax1 = classify_peaks_bad_events_Ax(Ax1, axs, 1)
        bad_event_peaks_density_Ax1 = num_of_all_bad_event_peaks_Ax1/len(Ax1)
        axs[1].set_title("Ax"+axle_cm_name_channel_list[axle_cm_lane_key][1]+" density:"+str(round(bad_event_peaks_density_Ax1*10000, 2))+" E-4")
        collect_peaks_results_dict[event_type].append(bad_event_peaks_density_Ax1)

    plt.show()
    # new_fig_name = f'plotclassif_{event_number}.png'
    # fig.savefig(file_path.replace("event.txt",new_fig_name))
    # fig.savefig(f'classify_peaks_bad_events_Ax_results/{event_type}/{new_fig_name}')
    # plt.close(fig) 
    return collect_peaks_results_dict


    