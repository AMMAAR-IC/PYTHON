def knights_tour(N):
    board = [[-1]*N for _ in range(N)]
    moves = [(2,1), (1,2), (-1,2), (-2,1), 
             (-2,-1), (-1,-2), (1,-2), (2,-1)]

    def valid(x, y): return 0<=x<N and 0<=y<N and board[x][y]==-1

    def solve(x, y, movei):
        if movei == N*N:
            return True
        for dx, dy in moves:
            nx, ny = x+dx, y+dy
            if valid(nx, ny):
                board[nx][ny] = movei
                if solve(nx, ny, movei+1): return True
                board[nx][ny] = -1
        return False

    board[0][0] = 0
    if solve(0,0,1):
        for row in board:
            print(' '.join(f"{x:2}" for x in row))
    else:
        print("No solution")

knights_tour(5)
