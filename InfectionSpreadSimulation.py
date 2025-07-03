import os, time, random

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def virus_spread():
    w, h = 30, 15
    grid = [[' ' for _ in range(w)] for _ in range(h)]
    infected = [(h//2, w//2)]
    grid[h//2][w//2] = 'X'

    while True:
        clear()
        new_infected = []
        for y, x in infected:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if (dx or dy) and 0 <= y+dy < h and 0 <= x+dx < w:
                        if grid[y+dy][x+dx] == ' ' and random.random() < 0.25:
                            grid[y+dy][x+dx] = 'X'
                            new_infected.append((y+dy, x+dx))
        infected += new_infected

        for row in grid:
            print(''.join(row))
        time.sleep(0.2)

try:
    virus_spread()
except KeyboardInterrupt:
    print("\nVirus contained.")
