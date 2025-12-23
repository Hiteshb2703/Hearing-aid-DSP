from profile import audiogram

def gain():
    gain_dB = {}       # gain for each band
    data_audiogram = audiogram()
    frequencies = [250, 500, 1000, 2000, 4000, 8000]
    for freq in frequencies:
        HL = data_audiogram[freq]
        gain_dB[freq] = 0.6 * HL 
    return gain_dB
