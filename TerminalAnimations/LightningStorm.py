import os, time, random

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def lightning():
    width, height = 60, 20
    ground = ['=' * width]
    
    while True:
        clear()
        sky = [[' ' for _ in range(width)] for _ in range(height)]
        x = random.randint(10, width-10)
        bolt_path = [(x, 0)]

        for _ in range(height - 1):
            dx = random.choice([-1, 0, 1])
            x = max(0, min(width - 1, x + dx))
            bolt_path.append((x, len(bolt_path)))

        for x, y in bolt_path:
            sky[y][x] = '|'
            if random.random() < 0.3:
                sky[y][x] = random.choice(['\\', '|', '/'])

        for row in sky:
            print(''.join(row))
        print(ground[0])
        time.sleep(0.2)

try:
    lightning()
except KeyboardInterrupt:
    print("\nLightning gone.")
