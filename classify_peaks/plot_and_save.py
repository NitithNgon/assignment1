import numpy as np
import matplotlib.pyplot as plt
from typing import List,Dict
from classify_peaks.Result_classify_peaks_bad_events import Result_classify_peaks_bad_events

def save_and_plot_shifted_bad_event_result(path_component_list: List[str], file_path: str, result_classify_peaks_bad_events: Result_classify_peaks_bad_events):
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
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [1, 1]})
    fig.canvas.manager.set_window_title(data_tag)
    fig.tight_layout(pad=3)
    plot_shifted_bad_event_result(axes, 0, axle_cm_name_channel_list, axle_cm_lane_key, result_classify_peaks_bad_events)
    plot_shifted_bad_event_result(axes, 1, axle_cm_name_channel_list, axle_cm_lane_key, result_classify_peaks_bad_events)
    textstr = '\n'.join((
            f"axle_sensors_durability={result_classify_peaks_bad_events.defuzzified:.2f}%",
            f"  ax{axle_cm_name_channel_list[axle_cm_lane_key][0]} situation={result_classify_peaks_bad_events.ax0_situation_dict}%",
            f"  ax{axle_cm_name_channel_list[axle_cm_lane_key][1]} situation={result_classify_peaks_bad_events.ax1_situation_dict}%",
            f"  output situation={result_classify_peaks_bad_events.output_layer_situation_dict}%"
    ))
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    axes[0].text(0.05 , 0.45, textstr, transform=axes[0].transAxes, bbox=props)
    # plt.show()
    new_fig_name = f'plotclassif_{event_number}.png'
    fig.savefig(file_path.replace('event.txt',new_fig_name))
    fig.savefig(f'classify_peaks_bad_events_ax_results/{event_type}/{new_fig_name}')
    plt.close(fig) 


def plot_shifted_bad_event_result(axes: np.ndarray[plt.axes], axs_num: int, axle_cm_name_channel_list: Dict[str,List[str]], axle_cm_lane_key: str, result_classify_peaks_bad_events: Result_classify_peaks_bad_events):
    axs=axes[axs_num]
    result_classify_peaks_bad_events_ax = result_classify_peaks_bad_events.result_classify_peaks_bad_events_ax0 if axs_num==0 else result_classify_peaks_bad_events.result_classify_peaks_bad_events_ax1

    axs.set_title(f"ax{axle_cm_name_channel_list[axle_cm_lane_key][axs_num]} density: {round(result_classify_peaks_bad_events_ax.bad_event_peaks_density, 2)} E-4")
    axs.set_xlabel('time-ms.')
    axs.set_ylabel('axle-cm.')

    if result_classify_peaks_bad_events_ax.bad_event_peaks_density !=-10 :


        ax_original= result_classify_peaks_bad_events_ax.ax_original
        axs.plot(ax_original, "+", color = "C3")
        
        # bad peaks
        axs.plot(result_classify_peaks_bad_events_ax.bad_event_peak, result_classify_peaks_bad_events_ax.y_bad_event_peak, "x", color = "C2")

        # bad peaks above wheel
        axs.plot(result_classify_peaks_bad_events_ax.bad_event_above_wheel_peak, result_classify_peaks_bad_events_ax.y_bad_event_above_wheel_peak, "x", color = "C4")
        axs.vlines(    
            x=result_classify_peaks_bad_events_ax.bad_event_above_wheel_peak,
            ymin=result_classify_peaks_bad_events_ax.y_bad_event_above_wheel_peak - 1*result_classify_peaks_bad_events_ax.properties_bad_event_above_wheel_peak["prominences"],
            ymax=result_classify_peaks_bad_events_ax.y_bad_event_above_wheel_peak,
            color="C4",
        )
        # wheel flat peaks
        axs.plot(result_classify_peaks_bad_events_ax.wheel_peaks, result_classify_peaks_bad_events_ax.y_wheel_peaks, "x", color = "C1")
        axs.vlines(
            x=result_classify_peaks_bad_events_ax.wheel_peaks,
            ymin=result_classify_peaks_bad_events_ax.y_wheel_peaks - result_classify_peaks_bad_events_ax.properties_wheel_bad_event_peak["prominences"],
            ymax=result_classify_peaks_bad_events_ax.y_wheel_peaks,
            color="C1",
        )
        axs.hlines(
            y=result_classify_peaks_bad_events_ax.properties_wheel_bad_event_peak["width_heights"],
            xmin=result_classify_peaks_bad_events_ax.properties_wheel_bad_event_peak["left_ips"],
            xmax=result_classify_peaks_bad_events_ax.properties_wheel_bad_event_peak["right_ips"],
            color="C1",
        )
        if result_classify_peaks_bad_events_ax.wheel_peaks.size >0 :
            axs.hlines(
                y=result_classify_peaks_bad_events_ax.properties_wheel_bad_event_peak["width_heights"].mean() -15,
                xmin=(result_classify_peaks_bad_events_ax.properties_wheel_bad_event_peak["left_ips"])[0],
                xmax=(result_classify_peaks_bad_events_ax.properties_wheel_bad_event_peak["right_ips"])[-1],
                color = "C3",
            )

        # shifted down result
        ax_final= result_classify_peaks_bad_events_ax.ax_final
        axs.plot(ax_final, color = "C0")