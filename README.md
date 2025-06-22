# Audio Steganography Tool

This tool allows you to embed arbitrary binary data into a base WAV audio file and later extract it back.

## Usage

### Embed data into audio (`create`)

```bash
python script.py create --target secret.bin --base base_audio.wav --output embedded_audio.wav
````

* `--target` : Binary file you want to embed into audio
* `--base` : Base WAV audio file used as carrier
* `--output` : Output WAV file with embedded data (default: `combined_audio.wav`)

### Extract embedded data from audio (`drop`)

```bash
python script.py drop --target embedded_audio.wav --output extracted_data.bin
```

* `--target` : WAV audio file with embedded data
* `--output` : Filename for extracted binary data (default: `extracted_data.bin`)

---

This script converts the binary data into waveform form and interleaves it with the base audio waveform, enabling steganographic embedding. The extraction reads back the embedded data correctly.
