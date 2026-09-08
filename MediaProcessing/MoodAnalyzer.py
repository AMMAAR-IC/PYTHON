import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SECONDS = 3

p = pyaudio.PyAudio()
print("🎙️ Recording for 3 seconds...")

stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True, frames_per_buffer=CHUNK)

frames = []
for _ in range(int(RATE / CHUNK * SECONDS)):
    data = stream.read(CHUNK)
    frames.append(np.frombuffer(data, dtype=np.int16))

stream.stop_stream()
stream.close()
p.terminate()

audio = np.hstack(frames)
volume = np.mean(np.abs(audio))
energy = np.sum(audio ** 2) / len(audio)

if energy > 1e7:
    mood = "Energetic or Angry 😤"
elif volume > 1000:
    mood = "Happy or Excited 😄"
else:
    mood = "Calm or Sad 😔"

print(f"🧠 Estimated Mood: {mood}") 
