import numpy as np
from scipy.io.wavfile import write, read
import argparse

def encode_bytes_to_waveform(data: bytes) -> np.ndarray:
    waveform = np.frombuffer(data, dtype=np.uint8)
    return (waveform.astype(np.int16) - 128).astype(np.int8)

def pad_waveform_loop(waveform: np.ndarray, target_length: int) -> np.ndarray:
    if len(waveform) >= target_length:
        return waveform[:target_length]
    repeats = target_length // len(waveform)
    remainder = target_length % len(waveform)
    extended = np.tile(waveform, repeats)
    if remainder > 0:
        extended = np.concatenate([extended, waveform[:remainder]])
    return extended

def interleave_base3_and_signal_base_scaled(base: np.ndarray, signal: np.ndarray, base_scale: int = 2) -> np.ndarray:
    if base.ndim == 2:
        base = base[:, 0]

    max_len = len(base) // 3
    usable_signal_len = min(len(signal), max_len)

    base = base[:usable_signal_len * 3]
    signal = signal[:usable_signal_len]

    base_scaled = base.astype(np.int16) * (base_scale * 0.5)
    base_reshaped = base_scaled.reshape((usable_signal_len, 3))

    combined = np.zeros((usable_signal_len, 4), dtype=np.int16)
    combined[:, 0:3] = base_reshaped
    combined[:, 3] = signal.astype(np.int16)

    return combined.reshape(-1)

def main():
    parser = argparse.ArgumentParser(description="Audio steganography tool: Embed binary data into a base WAV audio")
    parser.add_argument("--target", required=True, help="Binary file to embed")
    parser.add_argument("--base", required=True, help="Base WAV audio file")
    parser.add_argument("--output", default="combined_audio.wav", help="Output WAV filename")
    args = parser.parse_args()

    base_rate, base_wave = read(args.base)

    with open(args.target, "rb") as f:
        original_bytes = f.read()

    signal_wave = encode_bytes_to_waveform(original_bytes)
    signal_wave_padded = pad_waveform_loop(signal_wave, len(base_wave) // 3)
    combined_wave = interleave_base3_and_signal_base_scaled(base_wave, signal_wave_padded)

    combined_rate = int(base_rate * 4 / 3)
    write(args.output, combined_rate, combined_wave)
    print(f"[+] Embedded binary data into audio: {args.output}")

if __name__ == "__main__":
    main()
