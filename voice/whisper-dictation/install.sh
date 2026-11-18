#!/usr/bin/env bash
set -euo pipefail
PROJECT="$HOME/projects/whisper-dictation"
DEST="$HOME/.local/share/whisper-dictation"
BIN="$HOME/.local/bin"
UNIT="$HOME/.config/systemd/user"

sudo apt update
sudo apt install -y git cmake build-essential python3 python3-venv python3-pip libportaudio2 portaudio19-dev alsa-utils curl
mkdir -p "$PROJECT" "$DEST" "$BIN" "$UNIT"
if [[ ! -d "$PROJECT/whisper.cpp/.git" ]]; then
  git clone https://github.com/ggml-org/whisper.cpp.git "$PROJECT/whisper.cpp"
fi
cmake -S "$PROJECT/whisper.cpp" -B "$PROJECT/whisper.cpp/build" -DCMAKE_BUILD_TYPE=Release
cmake --build "$PROJECT/whisper.cpp/build" -j"$(nproc)"
if [[ ! -f "$PROJECT/whisper.cpp/models/ggml-base.en.bin" ]]; then
  bash "$PROJECT/whisper.cpp/models/download-ggml-model.sh" base.en
fi
# Keep the runtime tree self-contained under ~/.local/share.
rm -rf "$DEST/whisper.cpp"
cp -a "$PROJECT/whisper.cpp" "$DEST/whisper.cpp"
python3 -m venv "$DEST/.venv"
"$DEST/.venv/bin/pip" install --upgrade pip
"$DEST/.venv/bin/pip" install numpy sounddevice
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$DEST/src"
install -m 755 "$SCRIPT_DIR/src/speechd.py" "$DEST/src/speechd.py"
install -m 755 "$SCRIPT_DIR/bin/whisper-dictation" "$BIN/whisper-dictation"
install -m 644 "$SCRIPT_DIR/systemd/whisper-dictation.service" "$UNIT/whisper-dictation.service"
systemctl --user daemon-reload
systemctl --user enable whisper-dictation.service
mkdir -p "$HOME/Documents/Transcriptions"
echo
echo "Installation complete. Ensure ~/.local/bin is in PATH."
echo "Start continuous transcription: whisper-dictation start"
echo "Push-to-talk toggle:          whisper-dictation ptt"
