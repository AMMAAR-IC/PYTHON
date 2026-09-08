import os, time, random

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def matrix_clock():
    columns = 80
    chars = '01'
    while True:
        clear()
        clock = time.strftime("%H:%M:%S")
        for _ in range(18):
            line = ''.join(random.choice(chars) for _ in range(columns))
            print('\033[32m' + line)
        print(f"\n\033[92m{' ' * ((columns - len(clock)) // 2)}⏱️ {clock} ⏱️")
        time.sleep(1)

matrix_clock()
