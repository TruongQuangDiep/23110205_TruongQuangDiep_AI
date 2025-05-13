import time
import math
import random
from function import run_gui
from utils import is_goal_state, is_valid, row, col, heuristic

def solve_puzzle_simulated_annealing_core(start, x, y, display_mode=None, update_display=None):
    """Hàm chung cho Simulated Annealing, hỗ trợ cả hiển thị text và giao diện"""
    start_time = time.time()
    current_board = start
    current_x, current_y = x, y
    current_heuristic = heuristic(current_board)
    path = [current_board]
    visited = set()
    visited.add(tuple(map(tuple, current_board)))

    # Tham số Simulated Annealing
    T = 100.0  # Nhiệt độ ban đầu
    cooling_rate = 0.99  # Tỷ lệ giảm nhiệt độ
    min_temperature = 0.1  # Nhiệt độ tối thiểu

    while T > min_temperature and not is_goal_state(current_board):
        improved = False  # Biến để kiểm tra có cải thiện hay không

        for i in range(4):
            new_x, new_y = current_x + row[i], current_y + col[i]
            if is_valid(new_x, new_y):
                new_board = [r[:] for r in current_board]
                new_board[current_x][current_y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[current_x][current_y]
                board_tuple = tuple(map(tuple, new_board))
                new_h = heuristic(new_board)

                # Nếu bước đi tốt hơn hoặc chấp nhận bước đi xấu hơn với xác suất
                if board_tuple not in visited:
                    delta_h = new_h - current_heuristic
                    if delta_h < 0 or math.exp(-delta_h / T) > random.random():
                        current_board, current_x, current_y, current_heuristic = new_board, new_x, new_y, new_h
                        path.append(current_board)
                        visited.add(tuple(map(tuple, current_board)))
                        improved = True
                        break

        # Giảm nhiệt độ
        T *= cooling_rate

        if not improved:  # Nếu không có cải thiện, dừng lại
            if display_mode == "text" and update_display:
                update_display('No improvement found, stuck in local optimum (Simulated Annealing)')
            return

    end_time = time.time()

    if display_mode == "text" and update_display:
        for step, state in enumerate(path):
            display_text = f"Step {step}:\n"
            display_text += "\n".join([" ".join(map(str, row)) for row in state]) + "\n------"
            update_display(display_text)

        update_display(f'Solution found in {len(path) - 1} steps (Simulated Annealing)')
        update_display(f'Time taken: {end_time - start_time:.6f} seconds')
        update_display(f'Nodes expanded: {len(visited)}')
    elif display_mode == "gui":
        run_gui(path)  # Gửi danh sách trạng thái để hiển thị

def solve_puzzle_simulated_annealing(start, x, y, update_display):
    """Simulated Annealing hiển thị qua text"""
    solve_puzzle_simulated_annealing_core(start, x, y, display_mode="text", update_display=update_display)

def solve_puzzle_simulated_annealing_giao_dien(start, x, y):
    """Simulated Annealing hiển thị qua giao diện"""
    solve_puzzle_simulated_annealing_core(start, x, y, display_mode="gui")