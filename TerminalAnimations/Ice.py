import os, time, random

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def ice_crystal():
    size = 21
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    mid = size // 2
    grid[mid][mid] = '*'

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (1, 1)]

    def grow():
        new = []
        for y in range(size):
            for x in range(size):
                if grid[y][x] == '*':
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < size and 0 <= ny < size and grid[ny][nx] == ' ':
                            if random.random() < 0.2:
                                new.append((nx, ny))
        for x, y in new:
            grid[y][x] = '*'

    while True:
        clear()
        for row in grid:
            print(''.join(row))
        grow()
        time.sleep(0.1)

try:
    ice_crystal()
except KeyboardInterrupt:
    print("\nCrystal frozen.")
