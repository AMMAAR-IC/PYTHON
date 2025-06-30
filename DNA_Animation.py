import time
import math
import os
import random

base_pairs = [('A', 'T'), ('T', 'A'), ('G', 'C'), ('C', 'G')]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def dna_helix():
    chars = [" ", ".", ":", "-", "=", "*", "#", "%", "@"]

    while True:
        clear()
        for i in range(20):
            angle = i + time.time() * 5
            x = int(15 * math.sin(angle))
            y = int(15 * math.cos(angle))
            bp = random.choice(base_pairs)

            l = 30 + x
            r = 30 - x
            strand = [' '] * 60
            strand[l] = bp[0]
            strand[r] = bp[1]
            mid = (l + r) // 2
            strand[mid] = '-'
            print("".join(strand))
        time.sleep(0.1)

try:
    dna_helix()
except KeyboardInterrupt:
    print("\nExited.")
