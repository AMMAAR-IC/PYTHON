import os, msvcrt, random, time

WIDTH, HEIGHT = 20, 10
maze = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]
px, py = 1, 1
maze[py][px] = '☣'

def print_maze():
    os.system('cls')
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x == WIDTH - 1 or y == HEIGHT - 1 or x == 0 or y == 0:
                print('#', end='')
            else:
                print(maze[y][x], end='')
        print()

print_maze()
while True:
    key = msvcrt.getch()
    dx, dy = 0, 0
    if key == b'H': dy = -1   # up
    elif key == b'P': dy = 1   # down
    elif key == b'K': dx = -1  # left
    elif key == b'M': dx = 1   # right

    newx, newy = px + dx, py + dy
    if 0 < newx < WIDTH - 1 and 0 < newy < HEIGHT - 1:
        maze[py][px] = ' '
        px, py = newx, newy
        maze[py][px] = '☣'
    print_maze()
