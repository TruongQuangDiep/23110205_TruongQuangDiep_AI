N = 3

row = [0, 0, -1, 1]
col = [-1, 1, 0, 0]

def is_goal_state(board):
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    return board == goal

def is_valid(x, y):
    return 0 <= x < N and 0 <= y < N

def print_board(board):
    for row in board:
        print(' '.join(map(str, row)))
    print("--------")
    
def heuristic(board):
    """Hàm heuristic: Đếm số ô sai vị trí"""
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    return sum(1 for i in range(3) for j in range(3) if board[i][j] and board[i][j] != goal[i][j])
