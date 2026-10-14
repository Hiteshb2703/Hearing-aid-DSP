# Digital Hearing Aid (Multiband Compression Pipeline)

A Python-based Digital Signal Processing (DSP) simulation of a digital hearing aid's audio processing chain. It splits audio into 6 frequency bands, tracks each band's envelope, applies per-band dynamic range compression, and recombines the bands into a full-band output.

A prescriptive-gain module based on a mock audiogram (`profile.py`, `gain.py`, `audio_gain.py`) is included but is **not yet integrated** into the main pipeline. The current output is therefore compression only: loud sounds are attenuated, soft sounds are not amplified.

## Pipeline Architecture

The signal chain processes audio offline (batch, not real-time) through the following stages:

1. **Filterbank Splitting (`filters.py`, `signals.py`)**
   * The input is split into 6 bands: 0–250 Hz (lowpass), then bandpass 250–500 Hz, 500 Hz–1 kHz, 1–2 kHz, 2–4 kHz, and 4–7.9 kHz.
   * Uses SciPy Butterworth IIR filters (5th-order prototypes, so 10th-order for the bandpass bands), applied causally with `lfilter`.

2. **Envelope Detection (`envelope.py`)**
   * A first-order recursive filter tracks the amplitude envelope of each band.
   * Formula implemented: $y[n] = (1 - \alpha)|x[n]| + \alpha y[n-1]$, with $\alpha = e^{-1/(f_s \tau)}$ and $\tau = 20$ ms (as called from `compression.py`).

3. **Dynamic Range Compression (`compression.py`)**
   * Converts each band's envelope to dBFS.
   * Static curve: threshold −30 dBFS, 2:1 ratio, hard knee. Below the threshold the gain is 0 dB; above it the gain is $(\text{threshold} - \text{level}) \times (1 - 1/\text{ratio})$ dB.
   * The gain (in dB) is then smoothed with asymmetric time constants: **Attack** ($0.01s$) when the gain is falling and **Release** ($0.2s$) when it is rising. Fast attack reacts quickly to sudden loud sounds, and slow release helps avoid audible "pumping".
   * The smoothed gain is converted to linear and multiplied into the band signal. This gain smoothing is a separate stage from the envelope smoothing in step 2.

4. **Recombination (`main.py`)**
   * The six compressed bands are summed into a single full-band output.
   * `main.py` runs normal, soft (0.05×) and loud (6×, clipped) versions of a test file through the pipeline and prints input vs output RMS levels. Loud input is attenuated by about 8 dB, normal speech by about 2 dB, and soft input is unchanged (it stays below the compression threshold).

## File Structure & Modules

* `main.py`: Runs the full pipeline (filterbank → envelope → compression → sum) on normal, soft and loud test signals, writes FLAC outputs and prints RMS levels.
* `signals.py`, `filters.py`: Audio loading (16 kHz required) and the 6-band Butterworth filterbank.
* `envelope.py`: First-order envelope detector.
* `compression.py`: Per-band compression: static curve plus attack/release gain smoothing.
* `reconstruct.py`: Filterbank-only check. Plots each band, the sum of bands vs the original, the reconstruction error, and prints the reconstruction SNR. It does not run the compressor.
* `profile.py`: Mock patient audiogram (Hearing Level in dB HL at 250 Hz–8 kHz).
* `gain.py`: Computes a per-band target gain with a simple linear rule: gain = 0.6 × HL.
* `audio_gain.py`: Applies those static gains to the bands. **Not currently used by the pipeline.**

## Known Issues / Future Optimizations

* **Filter stability:** The filterbank uses `scipy.signal.butter`'s polynomial (`b, a`) output. For narrow low-frequency bandpass bands this is poorly conditioned and can cause numerical instability. Planned fix: Second-Order Sections (`output='sos'` with `sosfilt`).
* **Band recombination:** The six bands are overlapping causal Butterworth filters summed directly. Output RMS level is preserved (soft test: −0.1 dB), but the waveform is not: on the test file the reconstruction error peaks at roughly 0.6–0.8 against a signal peak of about 0.35, because adjacent bands have different phase at the crossovers. A proper crossover design (e.g. Linkwitz–Riley) or zero-phase filtering would fix this. `reconstruct.py` plots and prints the error.
* **No prescribed gain in the pipeline:** `gain.py` and `audio_gain.py` compute and apply audiogram-based gain, but `compression.py` does not use them. Soft sounds are not amplified.
* **Offline only:** Envelope and gain smoothing use per-sample Python loops, so this is a simulation and not real-time.
* **Levels are dBFS**, not dB SPL.

## Example results (test file: LibriSpeech 84-121123-0002)

| Input | RMS before (dB) | RMS after (dB) | Change |
|-------|-----------------|----------------|--------|
| Normal | −23.61 | −25.62 | −2.01 |
| Soft (0.05×) | −49.63 | −49.73 | −0.10 |
| Loud (6×, clipped) | −8.61 | −16.50 | −7.89 |

The soft result (−0.1 dB) shows the filterbank itself barely changes the level, so the changes on the other rows come from compression. The loud input is clipped before processing, so it already contains distortion.

Filterbank-only reconstruction SNR on the same file: **-4.5 dB** (printed by `reconstruct.py`).

## Usage

Requires `numpy`, `scipy`, `soundfile`, `matplotlib`. Input audio must be 16 kHz (mono or stereo; resampling is not implemented). A 13.7 s sample (`84-121123-0002.flac`, from LibriSpeech, CC BY 4.0, Panayotov et al. 2015) is included in the repo, so both scripts run with no arguments.

```bash
python main.py          # full pipeline: writes compressed FLACs to the current folder, prints RMS levels
python reconstruct.py   # filterbank check: band plots, reconstruction error and SNR
```

Both scripts also accept a path to your own 16 kHz audio file as the first argument.
