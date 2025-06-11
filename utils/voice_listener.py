from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os

# Use 'base' or 'tiny' model for speed (tiny is fastest)
model = WhisperModel("tiny", compute_type="auto")  # use 'int8' if you face M1 issues

def listen_for_command(filename="audio/command.wav"):
    fs = 16000
    duration = 3
    print("🎤 Listening for command...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, fs, recording)

    segments, _ = model.transcribe(filename)
    for segment in segments:
        command = segment.text.lower().strip()
        print(f"✅ Heard: '{command}'")
        return command