from typing import Optional
from typing import List

def find_wheel_width_sample(velocity: Optional[int], raw_time_sec: float, all_sample: int) -> Optional[List[float]]:
    wheel_width_sample_range = None
    if velocity != None:
        wheel_width_cm = 80
        sensor_sampling_rate = all_sample / raw_time_sec
        wheel_width_sample= wheel_width_cm/velocity*sensor_sampling_rate*3600/10**5 # km/hr to cm/s
        wheel_width_sample_range =[wheel_width_sample*0.9 , wheel_width_sample*1.1]
    return wheel_width_sample_range


    