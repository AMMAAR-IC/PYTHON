import heapq

def astar(start, goal, grid):
    def h(a, b): return abs(a[0]-b[0]) + abs(a[1]-b[1])
    open_set = [(0 + h(start, goal), 0, start, [])]
    visited = set()

    while open_set:
        f, g, node, path = heapq.heappop(open_set)
        if node in visited: continue
        visited.add(node)
        path = path + [node]
        if node == goal: return path
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = node[0]+dx, node[1]+dy
            if 0<=nx<len(grid) and 0<=ny<len(grid[0]) and grid[nx][ny]==0:
                heapq.heappush(open_set, (g+1+h((nx,ny), goal), g+1, (nx,ny), path))
    return None

grid = [
 [0, 0, 0, 0],
 [1, 1, 0, 1],
 [0, 0, 0, 0],
 [0, 1, 1, 0]
]

path = astar((0,0), (3,3), grid)
print("Path found:" if path else "No path")
print(path)
