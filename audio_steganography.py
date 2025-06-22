import numpy as np
from scipy.io.wavfile import write, read
import argparse

def encode_bytes_to_waveform(data: bytes) -> np.ndarray:
    waveform = np.frombuffer(data, dtype=np.uint8)
    return (waveform.astype(np.int16) - 128).astype(np.int8)

def decode_waveform_to_bytes(waveform: np.ndarray) -> bytes:
    # waveform is expected to be int8 representing values from -128 to 127
    return ((waveform.astype(np.int16) + 128) & 0xFF).astype(np.uint8).tobytes()

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

def extract_signal_from_combined_waveform(combined_waveform: np.ndarray) -> np.ndarray:
    # combined waveform shape: multiple of 4, interleaved as [base0, base1, base2, signal]
    length = len(combined_waveform) // 4
    reshaped = combined_waveform.reshape(length, 4)
    signal = reshaped[:, 3]
    # Return as int8 array
    return signal.astype(np.int8)

def main():
    parser = argparse.ArgumentParser(description="Audio steganography tool: Embed or extract binary data in/from WAV audio")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # create command
    create_parser = subparsers.add_parser("create", help="Embed binary data into base audio")
    create_parser.add_argument("--target", required=True, help="Binary file to embed")
    create_parser.add_argument("--base", required=True, help="Base WAV audio file")
    create_parser.add_argument("--output", default="combined_audio.wav", help="Output WAV filename")

    # drop command
    drop_parser = subparsers.add_parser("drop", help="Extract embedded binary data from audio")
    drop_parser.add_argument("--target", required=True, help="WAV audio file with embedded data")
    drop_parser.add_argument("--output", default="extracted_data.bin", help="Output binary filename")

    args = parser.parse_args()

    if args.command == "create":
        base_rate, base_wave = read(args.base)

        with open(args.target, "rb") as f:
            original_bytes = f.read()

        signal_wave = encode_bytes_to_waveform(original_bytes)
        signal_wave_padded = pad_waveform_loop(signal_wave, len(base_wave) // 3)
        combined_wave = interleave_base3_and_signal_base_scaled(base_wave, signal_wave_padded)

        combined_rate = int(base_rate * 4 / 3)
        write(args.output, combined_rate, combined_wave)
        print(f"[+] Embedded binary data into audio: {args.output}")

    elif args.command == "drop":
        combined_rate, combined_wave = read(args.target)
        signal_wave = extract_signal_from_combined_waveform(combined_wave)
        extracted_bytes = decode_waveform_to_bytes(signal_wave)
        with open(args.output, "wb") as f:
            f.write(extracted_bytes)
        print(f"[+] Extracted embedded data to file: {args.output}")

if __name__ == "__main__":
    main()
