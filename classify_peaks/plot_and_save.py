import numpy as np
import matplotlib.pyplot as plt
from typing import List,Dict

def save_and_plot_shifted_bad_event_result(path_component_list: List[str]):
    event_type = path_component_list[0]
    event_number = path_component_list[1]
    data_tag = event_type+' | '+event_number
    axle_cm_lane_key = path_component_list[-1]
    axle_cm_name_channel_list = {
        '1':['1','2'],
        '2':['1','2'],
        '3':['3','4'],
        '4':['3','4'],
    }
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [1, 1]})
    fig.canvas.manager.set_window_title(data_tag)
    fig.tight_layout(pad=3)
    plot_shifted_bad_event_result(axs[0],)
    plot_shifted_bad_event_result(axs[1],)
    textstr = '\n'.join((
            f"Axle_sensors_durability={defuzzified:.2f}%",
            f"  Ax{axle_cm_name_channel_list[axle_cm_lane_key][0]} situation={Ax0_situation_dict}%",
            f"  Ax{axle_cm_name_channel_list[axle_cm_lane_key][1]} situation={Ax1_situation_dict}%",
            f"  output situation={output_layer_situation_dict}%"
    ))
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    axs[0].text(0.05 , 0.45, textstr, transform=axs[0].transAxes, bbox=props)
    # plt.show()
    new_fig_name = f'plotclassif_{event_number}.png'
    fig.savefig(file_path.replace('event.txt',new_fig_name))
    fig.savefig(f'classify_peaks_bad_events_Ax_results/{event_type}/{new_fig_name}')
    plt.close(fig) 


def plot_shifted_bad_event_result(axs: np.ndarray[plt.Axes], Ax_original: np.ndarray, Ax_result: np.ndarray):
    axs.set_title(f"Ax{axle_cm_name_channel_list[axle_cm_lane_key][0]} density: {round(bad_event_peaks_density_Ax0, 2)} E-4")
    axs.set_xlabel('time-ms.')
    axs.set_ylabel('Axle-cm.')
    axs.plot(Ax_original, "+", color = "C3")
    # bad peaks
    axs[axs_num].plot(bad_event_Ax_peak, Ax[bad_event_Ax_peak], "x", color = "C2")
    # bad peaks above wheel
    axs[axs_num].plot(bad_event_above_wheel_Ax_peak, Ax[bad_event_above_wheel_Ax_peak], "x", color = "C4")
    axs[axs_num].vlines(    
        x=bad_event_above_wheel_Ax_peak,
        ymin=Ax[bad_event_above_wheel_Ax_peak] - 1*properties_bad_event_above_wheel_Ax_peak["prominences"],
        ymax=Ax[bad_event_above_wheel_Ax_peak],
        color="C4",
    )
    # wheel flat peaks
    axs[axs_num].plot(wheel_Ax_peaks, Ax[wheel_Ax_peaks], "x", color = "C1")
    axs[axs_num].vlines(
        x=wheel_Ax_peaks,
        ymin=Ax[wheel_Ax_peaks] - properties_wheel_bad_event_Ax_peak["prominences"],
        ymax=Ax[wheel_Ax_peaks],
        color="C1",
    )
    axs[axs_num].hlines(
        y=properties_wheel_bad_event_Ax_peak["width_heights"],
        xmin=properties_wheel_bad_event_Ax_peak["left_ips"],
        xmax=properties_wheel_bad_event_Ax_peak["right_ips"],
        color="C1",
    )
    if wheel_Ax_peaks.size >0 :
        axs[axs_num].hlines(
            y=properties_wheel_bad_event_Ax_peak["width_heights"].mean() -15,
            xmin=(properties_wheel_bad_event_Ax_peak["left_ips"])[0],
            xmax=(properties_wheel_bad_event_Ax_peak["right_ips"])[-1],
            color = "C3",
        )

    # shifted down result
    axs[axs_num].plot(Ax, color = "C0")