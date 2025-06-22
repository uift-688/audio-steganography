# Audio Steganography Tool

This tool embeds arbitrary binary data into a base WAV audio file by interleaving the data as a low-level audio signal alongside the base audio.

## Overview

The binary data (e.g. images, documents, etc.) is converted to an `int8` waveform and interleaved in groups of four samples with the base audio samples in the pattern:

```

\[ base1, base2, base3, data\_signal ] × N

````

This creates a combined WAV file with the binary data hidden inside the audio.

## Requirements

- Python 3.x
- numpy
- scipy

Install dependencies with:

```bash
pip install numpy scipy
````

## Usage

```bash
python audio_steganography.py --target path/to/data.bin --base path/to/base.wav --output output.wav
```

### Arguments

| Option     | Description                       | Example               |
| ---------- | --------------------------------- | --------------------- |
| `--target` | Binary file to embed              | `secret.zip`          |
| `--base`   | Base WAV audio file (mono/stereo) | `background.wav`      |
| `--output` | Output WAV filename (optional)    | `embedded_output.wav` |

## Notes

* The base audio must be uncompressed WAV format.
* The output audio sample rate is scaled by 4/3 of the base audio rate to account for interleaving.
* This script currently does **not** provide a decoding mechanism.
* The embedded data is represented as subtle signal components alongside the base audio.

## License

BSD 3-Clause License

```
