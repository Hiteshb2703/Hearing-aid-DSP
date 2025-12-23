import soundfile as sf
import numpy as np
from scipy.signal import lfilter
from filters import filter_low, filter_band


fs = 16000  # Sampling frequency

def read_audio(file_path, target_sr=16000):
    """Read an audio file and resample to target sampling rate if necessary."""
    audio, sr = sf.read(file_path)

    if audio.ndim == 2:
        audio = np.mean(audio, axis=1)

    if sr != target_sr:
        raise ValueError(f"Sampling rate {sr} does not match target {target_sr}. Resampling not implemented.")
    return audio, sr

def apply_filterbank(audio, sr, order=5):
    b = [None] * 6
    a = [None] * 6
    filtered_audio = [None] * 6
    b[0] , a[0] = filter_low(250, sr, order)
    b[1] , a[1] = filter_band(sr, 250, 500, order)
    b[2] , a[2] = filter_band(sr, 500, 1000, order)
    b[3] , a[3] = filter_band(sr, 1000, 2000, order)
    b[4] , a[4] = filter_band(sr, 2000, 4000, order)    
    b[5] , a[5] = filter_band(sr, 4000, 7900, order)
    for i in range(6):
        filtered_audio[i] = lfilter(b[i], a[i], audio)
    return filtered_audio