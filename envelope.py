import numpy as np

def enve(signal,fs=16000,tau=0.05):
    alpha = np.exp(-1/(fs*tau))
    y = np.zeros_like(signal)
    y[0] = np.abs(signal[0])
    for i in range(1 , len(signal)):
        y[i] = (1-alpha)*np.abs(signal[i]) + alpha*y[i-1]
    return y