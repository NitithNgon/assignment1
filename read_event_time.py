import numpy as np
from typing import List
from datetime import (
    datetime,
    # timedelta,
)

def read_event_time( file_path:str ) -> float:
    with open(file_path, 'r') as f:

        lines = f.readlines()

        # first line = {event 1 : left lane outbound, event 2 : right lane outbound)
        event_number = int(lines[0].split('-')[-1])

        event_start_time = lines[1].split('=')[-1].strip()
        start = datetime.strptime(event_start_time, '%Y-%m-%d %H:%M:%S-%f')
  
        event_end_time = lines[-1].split('=')[-1].strip()
        stop = datetime.strptime(event_end_time, '%Y-%m-%d %H:%M:%S-%f')
        
   
    timedelta = stop - start
    raw_time = timedelta.seconds + timedelta.microseconds / 1000000
    return raw_time