# Ubuntu Whisper Dictation

Local English speech-to-text using whisper.cpp, Python sounddevice, a simple RMS voice activity detector, and a systemd user service.

## Install

```bash
cd ~/projects/whisper-dictation  # or extract this project and cd into it
./install.sh
```

The installer builds whisper.cpp, downloads `base.en`, creates a Python venv, and installs the CLI and user service. Run the installer from the extracted project directory.

## Modes
### PTT mode
1. Activate recording.
2. Speak.
3. Stop recording.
4. The detected speech segment is sent to Whisper.

### Continuous mode
1. Microphone is continuously monitored.
2. VAD detects when you start speaking.
3. Silence detection determines the end of each speech segment.
4. Each segment is automatically sent to Whisper.
5. Recognition continues without manual activation.

## Commands

```bash
whisper-dictation start       # continuous microphone dictation
whisper-dictation status      # current mode / recording state

whisper-dictation ptt         # toggle push-to-talk recording on/off
whisper-dictation continuous  # switch to continuous mode

whisper-dictation stop        # stop daemon
whisper-dictation restart     # restart in continuous mode

whisper-dictation logs        # follow systemd logs

whisper-dictation output      # open output directory
whisper-dictation clear       # clear both transcript files
```

```sh
# 1. Check microphone
arecord -l
# alsamixer for checking

# 2. Start continuous recognition
whisper-dictation continuous
whisper-dictation start

# 3. Check service
whisper-dictation status

# 4. Speak for 10-15 seconds

# 5. Inspect logs
whisper-dictation logs

# 6. Inspect output
cat ~/Documents/Transcriptions/speech.txt

# 7. Stop
whisper-dictation stop
```

The daemon starts in PTT mode (not recording) for privacy. `start` switches to continuous mode. `ptt` toggles capture on/off. Bind `whisper-dictation ptt` to a desktop keyboard shortcut for push-to-talk. For a true hold-to-talk key, use a key-down/key-up hotkey tool; this CLI command is a toggle.

## Output

- `~/Documents/Transcriptions/speech.txt` — one recognized utterance per line.
- `~/Documents/Transcriptions/speech.md` — timestamped Markdown sections.

## Troubleshooting
### check microphone 
```bash
arecord -l
pactl list sources short
systemctl --user status whisper-dictation
journalctl --user -u whisper-dictation -f
```

If the microphone is too quiet or noisy, edit `RMS_THRESHOLD` in `~/.local/share/whisper-dictation/src/speechd.py`. Lower it for quiet microphones; raise it if background noise triggers recognition. Restart the service after edits.

The built-in RMS VAD is deliberately simple. It is not the neural VAD model and may need threshold tuning in noisy environments. The first version processes each detected utterance as a separate Whisper job; longer utterances are split at 20 seconds.

### check input signal 
```sh
cd ~/.local/share/whisper-dictation

.venv/bin/python - <<'PY'
import sounddevice as sd
import numpy as np
import time

print("Default input:", sd.default.device)
print("Devices:")
print(sd.query_devices())

def callback(indata, frames, timing, status):
    rms = np.sqrt(np.mean(indata ** 2))
    print(f"Audio RMS: {rms:.5f}", flush=True)

print("\nSpeak into microphone for 15 seconds.")

with sd.InputStream(
    samplerate=16000,
    channels=1,
    dtype="float32",
    blocksize=1600,
    callback=callback
):
    time.sleep(15)
PY
```

### check whisper 
```sh
WHISPER="$HOME/.local/share/whisper-dictation/whisper.cpp/build/bin/whisper-cli"
MODEL="$HOME/.local/share/whisper-dictation/whisper.cpp/models/ggml-base.en.bin"

arecord -f S16_LE -r 16000 -c 1 -d 8 /tmp/whisper-test.wav

"$WHISPER" \
    -m "$MODEL" \
    -f /tmp/whisper-test.wav \
    -l en
```