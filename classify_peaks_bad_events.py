import numpy as np
import matplotlib.pyplot as plt
from error_signal_check import error_signal_check
from classify_peaks_bad_events_Ax import classify_peaks_bad_events_Ax
from fuzzy_inference_sys import fuzzy_inference_sys
from typing import List
from typing import Optional

def classify_peaks_bad_events(flip_axle_cm: np.ndarray, file_path: str, path_component_list: List[str] , collect_peaks_results_dict: dict[str, List[float]] , velocity : Optional[int]) -> dict[str, List[float]]:
    min_widths_wheel_Ax0, max_widths_wheel_Ax0, min_widths_wheel_Ax1, max_widths_wheel_Ax1 = None, None, None, None
    
    event_type = path_component_list[0]
    event_number = path_component_list[1]
    data_tag = event_type+" | "+event_number
    axle_cm_lane_key=path_component_list[-1]
    axle_cm_name_channel_list = {'1':'12','2':'12','3':'34','4':'34'}

    # plot peak
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [1, 1]})
    fig.canvas.manager.set_window_title(data_tag)
    fig.tight_layout(pad=3)

    Ax0=flip_axle_cm[:,0]
    if  error_signal_check(Ax0) :
        bad_event_peaks_density_Ax0=-10
        axs[0].set_title("Ax"+axle_cm_name_channel_list[axle_cm_lane_key][0]+" density:"+str(round(bad_event_peaks_density_Ax0, 2))+" E-4")
    else :
        # plot peak Ax0
        num_of_all_bad_event_peaks_Ax0, min_widths_wheel_Ax0, max_widths_wheel_Ax0 = classify_peaks_bad_events_Ax(Ax0, axs, 0, velocity)
        bad_event_peaks_density_Ax0 = num_of_all_bad_event_peaks_Ax0*10000/len(Ax0)
        axs[0].set_title("Ax"+axle_cm_name_channel_list[axle_cm_lane_key][0]+" density:"+str(round(bad_event_peaks_density_Ax0, 2))+" E-4")
        collect_peaks_results_dict[event_type].append(bad_event_peaks_density_Ax0)

    
    Ax1=flip_axle_cm[:,1]
    if  error_signal_check(Ax1) :
        bad_event_peaks_density_Ax1=-10
        axs[1].set_title("Ax"+axle_cm_name_channel_list[axle_cm_lane_key][1]+" density:"+str(round(bad_event_peaks_density_Ax1, 2))+" E-4")
    else :
        # plot peak Ax1
        num_of_all_bad_event_peaks_Ax1, min_widths_wheel_Ax1, max_widths_wheel_Ax1 = classify_peaks_bad_events_Ax(Ax1, axs, 1, velocity)
        bad_event_peaks_density_Ax1 = num_of_all_bad_event_peaks_Ax1*10000/len(Ax1)
        axs[1].set_title("Ax"+axle_cm_name_channel_list[axle_cm_lane_key][1]+" density:"+str(round(bad_event_peaks_density_Ax1, 2))+" E-4")
        collect_peaks_results_dict[event_type].append(bad_event_peaks_density_Ax1)

    if event_type=="bad_events_dirtyAX":
        collect_peaks_results_dict["min_widths_wheel_Ax0"].append(min_widths_wheel_Ax0), collect_peaks_results_dict["max_widths_wheel_Ax0"].append(max_widths_wheel_Ax0), collect_peaks_results_dict["min_widths_wheel_Ax1"].append(min_widths_wheel_Ax1), collect_peaks_results_dict["max_widths_wheel_Ax1"].append(max_widths_wheel_Ax1)

    defuzzified, Ax0_situation_dict, Ax1_situation_dict, output_layer_situation_dict = fuzzy_inference_sys(bad_event_peaks_density_Ax0, bad_event_peaks_density_Ax1)
    textstr = '\n'.join((
        "Axle_sensors_durability=%.2f%%" % (defuzzified, ),
        "  Ax%s situation=%s%%" % (axle_cm_name_channel_list[axle_cm_lane_key][0], Ax0_situation_dict, ),
        "  Ax%s situation=%s%%" % (axle_cm_name_channel_list[axle_cm_lane_key][1], Ax1_situation_dict, ),
        "  output situation=%s%%" % (output_layer_situation_dict, )))
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    axs[0].text(0.05 , 0.45, textstr, transform=axs[0].transAxes, bbox=props)
    # plt.show()
    new_fig_name = f'plotclassif_{event_number}.png'
    fig.savefig(file_path.replace("event.txt",new_fig_name))
    fig.savefig(f'classify_peaks_bad_events_Ax_results/{event_type}/{new_fig_name}')
    plt.close(fig) 
    return collect_peaks_results_dict


    