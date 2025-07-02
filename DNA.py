import os, time, random

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def dna_rain():
    w, h = 60, 25
    columns = [0] * w
    chars = ['A', 'T', 'G', 'C']

    while True:
        clear()
        for y in range(h):
            line = ''
            for x in range(w):
                if random.random() < 0.03:
                    line += random.choice(chars)
                else:
                    line += ' '
            print(line)
        time.sleep(0.07)

try:
    dna_rain()
except KeyboardInterrupt:
    print("\nDNA stream cut off.")
