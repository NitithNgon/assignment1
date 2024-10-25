import os
import json
from typing import Optional


def read_json(current_sub_event_location: str | os.PathLike) -> Optional[int]:
    velocity=None
    for file in os.listdir(current_sub_event_location):
        if file[:4]=="json":
            current_sub_event_location=os.path.join(current_sub_event_location, file)
            f=open(current_sub_event_location)
            data=json.load(f)
            velocity=data["velocity"]
            break
    return velocity