def is_valid_sudoku(board):
    for i in range(9):
        row = set()
        col = set()
        box = set()
        for j in range(9):
            # Row
            if board[i][j] in row: return False
            if board[i][j] != 0: row.add(board[i][j])

            # Column
            if board[j][i] in col: return False
            if board[j][i] != 0: col.add(board[j][i])

            # Box
            r = 3 * (i // 3) + j // 3
            c = 3 * (i % 3) + j % 3
            if board[r][c] in box: return False
            if board[r][c] != 0: box.add(board[r][c])
    return True

# Sample valid board
sudoku = [
    [5,3,4,6,7,8,9,1,2],
    [6,7,2,1,9,5,3,4,8],
    [1,9,8,3,4,2,5,6,7],
    [8,5,9,7,6,1,4,2,3],
    [4,2,6,8,5,3,7,9,1],
    [7,1,3,9,2,4,8,5,6],
    [9,6,1,5,3,7,2,8,4],
    [2,8,7,4,1,9,6,3,5],
    [3,4,5,2,8,6,1,7,9]
]

print("✅ Valid Sudoku" if is_valid_sudoku(sudoku) else "❌ Invalid Sudoku")
