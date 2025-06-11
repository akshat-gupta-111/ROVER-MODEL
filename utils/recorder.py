# recorder.py

import sounddevice as sd
import scipy.io.wavfile as wav

def record_audio(filename="command.wav", duration=3, fs=44100):
    print("🎤 Listening for command...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, fs, recording)
    print("🔈 Command recorded.")