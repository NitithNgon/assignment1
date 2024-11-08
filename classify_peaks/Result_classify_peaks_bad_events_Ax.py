import numpy as np
from typing import Optional
from typing import List,Dict

class Result_classify_peaks_bad_events_Ax:
    def __init__(
        self,
        Ax_original :np.ndarray,
        Ax_final :np.ndarray,
        bad_event_Ax_peak :np.ndarray,
        properties_bad_event_Ax_peak :Dict,
        num_of_bad_event_peaks :int,
        bad_event_above_wheel_Ax_peak :np.ndarray,
        properties_bad_event_above_wheel_Ax_peak :Dict,
        num_of_bad_event_above_wheel_peaks :int,
        wheel_Ax_peaks :np.ndarray,
        properties_wheel_bad_event_Ax_peak :Dict,
        min_widths_wheel :Optional[float],
        max_widths_wheel :Optional[float],
        widths_wheel :Optional[List[float]],
    ):
        self.Ax_original =Ax_original
        self.Ax_final =Ax_final
        self.bad_event_Ax_peak =bad_event_Ax_peak
        self.properties_bad_event_Ax_peak =properties_bad_event_Ax_peak
        self.num_of_bad_event_peaks =num_of_bad_event_peaks
        self.bad_event_above_wheel_Ax_peak =bad_event_above_wheel_Ax_peak
        self.properties_bad_event_above_wheel_Ax_peak =properties_bad_event_above_wheel_Ax_peak
        self.num_of_bad_event_above_wheel_peaks =num_of_bad_event_above_wheel_peaks
        self.wheel_Ax_peaks =wheel_Ax_peaks
        self.properties_wheel_bad_event_Ax_peak =properties_wheel_bad_event_Ax_peak
        self.min_widths_wheel =min_widths_wheel
        self.max_widths_wheel =max_widths_wheel
        self.widths_wheel =widths_wheel


        