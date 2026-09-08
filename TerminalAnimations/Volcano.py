import os, time, random

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def volcano():
    w, h = 60, 20
    vent = w // 2
    lava = []

    while True:
        clear()
        grid = [[' ' for _ in range(w)] for _ in range(h)]
        
        # Add new lava
        for _ in range(random.randint(1, 3)):
            lava.append([vent, h - 2])

        # Move lava upward
        for l in lava:
            l[1] -= 1
            l[0] += random.choice([-1, 0, 1])

        lava[:] = [l for l in lava if l[1] >= 0 and 0 <= l[0] < w]

        # Draw lava
        for x, y in lava:
            grid[y][x] = random.choice(['*', '^', '~'])

        # Draw volcano
        grid[h-1][vent-1:vent+2] = ['/', '|', '\\']

        for row in grid:
            print(''.join(row))
        time.sleep(0.1)

try:
    volcano()
except KeyboardInterrupt:
    print("\nVolcano cooled.")
