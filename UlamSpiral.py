import matplotlib.pyplot as plt
import math

def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def prime_spiral(n):
    x = y = 0
    dx, dy = 0, -1
    coords = []
    for i in range(1, n**2 + 1):
        if is_prime(i):
            coords.append((x, y))
        if x == y or (x <
