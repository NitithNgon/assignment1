import numpy as np
from typing import Optional
from typing import List,Dict

class Result_classify_peaks_bad_events_ax:
    def __init__(
        self,
        ax_original :np.ndarray = np.array([]),
        ax_final :np.ndarray = np.array([]),
        bad_event_peak :np.ndarray = np.array([]),
        y_bad_event_peak :np.ndarray = np.array([]),
        properties_bad_event_peak :Dict ={},
        num_of_bad_event_peaks :int = 0,
        bad_event_above_wheel_peak :np.ndarray = np.array([]),
        y_bad_event_above_wheel_peak :np.ndarray = np.array([]),
        properties_bad_event_above_wheel_peak :Dict ={},
        num_of_bad_event_above_wheel_peaks :int =0,
        bad_event_peaks_density :float = -10,
        wheel_peaks :np.ndarray =np.array([]),
        y_wheel_peaks :np.ndarray =np.array([]),
        properties_wheel_bad_event_peak :Dict ={},
        min_widths_wheel :Optional[float] =None,
        max_widths_wheel :Optional[float] =None,
        widths_wheel :Optional[List[float]] =None,
    ):
        self.ax_original =ax_original
        self.ax_final =ax_final
        self.bad_event_peak =bad_event_peak
        self.y_bad_event_peak =y_bad_event_peak
        self.properties_bad_event_peak =properties_bad_event_peak
        self.num_of_bad_event_peaks =num_of_bad_event_peaks
        self.bad_event_above_wheel_peak =bad_event_above_wheel_peak
        self.y_bad_event_above_wheel_peak =y_bad_event_above_wheel_peak
        self.properties_bad_event_above_wheel_peak =properties_bad_event_above_wheel_peak
        self.num_of_bad_event_above_wheel_peaks =num_of_bad_event_above_wheel_peaks
        self.bad_event_peaks_density = bad_event_peaks_density
        self.wheel_peaks =wheel_peaks
        self.y_wheel_peaks =y_wheel_peaks
        self.properties_wheel_bad_event_peak =properties_wheel_bad_event_peak
        self.min_widths_wheel =min_widths_wheel
        self.max_widths_wheel =max_widths_wheel
        self.widths_wheel =widths_wheel


        