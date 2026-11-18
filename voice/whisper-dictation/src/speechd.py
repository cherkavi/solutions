
#!/usr/bin/env python3
"""Local Whisper dictation daemon: continuous recording and push-to-talk."""

import argparse
import datetime as dt
import json
import os
import queue
import signal
import socket
import subprocess
import tempfile
import threading
import time
import wave
from pathlib import Path

import numpy as np
import sounddevice as sd


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

HOME = Path.home()

ROOT = HOME / ".local/share/whisper-dictation"

WHISPER = ROOT / "whisper.cpp/build/bin/whisper-cli"
MODEL = ROOT / "whisper.cpp/models/ggml-base.en.bin"

OUT = HOME / "Documents/Transcriptions"
TXT = OUT / "speech.txt"
MD = OUT / "speech.md"

SOCKET = (
    Path(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}"))
    / "whisper-dictation.sock"
)

RATE = 16000
BLOCK = 1600                    # 100 ms audio blocks

RMS_THRESHOLD = 0.012           # Microphone sensitivity
SILENCE_SECONDS = 0.9           # Silence required to finish a segment
MIN_SPEECH_SECONDS = 0.45       # Ignore very short segments
MAX_SEGMENT_SECONDS = 20        # Maximum segment length

AUDIO_QUEUE_SIZE = 200
TRANSCRIPTION_QUEUE_SIZE = 30


# ---------------------------------------------------------------------
# Daemon
# ---------------------------------------------------------------------

class DictationDaemon:

    def __init__(self):
        self.running = threading.Event()
        self.running.set()

        self.audio_queue = queue.Queue(maxsize=AUDIO_QUEUE_SIZE)
        self.transcription_queue = queue.Queue(
            maxsize=TRANSCRIPTION_QUEUE_SIZE
        )

        self.mode_lock = threading.Lock()
        self.output_lock = threading.Lock()

        self.mode = "ptt"
        self.ptt_active = False

        self.segment = []
        self.segment_duration = 0.0
        self.speech_started = False
        self.silence_blocks = 0

        self.last_text = ""

        self.audio_thread = None
        self.worker_thread = None
        self.socket_thread = None

    # -----------------------------------------------------------------
    # Recording state
    # -----------------------------------------------------------------

    def enabled(self):
        with self.mode_lock:
            return (
                self.mode == "continuous"
                or (self.mode == "ptt" and self.ptt_active)
            )

    def get_status(self):
        with self.mode_lock:
            mode = self.mode
            recording = (
                mode == "continuous"
                or (mode == "ptt" and self.ptt_active)
            )

        return {
            "ok": True,
            "mode": mode,
            "recording": recording,
            "output_txt": str(TXT),
            "output_md": str(MD),
        }

    # -----------------------------------------------------------------
    # Audio callback
    # -----------------------------------------------------------------

    def callback(self, indata, frames, timing, status):

        if status:
            print(f"[AUDIO] {status}", flush=True)

        try:
            block = indata[:, 0].copy()
            self.audio_queue.put_nowait(block)

        except queue.Full:
            print("[AUDIO] Queue full; dropping audio block", flush=True)

        except Exception as exc:
            print(f"[AUDIO] Callback error: {exc}", flush=True)

    # -----------------------------------------------------------------
    # Voice activity detection
    # -----------------------------------------------------------------

    def audio_loop(self):

        print("[AUDIO] Audio processing thread started", flush=True)

        while self.running.is_set() or not self.audio_queue.empty():

            try:
                block = self.audio_queue.get(timeout=0.2)

            except queue.Empty:
                continue

            try:
                if not self.enabled():

                    if self.segment:
                        print(
                            "[VAD] Recording disabled; flushing segment",
                            flush=True
                        )
                        self.finish_segment()

                    continue

                rms = float(
                    np.sqrt(
                        np.mean(
                            np.square(block, dtype=np.float64)
                        )
                    )
                )

                if rms >= RMS_THRESHOLD:

                    if not self.speech_started:
                        print(
                            f"[VAD] Speech detected, RMS={rms:.5f}",
                            flush=True
                        )

                    self.speech_started = True
                    self.silence_blocks = 0

                    self.segment.append(block)
                    self.segment_duration += len(block) / RATE

                elif self.speech_started:

                    # Keep trailing silence in the audio segment.
                    self.segment.append(block)
                    self.segment_duration += len(block) / RATE

                    self.silence_blocks += 1

                if self.speech_started:

                    silence_duration = (
                        self.silence_blocks * BLOCK / RATE
                    )

                    if silence_duration >= SILENCE_SECONDS:

                        print(
                            f"[VAD] Silence detected: "
                            f"{silence_duration:.2f}s",
                            flush=True
                        )

                        self.finish_segment()

                    elif self.segment_duration >= MAX_SEGMENT_SECONDS:

                        print(
                            "[VAD] Maximum segment duration reached",
                            flush=True
                        )

                        self.finish_segment()

            except Exception as exc:
                print(f"[VAD] Processing error: {exc}", flush=True)

        # Flush any remaining audio when the daemon stops.
        if self.segment:
            print("[VAD] Flushing final segment", flush=True)
            self.finish_segment()

        print("[AUDIO] Audio processing thread stopped", flush=True)

    # -----------------------------------------------------------------
    # Segment handoff
    # -----------------------------------------------------------------

    def finish_segment(self):

        if not self.segment:
            return

        segment = self.segment

        duration = self.segment_duration

        self.segment = []
        self.segment_duration = 0.0
        self.speech_started = False
        self.silence_blocks = 0

        print(
            f"[VAD] Segment completed: {duration:.2f}s",
            flush=True
        )

        if duration < MIN_SPEECH_SECONDS:

            print(
                f"[VAD] Segment ignored: shorter than "
                f"{MIN_SPEECH_SECONDS}s",
                flush=True
            )

            return

        try:
            self.transcription_queue.put_nowait(segment)

            print(
                "[QUEUE] Segment submitted for transcription",
                flush=True
            )

        except queue.Full:

            print(
                "[QUEUE] ERROR: Transcription queue full; "
                "segment dropped",
                flush=True
            )

    # -----------------------------------------------------------------
    # Transcription worker
    # -----------------------------------------------------------------

    def transcription_worker(self):

        print("[WORKER] Transcription worker started", flush=True)

        while True:

            samples = self.transcription_queue.get()

            try:
                if samples is None:
                    break

                self.transcribe(samples)

            except Exception as exc:

                print(
                    f"[WORKER] Unexpected transcription error: {exc}",
                    flush=True
                )

            finally:
                self.transcription_queue.task_done()

        print("[WORKER] Transcription worker stopped", flush=True)

    # -----------------------------------------------------------------
    # Whisper execution
    # -----------------------------------------------------------------

    def transcribe(self, samples):

        try:

            audio = np.concatenate(samples)

            duration = len(audio) / RATE

            print(
                f"[WHISPER] Processing {duration:.2f}s of audio",
                flush=True
            )

            with tempfile.TemporaryDirectory(
                prefix="whisper-dictation-"
            ) as td:

                wav_path = Path(td) / "segment.wav"
                txt_base = Path(td) / "result"

                # Convert float32 audio to signed 16-bit PCM.
                pcm = np.clip(
                    audio * 32767,
                    -32768,
                    32767
                ).astype(np.int16)

                with wave.open(str(wav_path), "wb") as wf:

                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(RATE)
                    wf.writeframes(pcm.tobytes())

                cmd = [
                    str(WHISPER),
                    "-m", str(MODEL),
                    "-f", str(wav_path),
                    "-l", "en",
                    "-nt",
                    "-otxt",
                    "-of", str(txt_base),
                ]

                print(
                    f"[WHISPER] Executing: {WHISPER}",
                    flush=True
                )

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=180
                )

                if result.returncode != 0:

                    print(
                        f"[WHISPER] ERROR: Exit code "
                        f"{result.returncode}",
                        flush=True
                    )

                    if result.stderr:
                        print(
                            "[WHISPER] STDERR:\n"
                            + result.stderr[-4000:],
                            flush=True
                        )

                    if result.stdout:
                        print(
                            "[WHISPER] STDOUT:\n"
                            + result.stdout[-2000:],
                            flush=True
                        )

                    return

                output_file = Path(str(txt_base) + ".txt")

                if not output_file.exists():

                    print(
                        "[WHISPER] ERROR: Output file was not created",
                        flush=True
                    )

                    if result.stderr:
                        print(
                            result.stderr[-2000:],
                            flush=True
                        )

                    return

                recognized = output_file.read_text(
                    encoding="utf-8"
                ).strip()

                if not recognized:

                    print(
                        "[WHISPER] No speech recognized",
                        flush=True
                    )

                    return

                print(
                    f"[WHISPER] Recognized: {recognized!r}",
                    flush=True
                )

                self.write_transcript(recognized)

        except subprocess.TimeoutExpired:

            print(
                "[WHISPER] ERROR: Transcription timed out",
                flush=True
            )

        except Exception as exc:

            print(
                f"[WHISPER] ERROR: {type(exc).__name__}: {exc}",
                flush=True
            )

    # -----------------------------------------------------------------
    # Output files
    # -----------------------------------------------------------------


def write_transcript(self, text):

    text = " ".join(text.split()).strip()

    if not text:
        return

    with self.output_lock:

        now = dt.datetime.now().astimezone()

        # Unique filename for every recognized segment.
        timestamp = now.strftime("%Y%m%d_%H%M%S_%f")

        OUT.mkdir(parents=True, exist_ok=True)

        txt_file = OUT / f"{timestamp}.txt"
        md_file = OUT / f"{timestamp}.md"

        stamp = now.strftime("%Y-%m-%d %H:%M:%S %Z")

        # Individual TXT file.
        txt_file.write_text(
            text + "\n",
            encoding="utf-8"
        )

        # Individual Markdown file.
        md_file.write_text(
            f"# Transcription\n\n"
            f"**Date:** {stamp}\n\n"
            f"{text}\n",
            encoding="utf-8"
        )

        # Append to aggregate TXT file.
        with TXT.open("a", encoding="utf-8") as f:
            f.write(text + "\n")

        # Append to aggregate Markdown file.
        with MD.open("a", encoding="utf-8") as f:
            f.write(
                f"\n### {stamp}\n\n"
                f"{text}\n"
            )

        print(
            f"[OUTPUT] Created: {txt_file.name}, {md_file.name}",
            flush=True
        )

    # -----------------------------------------------------------------
    # Socket commands
    # -----------------------------------------------------------------

    def handle_command(self, command):

        action = command.get("action")

        if action == "mode":

            mode = command.get("mode")

            if mode not in ("continuous", "ptt"):

                return {
                    "ok": False,
                    "error": "mode must be continuous or ptt"
                }

            with self.mode_lock:
                self.mode = mode
                self.ptt_active = False

            print(
                f"[CONTROL] Mode changed to {mode}",
                flush=True
            )

        elif action == "toggle":

            with self.mode_lock:

                self.mode = "ptt"
                self.ptt_active = not self.ptt_active

                active = self.ptt_active

            print(
                f"[CONTROL] Push-to-talk "
                f"{'activated' if active else 'deactivated'}",
                flush=True
            )

        elif action == "status":

            return self.get_status()

        elif action == "shutdown":

            print("[CONTROL] Shutdown requested", flush=True)
            self.running.clear()

        else:

            return {
                "ok": False,
                "error": "unknown action"
            }

        return self.get_status()

    def socket_loop(self):

        SOCKET.parent.mkdir(parents=True, exist_ok=True)

        try:

            SOCKET.unlink(missing_ok=True)

            with socket.socket(
                socket.AF_UNIX,
                socket.SOCK_STREAM
            ) as server:

                server.bind(str(SOCKET))
                os.chmod(SOCKET, 0o600)

                server.listen(5)
                server.settimeout(0.5)

                print(
                    f"[SOCKET] Listening on {SOCKET}",
                    flush=True
                )

                while self.running.is_set():

                    try:
                        conn, _ = server.accept()

                    except socket.timeout:
                        continue

                    with conn:

                        try:

                            raw = conn.recv(4096)

                            command = json.loads(
                                raw.decode("utf-8")
                            )

                            response = self.handle_command(
                                command
                            )

                        except Exception as exc:

                            response = {
                                "ok": False,
                                "error": str(exc)
                            }

                        conn.sendall(
                            (
                                json.dumps(response) + "\n"
                            ).encode("utf-8")
                        )

        except Exception as exc:

            print(
                f"[SOCKET] ERROR: {exc}",
                flush=True
            )

            self.running.clear()

        finally:

            SOCKET.unlink(missing_ok=True)

            print(
                "[SOCKET] Socket server stopped",
                flush=True
            )

    # -----------------------------------------------------------------
    # Main
    # -----------------------------------------------------------------

    def run(self):

        if not WHISPER.exists():

            raise SystemExit(
                f"Whisper executable missing:\n{WHISPER}"
            )

        if not MODEL.exists():

            raise SystemExit(
                f"Whisper model missing:\n{MODEL}"
            )

        OUT.mkdir(parents=True, exist_ok=True)

        print(
            "[START] Whisper dictation daemon",
            flush=True
        )

        print(
            f"[START] Whisper: {WHISPER}",
            flush=True
        )

        print(
            f"[START] Model: {MODEL}",
            flush=True
        )

        print(
            f"[START] Output directory: {OUT}",
            flush=True
        )

        print(
            f"[START] Initial mode: {self.mode}",
            flush=True
        )

        # Start transcription worker.
        self.worker_thread = threading.Thread(
            target=self.transcription_worker,
            name="whisper-worker",
            daemon=True
        )

        self.worker_thread.start()

        # Start audio processing.
        self.audio_thread = threading.Thread(
            target=self.audio_loop,
            name="audio-processing",
            daemon=True
        )

        self.audio_thread.start()

        # Start command socket.
        self.socket_thread = threading.Thread(
            target=self.socket_loop,
            name="socket-server",
            daemon=True
        )

        self.socket_thread.start()

        try:

            print(
                "[START] Opening microphone",
                flush=True
            )

            with sd.InputStream(
                samplerate=RATE,
                channels=1,
                dtype="float32",
                blocksize=BLOCK,
                callback=self.callback
            ):

                print(
                    "[START] Microphone ready",
                    flush=True
                )

                while self.running.is_set():
                    time.sleep(0.25)

        except Exception as exc:

            print(
                f"[AUDIO] Microphone error: {exc}",
                flush=True
            )

            print(
                "[AUDIO] Check microphone devices with: "
                "arecord -l",
                flush=True
            )

            self.running.clear()

        finally:

            print(
                "[STOP] Shutting down daemon",
                flush=True
            )

            self.running.clear()

            # Allow audio thread to finish queued blocks and
            # submit the final segment.
            if self.audio_thread:
                self.audio_thread.join(timeout=10)

            # Send worker shutdown signal after audio processing.
            self.transcription_queue.put(None)

            if self.worker_thread:
                self.worker_thread.join()

            if self.socket_thread:
                self.socket_thread.join(timeout=2)

            SOCKET.unlink(missing_ok=True)

            print(
                "[STOP] Whisper dictation daemon stopped",
                flush=True
            )


# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=["ptt", "continuous"],
        default="ptt"
    )

    args = parser.parse_args()

    daemon = DictationDaemon()
    daemon.mode = args.mode

    signal.signal(
        signal.SIGTERM,
        lambda *_: daemon.running.clear()
    )

    signal.signal(
        signal.SIGINT,
        lambda *_: daemon.running.clear()
    )

    daemon.run()
