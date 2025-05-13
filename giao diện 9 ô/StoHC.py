import time
import random
from function import run_gui
from utils import is_goal_state, is_valid, row, col, heuristic

def solve_puzzle_stochastic_core(start, x, y, display_mode=None, update_display=None):
    """Thuật toán Stochastic Hill Climbing"""
    start_time = time.time()
    current_board = start
    current_x, current_y = x, y
    current_heuristic = heuristic(current_board)
    path = [current_board]
    visited = set()
    visited.add(tuple(map(tuple, current_board)))

    while not is_goal_state(current_board):
        better_neighbors = []

        # Xét tất cả các bước di chuyển hợp lệ
        for i in range(4):
            new_x, new_y = current_x + row[i], current_y + col[i]
            if is_valid(new_x, new_y):
                new_board = [r[:] for r in current_board]
                new_board[current_x][current_y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[current_x][current_y]

                board_tuple = tuple(map(tuple, new_board))
                if board_tuple not in visited:
                    h = heuristic(new_board)
                    if h < current_heuristic:
                        better_neighbors.append((new_board, new_x, new_y, h))

        if not better_neighbors:
            if display_mode == "text" and update_display:
                update_display('No better neighbor found (stuck in local optimum)')
            return

        # Chọn ngẫu nhiên một trong các trạng thái tốt hơn
        next_board, next_x, next_y, next_heuristic = random.choice(better_neighbors)
        current_board, current_x, current_y, current_heuristic = next_board, next_x, next_y, next_heuristic
        path.append(current_board)
        visited.add(tuple(map(tuple, current_board)))

    end_time = time.time()

    if display_mode == "text" and update_display:
        for step, state in enumerate(path):
            display_text = f"Step {step}:\n"
            display_text += "\n".join([" ".join(map(str, row)) for row in state]) + "\n------"
            update_display(display_text)

        update_display(f'Solution found in {len(path) - 1} steps (StoHC)')
        update_display(f'Time taken: {end_time - start_time:.6f} seconds')
        update_display(f'Nodes expanded: {len(visited)}')
    elif display_mode == "gui":
        run_gui(path)

def solve_puzzle_stochastic(start, x, y, update_display):
    solve_puzzle_stochastic_core(start, x, y, display_mode="text", update_display=update_display)

def solve_puzzle_stochastic_giao_dien(start, x, y):
    solve_puzzle_stochastic_core(start, x, y, display_mode="gui")
