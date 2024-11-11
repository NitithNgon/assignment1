from typing import Optional
from typing import Dict,Optional
from classify_peaks.Result_classify_peaks_bad_events_ax import Result_classify_peaks_bad_events_ax

class Result_classify_peaks_bad_events:
    def __init__(
        self,
        result_classify_peaks_bad_events_ax0 :Result_classify_peaks_bad_events_ax,
        result_classify_peaks_bad_events_ax1 :Result_classify_peaks_bad_events_ax,
        velocity :Optional[int],
        sensor_sampling_rate :float,
        wheel_width_sample_range :Optional[tuple[float]],
        defuzzified :float,
        ax0_situation_dict :Dict,
        ax1_situation_dict :Dict,
        output_layer_situation_dict :Dict,
    ):
        self.result_classify_peaks_bad_events_ax0 =result_classify_peaks_bad_events_ax0
        self.result_classify_peaks_bad_events_ax1 =result_classify_peaks_bad_events_ax1
        self.velocity =velocity
        self.sensor_sampling_rate =sensor_sampling_rate
        self.wheel_width_sample_range =wheel_width_sample_range
        self.defuzzified =defuzzified
        self.ax0_situation_dict =ax0_situation_dict
        self.ax1_situation_dict =ax1_situation_dict
        self.output_layer_situation_dict =output_layer_situation_dict

        