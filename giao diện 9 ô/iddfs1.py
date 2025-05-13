from utils import is_goal_state, is_valid, row, col
from function import run_gui
import time
def depth_limited_search(board, x, y, depth, path, visited):
    if is_goal_state(board):
        return path + [board]
    if depth == 0:
        return None

    visited.add(tuple(map(tuple, board)))

    for i in range(4):
        new_x, new_y = x + row[i], y + col[i]
        if is_valid(new_x, new_y):
            new_board = [r[:] for r in board]
            new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]

            board_tuple = tuple(map(tuple, new_board))
            if board_tuple not in visited:
                result = depth_limited_search(new_board, new_x, new_y, depth - 1, path + [board], visited)
                if result:
                    return result

    visited.remove(tuple(map(tuple, board)))
    return None

def solve_puzzle_iddfs_core(start, x, y, display_mode=None, update_display=None):
    """Hàm chung cho IDDFS, hỗ trợ cả hiển thị text và giao diện"""
    start_time = time.time()
    depth = 0

    while True:
        visited = set()
        result = depth_limited_search(start, x, y, depth, [], visited)

        if result:
            end_time = time.time()

            if display_mode == "text" and update_display:
                for step, state in enumerate(result):
                    display_text = f"Step {step}:\n"
                    display_text += "\n".join([" ".join(map(str, row)) for row in state]) + "\n------"
                    update_display(display_text)

                update_display(f'Solution found in {len(result) - 1} steps (IDDFS)')
                update_display(f'Time taken: {end_time - start_time:.6f} seconds')
                update_display(f'Nodes expanded: {len(visited)}')
            elif display_mode == "gui":
                run_gui(result)  # Gửi danh sách trạng thái để hiển thị
            return

        depth += 1
        
def solve_puzzle_iddfs(start, x, y, update_display):
    """IDDFS hiển thị qua text"""
    solve_puzzle_iddfs_core(start, x, y, display_mode="text", update_display=update_display)
    
def solve_puzzle_iddfs_giao_dien(start, x, y):
    """IDDFS hiển thị qua giao diện"""
    solve_puzzle_iddfs_core(start, x, y, display_mode="gui")


