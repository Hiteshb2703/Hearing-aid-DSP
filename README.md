# Digital Hearing Aid (Wide Dynamic Range Compression)

A Python-based Digital Signal Processing (DSP) pipeline that simulates the core audio processing engine of a digital hearing aid. This project implements a 6-band Wide Dynamic Range Compression (WDRC) system to dynamically adjust audio levels based on a patient's simulated audiogram profile.

## Pipeline Architecture

The signal chain strictly follows standard hearing aid DSP architecture, processing audio through the following stages:

1. **Filterbank Splitting (`filters.py`, `signals.py`)**
   * The incoming audio signal is split into 6 distinct frequency bands (centered around 250Hz, 500Hz, 1kHz, 2kHz, 4kHz, and 8kHz).
   * Utilizes SciPy's Butterworth IIR filters (Lowpass and Bandpass) to isolate frequencies.

2. **Envelope Detection (`envelope.py`)**
   * A first-order recursive filter tracks the amplitude envelope of each frequency band in real-time.
   * Formula implemented: $y[n] = (1 - \alpha)|x[n]| + \alpha y[n-1]$.

3. **Wide Dynamic Range Compression (`compression.py`)**
   * Calculates the instantaneous dB level of the envelope.
   * Applies asymmetric smoothing using distinct **Attack** ($0.01s$) and **Release** ($0.2s$) time constants.
   * This ensures fast reaction to sudden loud noises (protecting the ear) while releasing slowly to prevent "pumping" artifacts in normal speech.

4. **Reconstruction (`reconstruct.py`)**
   * Converts the smoothed dB gain back to linear gain.
   * Multiplies the linear gain against the original bandpassed signals, then sums all 6 bands back into a single full-band output.

## File Structure & Modules

* `profile.py`: Mocks a patient's clinical audiogram, providing Hearing Level (HL) dB values across standard frequencies.
* `gain.py`: Calculates target static gain using standard prescriptive fitting rules.
* `compression.py`: The core WDRC logic handling thresholding, ratio application, and temporal smoothing.
* `reconstruct.py`: The main execution script. Runs test files (normal, soft, and loud) through the pipeline and calculates output RMS levels to prove compression efficacy.

## Known Issues / Future Optimizations

* **Filter Stability:** Currently, the filterbank uses `scipy.signal.butter`'s default polynomial (`b, a`) output. At the filter orders required for narrow bandpass bands, this becomes poorly conditioned and can introduce numerical instability.
* **Proposed Fix:** Transition the filterbank generation from `[b, a]` coefficients to Second-Order Sections (`sos`) using `scipy.signal.sosfilt` to guarantee stability at higher orders.

## Usage

Run the main reconstruction pipeline to process audio and output compressed FLAC files:

```bash
python reconstruct.py
