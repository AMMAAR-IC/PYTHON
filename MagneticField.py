import os, time, math

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def magnetic_field():
    w, h = 80, 24
    cx, cy = w // 2, h // 2
    arrows = ['←','↖','↑','↗','→','↘','↓','↙']

    while True:
        clear()
        for y in range(h):
            row = ''
            for x in range(w):
                dx, dy = x - cx, y - cy
                angle = math.atan2(dy, dx)
                index = int(((angle + math.pi) / (2 * math.pi)) * 8) % 8
                row += arrows[index]
            print(row)
        time.sleep(0.1)

try:
    magnetic_field()
except KeyboardInterrupt:
    print("\nField collapsed.")
