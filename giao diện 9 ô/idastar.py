from utils import is_goal_state, is_valid, row, col, heuristic
from function import run_gui
import time

def depth_limited_search(board, x, y, cost, bound, path, visited, update_display):
    f = cost + heuristic(board)
    if f > bound:
        return f
    if is_goal_state(board):
        return path + [board]

    min_bound = float('inf')
    visited.add(tuple(map(tuple, board)))

    for i in range(4):
        new_x, new_y = x + row[i], y + col[i]
        if is_valid(new_x, new_y):
            new_board = [r[:] for r in board]
            new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]

            board_tuple = tuple(map(tuple, new_board))
            if board_tuple not in visited:
                result = depth_limited_search(new_board, new_x, new_y, cost + 1, bound, path + [board], visited, update_display)
                if isinstance(result, list):
                    return result
                min_bound = min(min_bound, result)

    visited.remove(tuple(map(tuple, board)))
    return min_bound

def solve_puzzle_idastar_core(start, x, y, display_mode=None, update_display=None):
    """Hàm chung cho IDA*, hỗ trợ cả hiển thị text và giao diện"""
    start_time = time.time()
    bound = heuristic(start)

    while True:
        visited = set()
        result = depth_limited_search(start, x, y, 0, bound, [], visited, update_display)
        if isinstance(result, list):  # Nếu tìm thấy lời giải
            end_time = time.time()

            if display_mode == "text" and update_display:
                for step, state in enumerate(result):
                    display_text = f"Step {step}:\n"
                    display_text += "\n".join([" ".join(map(str, row)) for row in state]) + "\n------"
                    update_display(display_text)

                update_display(f'Solution found in {len(result) - 1} steps (IDA*)')
                update_display(f'Time taken: {end_time - start_time:.6f} seconds')
                update_display(f'Nodes expanded: {len(visited)}')
            elif display_mode == "gui":
                run_gui(result)  # Gửi danh sách trạng thái để hiển thị
            return

        bound = result  # Cập nhật giới hạn mới
        
def solve_puzzle_idastar(start, x, y, update_display):
    """IDA* hiển thị qua text"""
    solve_puzzle_idastar_core(start, x, y, display_mode="text", update_display=update_display)

def solve_puzzle_idastar_giao_dien(start, x, y):
    """IDA* hiển thị qua giao diện"""
    solve_puzzle_idastar_core(start, x, y, display_mode="gui")