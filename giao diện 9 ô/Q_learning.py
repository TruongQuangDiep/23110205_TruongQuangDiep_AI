import random
import time
from function import run_gui
from utils import is_goal_state, is_valid, row, col, heuristic

def board_to_tuple(board):
    return tuple(tuple(r) for r in board)

def get_possible_moves(board, x, y):
    moves = []
    for i in range(4):
        new_x, new_y = x + row[i], y + col[i]
        if is_valid(new_x, new_y):
            new_board = [r[:] for r in board]
            new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
            moves.append((new_board, new_x, new_y, i))
    return moves

def solve_puzzle_q_learning_core(
    start, x, y, display_mode=None, update_display=None,
    episodes=50000, max_steps=200, alpha=0.7, gamma=0.9, epsilon=0.2
):
    """
    Q-learning cho 8-puzzle. Đã cải tiến: tăng tập luyện, reward dựa heuristic, giảm epsilon dần.
    """
    start_time = time.time()
    Q = dict()  # Q[(state_tuple, action)] = value
    actions = [0, 1, 2, 3]

    # Training phase
    for episode in range(episodes):
        board = [r[:] for r in start]
        curr_x, curr_y = x, y
        state = board_to_tuple(board)
        curr_epsilon = max(0.05, epsilon * (0.995 ** episode))  # Giảm epsilon dần
        for step in range(max_steps):
            # Chọn hành động theo epsilon-greedy
            if random.random() < curr_epsilon:
                action = random.choice(actions)
            else:
                qs = [Q.get((state, a), 0) for a in actions]
                max_q = max(qs)
                best_actions = [a for a, q in zip(actions, qs) if q == max_q]
                action = random.choice(best_actions)
            # Thực hiện hành động
            new_x, new_y = curr_x + row[action], curr_y + col[action]
            if not is_valid(new_x, new_y):
                continue
            new_board = [r[:] for r in board]
            new_board[curr_x][curr_y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[curr_x][curr_y]
            new_state = board_to_tuple(new_board)
            # Phần thưởng cải tiến
            if is_goal_state(new_board):
                reward = 100
            else:
                reward = -1 - heuristic(new_board)  # Phạt nặng hơn nếu xa đích
            # Q-learning update
            old_q = Q.get((state, action), 0)
            next_qs = [Q.get((new_state, a), 0) for a in actions]
            Q[(state, action)] = old_q + alpha * (reward + gamma * max(next_qs) - old_q)
            # Chuyển sang trạng thái mới
            board = new_board
            curr_x, curr_y = new_x, new_y
            state = new_state
            if is_goal_state(board):
                break

    # Exploitation phase: lấy đường đi tốt nhất từ Q-table
    board = [r[:] for r in start]
    curr_x, curr_y = x, y
    state = board_to_tuple(board)
    path = [board]
    visited = set()
    visited.add(state)
    found = False

    for step in range(200):
        if is_goal_state(board):
            found = True
            break
        qs = [Q.get((state, a), -float('inf')) for a in actions]
        max_q = max(qs)
        if max_q == -float('inf'):
            break
        best_actions = [a for a, q in zip(actions, qs) if q == max_q]
        action = random.choice(best_actions)
        new_x, new_y = curr_x + row[action], curr_y + col[action]
        if not is_valid(new_x, new_y):
            break
        new_board = [r[:] for r in board]
        new_board[curr_x][curr_y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[curr_x][curr_y]
        new_state = board_to_tuple(new_board)
        if new_state in visited:
            break
        path.append([r[:] for r in new_board])
        visited.add(new_state)
        board = new_board
        curr_x, curr_y = new_x, new_y
        state = new_state

    end_time = time.time()
    if found:
        if display_mode == "text" and update_display:
            for step, state in enumerate(path):
                display_text = f"Step {step}:\n"
                display_text += "\n".join([" ".join(map(str, row)) for row in state]) + "\n------"
                update_display(display_text)
            update_display(f'Solution found in {len(path) - 1} steps (Q-learning)')
            update_display(f'Time taken: {end_time - start_time:.6f} seconds')
            update_display(f'Nodes expanded: {len(visited)}')
        elif display_mode == "gui":
            run_gui(path)
    else:
        if display_mode == "text" and update_display:
            update_display('No solution found (Q-learning)')

def solve_puzzle_q_learning(start, x, y, update_display):
    """Q-learning hiển thị qua text"""
    solve_puzzle_q_learning_core(start, x, y, display_mode="text", update_display=update_display)

def solve_puzzle_q_learning_giao_dien(start, x, y):
    """Q-learning hiển thị qua giao diện"""
    solve_puzzle_q_learning_core(start, x, y, display_mode="gui")