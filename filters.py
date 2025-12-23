import numpy as np
from scipy.signal import butter

def filter_low(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low')
    return b, a

def filter_band(fs, f_low, f_high, order=5):
    nyq = 0.5 * fs
    low = min(f_low,f_high) / nyq
    high = max(f_low,f_high) / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

