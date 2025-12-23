from signals import read_audio, apply_filterbank
from gain import gain

def apply_gain(filtered_audio, gain_dB):
    gain_linear = {}
    audio_gain = {}
    frequencies = [250, 500, 1000, 2000, 4000, 8000]
    for freq in frequencies:
        gain_linear[freq] = 10 ** (gain_dB[freq] / 20)
        audio_gain[freq] = filtered_audio[frequencies.index(freq)] * gain_linear[freq]
    return audio_gain