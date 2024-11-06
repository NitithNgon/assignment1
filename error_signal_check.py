import numpy as np

def error_signal_check( Ax: np.ndarray) -> bool:
    return np.any(Ax[ Ax < -10000]) or np.any(Ax[ Ax > 10000])