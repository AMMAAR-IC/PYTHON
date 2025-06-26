def solve_maze(maze, x, y, sol):
    n = len(maze)
    if x == n - 1 and y == n - 1 and maze[x][y] == 1:
        sol[x][y] = 1
        return True
    if 0 <= x < n and 0 <= y < n and maze[x][y] == 1:
        sol[x][y] = 1
        if solve_maze(maze, x + 1, y, sol) or solve_maze(maze, x, y + 1, sol):
            return True
        sol[x][y] = 0
    return False

def run_maze_solver():
    maze = [
        [1, 0, 0, 0],
        [1, 1, 0, 1],
        [0, 1, 0, 0],
        [1, 1, 1, 1]
    ]
    n = len(maze)
    sol = [[0]*n for _ in range(n)]
    if solve_maze(maze, 0, 0, sol):
        for row in sol:
            print(row)
    else:
        print("No path found.")
