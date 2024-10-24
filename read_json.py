import os
import numpy as np
from typing import Optional


def read_json(current_sub_event_location: str | os.PathLike) -> Optional[int]:
    for file in os.listdir(current_sub_event_location):
        if file[:4]=="json":
            current_sub_event_location=os.path.join(current_sub_event_location, file)
            read 
        print("")
    return 