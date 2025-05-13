import heapq
import time
from function import run_gui
from utils import is_goal_state, is_valid, row, col, heuristic

def solve_puzzle_beam_search_core(start, x, y, beam_width, display_mode=None, update_display=None):
    """Hàm chung cho Beam Search, hỗ trợ cả hiển thị text và giao diện"""
    start_time = time.time()
    pq = [(heuristic(start), start, x, y, [])]  # Hàng đợi ưu tiên (heuristic, board, x, y, path)
    visited = set()
    visited.add(tuple(map(tuple, start)))

    while pq:
        # Chỉ giữ lại các trạng thái tốt nhất theo beam_width
        pq = heapq.nsmallest(beam_width, pq)
        next_pq = []

        for _, board, x, y, path in pq:
            path = path + [board]

            if is_goal_state(board):
                end_time = time.time()

                if display_mode == "text" and update_display:
                    for step, state in enumerate(path):
                        display_text = f"Step {step}:\n"
                        display_text += "\n".join([" ".join(map(str, row)) for row in state]) + "\n------"
                        update_display(display_text)

                    update_display(f'Solution found in {len(path) - 1} steps (Beam Search)')
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
                        heapq.heappush(next_pq, (heuristic(new_board), new_board, new_x, new_y, path))

        pq = next_pq

    if display_mode == "text" and update_display:
        update_display('No solution found (Beam Search)')

def solve_puzzle_beam_search(start, x, y, beam_width, update_display):
    """Beam Search hiển thị qua text"""
    solve_puzzle_beam_search_core(start, x, y, beam_width, display_mode="text", update_display=update_display)

def solve_puzzle_beam_search_giao_dien(start, x, y, beam_width):
    """Beam Search hiển thị qua giao diện"""
    solve_puzzle_beam_search_core(start, x, y, beam_width, display_mode="gui")