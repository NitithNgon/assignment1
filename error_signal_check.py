import numpy as np

def error_signal_check( Ax: np.ndarray) -> bool:
    return any(Ax[ Ax < -10000])