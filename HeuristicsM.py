import heapq

def manhattan(state, goal):
    dist = 0
    for i in range(1, 9):
        xi, yi = divmod(state.index(i), 3)
        xg, yg = divmod(goal.index(i), 3)
        dist += abs(xi - xg) + abs(yi - yg)
    return dist

def get_neighbors(state):
    idx = state.index(0)
    moves = []
    x, y = divmod(idx, 3)
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            ni = nx*3 + ny
            new = list(state)
            new[idx], new[ni] = new[ni], new[idx]
            moves.append(tuple(new))
    return moves

def solve_puzzle(start, goal):
    heap = [(manhattan(start, goal), 0, start, [])]
    visited = set()
    while heap:
        est, cost, state, path = heapq.heappop(heap)
        if state == goal:
            return path + [state]
        if state in visited:
            continue
        visited.add(state)
        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                heapq.heappush(heap, (cost + 1 + manhattan(neighbor, goal), cost + 1, neighbor, path + [state]))
    return None

start = (1, 2, 3, 4, 0, 5, 6, 7, 8)
goal  = (1, 2, 3, 4, 5, 6, 7, 8, 0)
solution = solve
