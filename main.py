from compression import compress
from signals import read_audio, apply_filterbank
import numpy as np
import sys
import soundfile as sf

def reconstruct(processed_signal):
    """Sum all bands to reconstruct full-band signal"""
    out = np.zeros_like(processed_signal[0])
    for band in processed_signal:
        out += band
    return out

def rms_db(x):
    """Compute RMS level in dB"""
    return 20 * np.log10(np.sqrt(np.mean(x**2)) + 1e-8)


def process_pipeline(audio, sr):
    """Full hearing-aid DSP pipeline"""
    filtered = apply_filterbank(audio, sr)
    processed = compress(filtered, fs=sr)
    reconstructed = reconstruct(processed)
    return reconstructed


if __name__ == "__main__":

    path = sys.argv[1] if len(sys.argv) > 1 else "84-121123-0002.flac"

    audio, sr = read_audio(path, target_sr=16000)

    audio_normal = audio.copy()

    audio_soft = 0.05 * audio           # very soft
    audio_loud = 6.0 * audio            # very loud
    audio_loud = np.clip(audio_loud, -1.0, 1.0)

    out_normal = process_pipeline(audio_normal, sr)
    out_soft   = process_pipeline(audio_soft, sr)
    out_loud   = process_pipeline(audio_loud, sr)

    sf.write("reconstructed.flac", out_normal, sr)

    sf.write("soft_original.flac", audio_soft, sr)
    sf.write("soft_reconstructed.flac", out_soft, sr)

    sf.write("loud_original.flac", audio_loud, sr)
    sf.write("loud_reconstructed.flac", out_loud, sr)

    print("\n====== RMS LEVELS (dB) ======")
    print(f"Original NORMAL : {rms_db(audio_normal):.2f} dB")
    print(f"Processed NORMAL: {rms_db(out_normal):.2f} dB\n")

    print(f"Original SOFT   : {rms_db(audio_soft):.2f} dB")
    print(f"Processed SOFT  : {rms_db(out_soft):.2f} dB\n")

    print(f"Original LOUD   : {rms_db(audio_loud):.2f} dB")
    print(f"Processed LOUD  : {rms_db(out_loud):.2f} dB")

    print("\n Compression test complete.")