from envelope import enve
from signals import read_audio, apply_filterbank 
from audio_gain import apply_gain
import numpy as np 

def compress(filtered_audio,fs=16000,threshold_dB = -30,attack_time=0.01,release_time=0.2,ratio=2):
	level_dB = [None] * 6
	smoothed_gain_dB = [None] * 6
	gain_linear = [None] * 6
	actual_gain_dB = [None] * 6
	processed_signal = [None] * 6
	eps = 1e-8
	alpha_a = np.exp(-1/(fs*attack_time))
	alpha_r = np.exp(-1/(fs*release_time))
	envelopes = [enve(filtered_audio[i], fs=16000, tau=0.02) for i in range(6)]

	for i in range(6):									#band-loop, looping over all 6 bands	
		envelope = envelopes[i]
		level_dB[i] = 20 * np.log10(envelope + eps)
		actual_gain_dB[i] = np.zeros_like(level_dB[i])
		for n in range(len(level_dB[i])):				#time-loop, looping over all samples of a chosen band
			if level_dB[i][n] <= threshold_dB:
				actual_gain_dB[i][n] = 0
			else:
				actual_gain_dB[i][n] = (threshold_dB - level_dB[i][n]) * (1 - 1/ratio)
		smoothed_gain_dB[i] = np.zeros_like(actual_gain_dB[i])
		smoothed_gain_dB[i][0] = actual_gain_dB[i][0]

		

		for n in range(1, len(actual_gain_dB[i])):
			if actual_gain_dB[i][n] < smoothed_gain_dB[i][n-1]:
				smoothed_gain_dB[i][n] = alpha_a * smoothed_gain_dB[i][n-1] + (1 - alpha_a) * actual_gain_dB[i][n]
			else:
				smoothed_gain_dB[i][n] = alpha_r * smoothed_gain_dB[i][n-1] + (1 - alpha_r) * actual_gain_dB[i][n]	
		gain_linear[i] = 10 ** (smoothed_gain_dB[i] / 20)
		processed_signal[i] = filtered_audio[i] * gain_linear[i]
	return processed_signal