import time
from function import run_gui
from utils import is_goal_state, is_valid, row, col, heuristic

def solve_puzzle_hill_climbing_core(start, x, y, display_mode=None, update_display=None):
    """Hàm chung cho SHC, hỗ trợ cả hiển thị text và giao diện"""
    start_time = time.time()
    current_board = start
    current_x, current_y = x, y
    current_heuristic = heuristic(current_board)
    path = [current_board]
    visited = set()
    visited.add(tuple(map(tuple, current_board)))

    while not is_goal_state(current_board):
        improved = False

        # Thử tất cả các bước di chuyển hợp lệ
        for i in range(4):
            new_x, new_y = current_x + row[i], current_y + col[i]
            if is_valid(new_x, new_y):
                new_board = [r[:] for r in current_board]
                new_board[current_x][current_y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[current_x][current_y]

                board_tuple = tuple(map(tuple, new_board))
                if board_tuple not in visited:
                    h = heuristic(new_board)
                    if h < current_heuristic:  # Chọn trạng thái con đầu tiên tốt hơn
                        current_board, current_x, current_y, current_heuristic = new_board, new_x, new_y, h
                        path.append(current_board)
                        visited.add(board_tuple)
                        improved = True
                        break  # Ngay lập tức di chuyển đến trạng thái con này

        # Nếu không có cải thiện, dừng lại
        if not improved:
            if display_mode == "text" and update_display:
                update_display('No improvement found, stuck in local optimum (SHC)')
            return

    end_time = time.time()

    if display_mode == "text" and update_display:
        for step, state in enumerate(path):
            display_text = f"Step {step}:\n"
            display_text += "\n".join([" ".join(map(str, row)) for row in state]) + "\n------"
            update_display(display_text)

        update_display(f'Solution found in {len(path) - 1} steps (SHC)')
        update_display(f'Time taken: {end_time - start_time:.6f} seconds')
        update_display(f'Nodes expanded: {len(visited)}')
    elif display_mode == "gui":
        run_gui(path)  # Gửi danh sách trạng thái để hiển thị

def solve_puzzle_hill_climbing(start, x, y, update_display):
    """SHC hiển thị qua text"""
    solve_puzzle_hill_climbing_core(start, x, y, display_mode="text", update_display=update_display)

def solve_puzzle_hill_climbing_giao_dien(start, x, y):
    """SHC hiển thị qua giao diện"""
    solve_puzzle_hill_climbing_core(start, x, y, display_mode="gui")