import time
from function import run_gui
from utils import is_goal_state, is_valid, row, col, heuristic

def and_or_search(state, x, y, path, visited, update_display=None, display_mode=None, depth=0, max_depth=50):
    state_tuple = tuple(map(tuple, state))
    if state_tuple in visited or depth > max_depth:
        return None

    visited.add(state_tuple)
    path = path + [state]

    if is_goal_state(state):
        if display_mode == "text" and update_display:
            for step, s in enumerate(path):
                display_text = f"Step {step}:\n"
                display_text += "\n".join([" ".join(map(str, row)) for row in s]) + "\n------"
                update_display(display_text)
            update_display(f"Solution found in {len(path)-1} steps (AND-OR Search)")
        elif display_mode == "gui":
            run_gui(path)
        return path

    # Sinh các hành động hợp lệ và sắp xếp theo heuristic tăng dần
    moves = []
    for i in range(4):
        new_x, new_y = x + row[i], y + col[i]
        if is_valid(new_x, new_y):
            new_state = [r[:] for r in state]
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            h = heuristic(new_state)
            moves.append((h, new_state, new_x, new_y))
    moves.sort()  # Ưu tiên trạng thái có heuristic nhỏ hơn

    for h, new_state, new_x, new_y in moves:
        result = and_or_search(new_state, new_x, new_y, path, visited, update_display, display_mode, depth+1, max_depth)
        if result is not None:
            return result

    return None

def solve_puzzle_and_or_core(start, x, y, display_mode=None, update_display=None):
    start_time = time.time()
    visited = set()
    result = and_or_search(start, x, y, [], visited, update_display, display_mode)
    end_time = time.time()
    if result is None and display_mode == "text" and update_display:
        update_display("No solution found (AND-OR Search)")
        update_display(f"Time taken: {end_time - start_time:.6f} seconds")
    elif result is not None and display_mode == "text" and update_display:
        update_display(f"Time taken: {end_time - start_time:.6f} seconds")
        update_display(f"Nodes expanded: {len(visited)}")

def solve_puzzle_and_or(start, x, y, update_display):
    solve_puzzle_and_or_core(start, x, y, display_mode="text", update_display=update_display)

def solve_puzzle_and_or_giao_dien(start, x, y):
    solve_puzzle_and_or_core(start, x, y, display_mode="gui")