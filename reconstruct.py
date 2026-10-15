from signals import read_audio, apply_filterbank
import numpy as np
import matplotlib.pyplot as plt
import sys

file_path = sys.argv[1] if len(sys.argv) > 1 else "84-121123-0002.flac"
audio, sr = read_audio(file_path)
filtered_audio = apply_filterbank(audio, sr)

def plot_waveforms(audio, filtered_audio, sr):
    time = np.arange(len(audio)) / sr
    plt.figure(figsize=(12, 10))

    plt.subplot(7, 1, 1)
    plt.plot(time, audio)
    plt.title('Original Audio Waveform')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')

    for i in range(6):
        plt.subplot(7, 1, i + 2)
        plt.plot(time, filtered_audio[i])
        plt.title(f'Filtered Audio Waveform - Band {i+1}')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')

    plt.tight_layout()
    plt.show()

plot_waveforms(audio, filtered_audio, sr)
reconstructed = np.sum (filtered_audio, axis=0)
error = audio - reconstructed
snr_db = 20*np.log10(np.sqrt(np.mean(audio**2)) / np.sqrt(np.mean(error**2)))
print(f"Reconstruction SNR: {snr_db:.1f} dB")
time = np.arange(len(audio)) / sr


plt.figure(figsize=(12, 6))
plt.plot(time, audio, label="Original", alpha=0.7)
plt.plot(time, reconstructed, label="Reconstructed", alpha=0.7)
plt.legend()
plt.title("Original vs Reconstructed Signal")
plt.show()

plt.figure(figsize=(12, 3))
plt.plot(time, error)
plt.title("Reconstruction Error")
plt.xlabel("Time [s]")
plt.ylabel("Error")
plt.show()
