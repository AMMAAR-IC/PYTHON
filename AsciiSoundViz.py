import sounddevice as sd
import numpy as np
import os
import time

BAR_WIDTH = 60
REFRESH_RATE = 0.05  # seconds

def get_volume(data):
    return np.linalg.norm(data) / len(data)

def print_bars(volume, max_volume=0.5):
    os.system("cls" if os.name == "nt" else "clear")
    bar_len = int(min(volume / max_volume, 1.0) * BAR_WIDTH)
    print("🎙️ Terminal Sound Visualizer".center(BAR_WIDTH + 10, "-"))
    print("[" + "#" * bar_len + "-" * (BAR_WIDTH - bar_len) + "]")
    print(f"Volume: {volume:.4f}".center(BAR_WIDTH + 10))
    print("-" * (BAR_WIDTH + 10))

def audio_callback(indata, frames, time_info, status):
    global last_volume
    volume = get_volume(indata)
    last_volume = volume

if __name__ == "__main__":
    last_volume = 0.0
    try:
        with sd.InputStream(callback=audio_callback, channels=1, samplerate=44100):
            while True:
                print_bars(last_volume)
                time.sleep(REFRESH_RATE)
    except KeyboardInterrupt:
        print("\nExited visualizer.")
    except Exception as e:
        print(f"Error: {e}")
