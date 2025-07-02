import os, time, random

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def neurons():
    size = 25
    grid = [[' ']*size for _ in range(size)]
    nodes = [(random.randint(2, size-3), random.randint(2, size-3)) for _ in range(20)]
    
    while True:
        clear()
        grid = [[' ']*size for _ in range(size)]
        for x, y in nodes:
            grid[y][x] = '●'
            for _ in range(random.randint(1, 3)):
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                if dx or dy:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < size and 0 <= ny < size:
                        grid[ny][nx] = random.choice(['-', '|', '*'])
        for row in grid:
            print(''.join(row))
        time.sleep(0.15)

try:
    neurons()
except KeyboardInterrupt:
    print("\nBrain offline.")
