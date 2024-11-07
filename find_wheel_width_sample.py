from typing import Optional
WHEEL_WIDTH_CM =110

def find_wheel_width_sample(velocity: Optional[int], raw_time_sec: float, all_sample: int) -> Optional[tuple[float]]:
    wheel_width_sample_range = None
    if velocity != None:
        sensor_sampling_rate = all_sample / raw_time_sec
        wheel_width_sample= WHEEL_WIDTH_CM/velocity*sensor_sampling_rate*3600/10**5 # km/hr to cm/s
        wheel_width_sample_range =(wheel_width_sample*0.85 , wheel_width_sample*1.15)
    return wheel_width_sample_range


    