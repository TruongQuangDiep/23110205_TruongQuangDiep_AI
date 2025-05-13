import time
from function import run_gui
from utils import is_goal_state, is_valid, row, col, heuristic

def solve_puzzle_steepest_ascent_core(start, x, y, display_mode=None, update_display=None):
    """Hàm chung cho SAHC, hỗ trợ cả hiển thị text và giao diện"""
    start_time = time.time()
    current_board = start
    current_x, current_y = x, y
    current_heuristic = heuristic(current_board)
    path = [current_board]
    visited = set()
    visited.add(tuple(map(tuple, current_board)))

    while not is_goal_state(current_board):
        next_board = None
        next_x, next_y = None, None
        next_heuristic = float('inf')

        # Thử tất cả các bước di chuyển hợp lệ
        for i in range(4):
            new_x, new_y = current_x + row[i], current_y + col[i]
            if is_valid(new_x, new_y):
                new_board = [r[:] for r in current_board]
                new_board[current_x][current_y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[current_x][current_y]

                board_tuple = tuple(map(tuple, new_board))
                if board_tuple not in visited:
                    h = heuristic(new_board)
                    if h < next_heuristic:  # Chọn trạng thái con tốt nhất
                        next_board = new_board
                        next_x, next_y = new_x, new_y
                        next_heuristic = h

        # Nếu không có trạng thái con tốt hơn, dừng lại
        if next_board is None or next_heuristic >= current_heuristic:
            if display_mode == "text" and update_display:
                update_display('No improvement found, stuck in local optimum (SAHC)')
            return

        # Cập nhật trạng thái hiện tại
        current_board, current_x, current_y, current_heuristic = next_board, next_x, next_y, next_heuristic
        path.append(current_board)
        visited.add(tuple(map(tuple, current_board)))

    end_time = time.time()

    if display_mode == "text" and update_display:
        for step, state in enumerate(path):
            display_text = f"Step {step}:\n"
            display_text += "\n".join([" ".join(map(str, row)) for row in state]) + "\n------"
            update_display(display_text)

        update_display(f'Solution found in {len(path) - 1} steps (SAHC)')
        update_display(f'Time taken: {end_time - start_time:.6f} seconds')
        update_display(f'Nodes expanded: {len(visited)}')
    elif display_mode == "gui":
        run_gui(path)  # Gửi danh sách trạng thái để hiển thị

def solve_puzzle_steepest_ascent(start, x, y, update_display):
    """SAHC hiển thị qua text"""
    solve_puzzle_steepest_ascent_core(start, x, y, display_mode="text", update_display=update_display)

def solve_puzzle_steepest_ascent_giao_dien(start, x, y):
    """SAHC hiển thị qua giao diện"""
    solve_puzzle_steepest_ascent_core(start, x, y, display_mode="gui")