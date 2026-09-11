import os, time

PATTERNS = {
    'glider':   [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
    'blinker':  [(1, 0), (1, 1), (1, 2)],
    'toad':     [(1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2)],
    'lwss':     [(0, 1), (0, 4), (1, 0), (2, 0), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3)],
    'r_pentomino': [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)],
}

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def place(pattern, w, h, top=None, left=None):
    cells = PATTERNS[pattern]
    top = h // 2 - 2 if top is None else top
    left = w // 2 - 2 if left is None else left
    return {((r + top) % h, (c + left) % w) for r, c in cells}

def neighbours(cell, w, h):
    r, c = cell
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr or dc:
                yield (r + dr) % h, (c + dc) % w  # the grid wraps into a torus

def step(alive, w, h):
    counts = {}
    for cell in alive:
        for n in neighbours(cell, w, h):
            counts[n] = counts.get(n, 0) + 1
    return {cell for cell, n in counts.items()
            if n == 3 or (n == 2 and cell in alive)}

def draw(alive, w, h, gen):
    rows = [''.join('#' if (r, c) in alive else ' ' for c in range(w)) for r in range(h)]
    print('\n'.join(rows))
    print(f"generation {gen:>4}   population {len(alive):>4}")

def run(pattern='glider', w=60, h=24, generations=120, delay=0.08):
    alive = place(pattern, w, h)
    seen = {}
    for gen in range(generations):
        clear()
        draw(alive, w, h, gen)
        key = frozenset(alive)
        if key in seen:
            print(f"repeats generation {seen[key]} -- period {gen - seen[key]}")
            break
        seen[key] = gen
        alive = step(alive, w, h)
        if not alive:
            print("population died out")
            break
        time.sleep(delay)

try:
    run('glider')
except KeyboardInterrupt:
    print("\nLife stopped.")
