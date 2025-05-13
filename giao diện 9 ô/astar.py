import heapq
import time
from function import run_gui
from utils import is_goal_state, is_valid, row, col, heuristic

def solve_puzzle_astar_core(start, x, y, display_mode=None, update_display=None):
    """Hàm chung cho A*, hỗ trợ cả hiển thị text và giao diện"""
    start_time = time.time()
    pq = [(heuristic(start), 0, start, x, y, [])]
    visited = set()
    visited.add(tuple(map(tuple, start)))

    while pq:
        _, cost, board, x, y, path = heapq.heappop(pq)
        path = path + [board]

        if is_goal_state(board):
            end_time = time.time()

            if display_mode == "text" and update_display:
                for step, state in enumerate(path):
                    display_text = f"Step {step}:\n"
                    display_text += "\n".join([" ".join(map(str, row)) for row in state]) + "\n------"
                    update_display(display_text)

                update_display(f'Solution found in {len(path) - 1} steps (A*)')
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
                    heapq.heappush(pq, (heuristic(new_board) + cost + 1, cost + 1, new_board, new_x, new_y, path))

    if display_mode == "text" and update_display:
        update_display('No solution found (A*)')
        
def solve_puzzle_astar(start, x, y, update_display):
    """A* hiển thị qua text"""
    solve_puzzle_astar_core(start, x, y, display_mode="text", update_display=update_display)
    
def solve_puzzle_astar_giao_dien(start, x, y):
    """A* hiển thị qua giao diện"""
    solve_puzzle_astar_core(start, x, y, display_mode="gui")