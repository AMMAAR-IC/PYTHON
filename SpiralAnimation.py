import math, time, os

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def spiral_matrix():
    w, h = 40, 20
    chars = ' .:-=+*#%@'
    while True:
        clear()
        t = time.time()
        for y in range(h):
            row = ''
            for x in range(w):
                dx = x - w // 2
                dy = y - h // 2
                d = math.hypot(dx, dy)
                angle = math.atan2(dy, dx) + t
                value = int((math.sin(5 * angle + d * 0.5 + t) + 1) * 5)
                row += chars[value % len(chars)]
            print(row)
        time.sleep(0.05)

try:
    spiral_matrix()
except KeyboardInterrupt:
    print("\nExiting...")
