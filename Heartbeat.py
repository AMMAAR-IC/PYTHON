import os, time, random

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def heartbeat():
    w, h = 60, 10
    pulse = [0] * w

    def beat_frame():
        return [0, 0, 0, 3, 7, 3, 0, 0, -2, 0, 0]

    while True:
        pulse = pulse[len(beat_frame()):] + beat_frame()
        clear()
        for y in range(h):
            row = ''
            for v in pulse:
                row += '|' if h - y - 1 == v else ' '
            print(row)
        time.sleep(0.05)

try:
    heartbeat()
except KeyboardInterrupt:
    print("\nMonitor offline.")
