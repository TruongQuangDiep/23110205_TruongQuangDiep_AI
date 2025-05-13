import time
from function import run_gui
from utils import is_goal_state, is_valid, row, col

def solve_puzzle_dfs_core(start, x, y, display_mode=None, update_display=None):
    """Hàm chung cho DFS, hỗ trợ cả hiển thị text và giao diện"""
    start_time = time.time()
    stack = [(start, x, y, [])]
    visited = set()
    visited.add(tuple(map(tuple, start)))

    while stack:
        board, x, y, path = stack.pop()
        path = path + [board]

        if is_goal_state(board):
            end_time = time.time()

            if display_mode == "text" and update_display:
                for step, state in enumerate(path):
                    display_text = f"Step {step}:\n"
                    display_text += "\n".join([" ".join(map(str, row)) for row in state]) + "\n------"
                    update_display(display_text)

                update_display(f'Solution found in {len(path) - 1} steps (DFS)')
                update_display(f'Time taken: {end_time - start_time:.6f} seconds')
                update_display(f'Nodes expanded: {len(visited)}')
            elif display_mode == "gui":
                run_gui(path)  # Gửi danh sách trạng thái để hiển thị
            return

        for i in range(4):
            new_x, new_y = x + row[i], y + col[i]
            if is_valid(new_x, new_y):
                new_board = [r[:] for r in board]
                new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]

                board_tuple = tuple(map(tuple, new_board))
                if board_tuple not in visited:
                    visited.add(board_tuple)
                    stack.append((new_board, new_x, new_y, path))

    if display_mode == "text" and update_display:
        update_display('No solution found (DFS)')

def solve_puzzle_dfs(start, x, y, update_display):
    """DFS hiển thị qua text"""
    solve_puzzle_dfs_core(start, x, y, display_mode="text", update_display=update_display)
    
def solve_puzzle_dfs_giao_dien(start, x, y):
    """DFS hiển thị qua giao diện"""
    solve_puzzle_dfs_core(start, x, y, display_mode="gui")