from typing import Optional,Tuple
WHEEL_WIDTH_CM =110

def find_wheel_width_sample(velocity: Optional[int], sensor_sampling_rate: float) -> Optional[Tuple[float, float]]:
    wheel_width_sample_range = None
    if velocity is not None:
        wheel_width_sample= WHEEL_WIDTH_CM/velocity*sensor_sampling_rate*3600/10**5 # km/hr to cm/s
        wheel_width_sample_range =(wheel_width_sample*0.85 , wheel_width_sample*1.15)
    return wheel_width_sample_range