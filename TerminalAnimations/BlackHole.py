import os, time, math

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def black_hole():
    w, h = 80, 24
    chars = " .,-~:;=!*#$@"

    while True:
        clear()
        t = time.time()
        for y in range(h):
            row = ''
            for x in range(w):
                dx, dy = x - w/2, y - h/2
                r = math.sqrt(dx**2 + dy**2)
                distort = math.sin(r - t*5) / (r+1)
                index = int((distort + 0.5) * (len(chars) - 1))
                index = max(0, min(len(chars)-1, index))
                row += chars[index]
            print(row)
        time.sleep(0.05)

try:
    black_hole()
except KeyboardInterrupt:
    print("\nTime-space reset.")
