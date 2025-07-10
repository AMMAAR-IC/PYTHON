import time
import threading
from pynput import keyboard
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from datetime import datetime

key_freq = defaultdict(int)
press_times = []
emotion_score = 0

# Basic key positions on a QWERTY keyboard (for heatmap)
layout = [
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm"
]

# Create blank heatmap
heatmap = np.zeros((3, 10))

def update_heatmap():
    for i, row in enumerate(layout):
        for j, key in enumerate(row):
            heatmap[i][j] = key_freq[key]

def display_heatmap():
    plt.clf()
    update_heatmap()
    plt.imshow(heatmap, cmap='hot', interpolation='nearest')
    plt.xticks(range(10), range(1, 11))
    plt.yticks(range(3), ["Top", "Mid", "Bottom"])
    plt.title("🧠 Keyboard Heatmap (Real-time)")
    plt.colorbar()
    plt.pause(0.01)

def analyze_emotion():
    if not press_times:
        return "neutral"
    intervals = [j - i for i, j in zip(press_times[:-1], press_times[1:])]
    avg_speed = sum(intervals) / len(intervals)
    if avg_speed < 0.08:
        return "angry"
    elif avg_speed < 0.15:
        return "focused"
    elif avg_speed < 0.3:
        return "calm"
    else:
        return "tired"

def on_press(key):
    global emotion_score
    try:
        k = key.char.lower()
        if k.isalpha():
            key_freq[k] += 1
            press_times.append(time.time())
    except:
        pass

def logger():
    while True:
        time.sleep(15)
        emotion = analyze_emotion()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🧠 Typing Mood: {emotion.upper()}")
        display_heatmap()

def main():
    print("🔍 Tracking your typing. Press ESC to exit.")
    threading.Thread(target=logger, daemon=True).start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    plt.ion()
    main()
