LINES = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]

def winner(board):
    for a, b, c in LINES:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def moves(board):
    return [i for i, cell in enumerate(board) if cell == ' ']

def minimax(board, player, alpha=-2, beta=2, prune=True, counter=None):
    if counter is not None:
        counter[0] += 1

    win = winner(board)
    if win == 'X': return 1, None
    if win == 'O': return -1, None
    if not moves(board): return 0, None

    best_move = None
    if player == 'X':
        best = -2
        for m in moves(board):
            board[m] = 'X'
            score, _ = minimax(board, 'O', alpha, beta, prune, counter)
            board[m] = ' '
            if score > best:
                best, best_move = score, m
            alpha = max(alpha, best)
            if prune and beta <= alpha: break
    else:
        best = 2
        for m in moves(board):
            board[m] = 'O'
            score, _ = minimax(board, 'X', alpha, beta, prune, counter)
            board[m] = ' '
            if score < best:
                best, best_move = score, m
            beta = min(beta, best)
            if prune and beta <= alpha: break
    return best, best_move

def show(board):
    for r in range(0, 9, 3):
        print(' ' + ' | '.join(board[r:r+3]))
        if r < 6: print(' ---+---+---')

def self_play():
    board = [' '] * 9
    player = 'X'
    while winner(board) is None and moves(board):
        _, move = minimax(board, player)
        board[move] = player
        player = 'O' if player == 'X' else 'X'
    return board

board = self_play()
show(board)
print("Result:", winner(board) or "draw", "(perfect play is always a draw)\n")

empty = [' '] * 9
plain, pruned = [0], [0]
minimax(empty[:], 'X', prune=False, counter=plain)
minimax(empty[:], 'X', prune=True, counter=pruned)
print(f"Positions searched without pruning: {plain[0]}")
print(f"Positions searched with alpha-beta: {pruned[0]}")

fork = ['X', ' ', ' ',
        ' ', 'O', ' ',
        ' ', ' ', 'X']
score, move = minimax(fork, 'O')
print(f"\nO to play in a double-threat position -> square {move}, score {score}")
