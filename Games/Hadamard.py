import random

def hadamard_choice(options):
    # Simulates a superposition collapse
    weights = [random.random() for _ in options]
    total = sum(weights)
    normalized = [w/total for w in weights]
    return random.choices(options, weights=normalized)[0]

def generate_maze(n):
    maze = [['#'] * n for _ in range(n)]
    stack = [(0, 0)]
    visited = set(stack)

    while stack:
        x, y = stack[-1]
        maze[y][x] = '.'
        neighbors = []

        for dx, dy in [(0,2), (2,0), (0,-2), (-2,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in visited:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = hadamard_choice(neighbors)
            maze[(y+ny)//2][(x+nx)//2] = '.'
            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            stack.pop()
    return maze

def display(maze):
    for row in maze:
        print("".join(row))

display(generate_maze(21))
