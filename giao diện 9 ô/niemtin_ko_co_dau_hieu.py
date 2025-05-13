import tkinter as tk
from tkinter import messagebox
import random
import math
import heapq
import copy
from collections import deque

PUZZLE_SIZE = 3

def flatten(state):
    """Chuyển trạng thái 2D thành tuple 1D để dễ dàng so sánh."""
    return tuple(item for row in state for item in row)

def is_goal_hint_match(state, goal_hint):
    """Kiểm tra xem trạng thái có thỏa mãn dấu hiệu (percept) hay không."""
    for i in range(PUZZLE_SIZE):
        for j in range(PUZZLE_SIZE):
            if goal_hint[i][j] is not None and state[i][j] != goal_hint[i][j]:
                return False
    return True

def generate_random_state(goal_hint):
    """Sinh ngẫu nhiên một trạng thái thỏa mãn dấu hiệu."""
    while True:
        numbers = list(range(9))
        random.shuffle(numbers)
        state = [numbers[i*3:(i+1)*3] for i in range(3)]
        if is_goal_hint_match(state, goal_hint):
            return state

def find_blank(state):
    """Tìm vị trí của ô trống (0) trong trạng thái."""
    for i in range(PUZZLE_SIZE):
        for j in range(PUZZLE_SIZE):
            if state[i][j] == 0:
                return i, j

def get_neighbors(state):
    """Sinh các trạng thái lân cận bằng cách di chuyển ô trống."""
    neighbors = []
    x, y = find_blank(state)
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < PUZZLE_SIZE and 0 <= ny < PUZZLE_SIZE:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def get_neighbors_with_hint(state, hint):
    """Sinh các trạng thái lân cận bằng cách di chuyển ô trống, kiểm tra dấu hiệu."""
    neighbors = []
    size = len(state)
    x, y = find_blank(state)  # Tìm vị trí ô trống (0)

    # Các hướng di chuyển: lên, xuống, trái, phải
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        # Kiểm tra nếu di chuyển hợp lệ (trong giới hạn ma trận)
        if 0 <= nx < size and 0 <= ny < size:
            # Tạo trạng thái mới bằng cách hoán đổi ô trống với ô đích
            new_state = [row[:] for row in state]  # Sao chép trạng thái hiện tại
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]

            # Kiểm tra nếu các ô có dấu hiệu ban đầu không bị thay đổi
            valid = True
            for i in range(size):
                for j in range(size):
                    if hint[i][j] is not None and new_state[i][j] != hint[i][j]:
                        valid = False
                        break
                if not valid:
                    break

            if valid:
                neighbors.append(new_state)

    return neighbors

def bfs(start_states, goal_states, hint):
    """Thuật toán BFS để tìm tất cả các trạng thái từ trạng thái ban đầu đến các trạng thái đích."""
    visited = set()
    visited_states = []  # Lưu tất cả các trạng thái đã xét
    paths = []  # Lưu tất cả các đường đi từ trạng thái đầu đến trạng thái đích

    for start_state in start_states:
        queue = deque([(start_state, [start_state])])  # Hàng đợi BFS cho từng trạng thái đầu
        goal_flat = [flatten(g) for g in goal_states]

        while queue:
            state, path = queue.popleft()
            flat_state = flatten(state) 
  
            if flat_state in visited:
                continue
            visited.add(flat_state)
            visited_states.append(state)  # Lưu trạng thái đã xét

            # Kiểm tra nếu trạng thái hiện tại là trạng thái đích
            if flat_state in goal_flat:
                paths.append(path)  # Lưu đường đi từ trạng thái đầu đến trạng thái đích
                break  # Dừng tìm kiếm cho trạng thái đầu này

            # Sinh tất cả các trạng thái lân cận
            for neighbor in get_neighbors_with_hint(state, hint):
                flat_neighbor = flatten(neighbor)
                if flat_neighbor not in visited and flat_neighbor not in [flatten(s) for s in start_states]:
                    queue.append((neighbor, path + [neighbor]))  # Lưu trạng thái và đường đi đến trạng thái đó

    return paths, visited_states

def dfs(start_states, goal_states, hint, max_depth=30):
    """DFS có giới hạn độ sâu và dừng khi tìm thấy lời giải đầu tiên cho mỗi trạng thái đầu."""
    visited_states = []
    paths = []

    def dfs_recursive(state, path, depth):
        flat_state = flatten(state)
        visited_states.append(state)
        if flat_state in [flatten(g) for g in goal_states]:
            paths.append(path)
            return True
        if depth == 0:
            return False
        for neighbor in get_neighbors_with_hint(state, hint):
            if neighbor not in path:  # tránh lặp lại trạng thái trên đường đi hiện tại
                if dfs_recursive(neighbor, path + [neighbor], depth - 1):
                    return True
        return False

    for start_state in start_states:
        dfs_recursive(start_state, [start_state], max_depth)

    return paths, visited_states

def heuristic(state, goal_state):
    """Hàm heuristic: Tính tổng khoảng cách Manhattan giữa các ô."""
    distance = 0
    for i in range(PUZZLE_SIZE):
        for j in range(PUZZLE_SIZE):
            value = state[i][j]
            if value != 0:  # Không tính ô trống
                for x in range(PUZZLE_SIZE):
                    for y in range(PUZZLE_SIZE):
                        if goal_state[x][y] == value:
                            distance += abs(i - x) + abs(j - y)
    return distance

def a_star(start_states, goal_states, hint):
    """Thuật toán A* tối ưu cho 8-puzzle."""
    visited = set()
    visited_states = []
    paths = []

    for start_state in start_states:
        for goal_state in goal_states:
            heap = []
            heapq.heappush(heap, (heuristic(start_state, goal_state), 0, start_state, [start_state]))
            while heap:
                f, g, state, path = heapq.heappop(heap)
                flat_state = flatten(state)
                if flat_state in visited:
                    continue
                visited.add(flat_state)
                visited_states.append(state)
                if flat_state == flatten(goal_state):
                    paths.append(path)
                    break
                for neighbor in get_neighbors_with_hint(state, hint):
                    flat_neighbor = flatten(neighbor)
                    if flat_neighbor not in visited:
                        h = heuristic(neighbor, goal_state)
                        heapq.heappush(heap, (g + 1 + h, g + 1, neighbor, path + [neighbor]))
    return paths, visited_states

def beam_search(start_states, goal_states, hint, beam_width=5):
    """Thuật toán Beam Search để tìm tất cả các trạng thái từ trạng thái ban đầu đến các trạng thái đích."""
    visited = set()
    visited_states = []  # Lưu tất cả các trạng thái đã xét
    paths = []  # Lưu tất cả các đường đi từ trạng thái đầu đến trạng thái đích

    for start_state in start_states:
        for goal_state in goal_states:
            queue = [(start_state, [start_state])]  # (state, path)

            while queue:
                # Tính heuristic cho tất cả các trạng thái trong hàng đợi
                scored_queue = [(heuristic(state, goal_state), state, path) for state, path in queue]
                scored_queue.sort(key=lambda x: x[0])  # Sắp xếp theo giá trị heuristic (h(n))

                # Chỉ giữ lại `beam_width` trạng thái tốt nhất
                queue = [(state, path) for _, state, path in scored_queue[:beam_width]]

                next_queue = []
                for state, path in queue:
                    flat_state = flatten(state)

                    if flat_state in visited:
                        continue
                    visited.add(flat_state)
                    visited_states.append(state)

                    # Kiểm tra nếu trạng thái hiện tại là trạng thái đích
                    if flat_state == flatten(goal_state):
                        paths.append(path)
                        break

                    # Sinh các trạng thái lân cận
                    for neighbor in get_neighbors_with_hint(state, hint):
                        flat_neighbor = flatten(neighbor)
                        if flat_neighbor not in visited:
                            next_queue.append((neighbor, path + [neighbor]))

                queue = next_queue

    return paths, visited_states

def ida_star(start_states, goal_states, hint, max_nodes=100000):
    """Thuật toán IDA* tối ưu cho 8-puzzle. Một trạng thái đầu chỉ tìm 1 đường đi đến 1 trạng thái đích."""
    visited_states = []
    paths = []
    node_count = [0]

    def search(state, path, g, threshold, goal_state, visited_set):
        flat_state = flatten(state)
        visited_states.append(state)
        node_count[0] += 1
        if node_count[0] > max_nodes:
            return float('inf'), None

        f = g + heuristic(state, goal_state)
        if f > threshold:
            return f, None
        if flat_state == flatten(goal_state):
            return True, path

        min_threshold = float('inf')
        for neighbor in get_neighbors_with_hint(state, hint):
            flat_neighbor = flatten(neighbor)
            if flat_neighbor not in visited_set:
                visited_set.add(flat_neighbor)
                t, result = search(neighbor, path + [neighbor], g + 1, threshold, goal_state, visited_set)
                visited_set.remove(flat_neighbor)
                if t is True:
                    return True, result
                if t < min_threshold:
                    min_threshold = t
        return min_threshold, None

    for start_state in start_states:
        found = False
        for goal_state in goal_states:
            threshold = heuristic(start_state, goal_state)
            while True:
                node_count[0] = 0
                visited_set = set([flatten(start_state)])
                t, result = search(start_state, [start_state], 0, threshold, goal_state, visited_set)
                if t is True:
                    paths.append(result)
                    found = True
                    break
                if t == float('inf') or node_count[0] > max_nodes:
                    break
                threshold = t
            if found:
                break  # Đã tìm ra đường đi cho start_state này, không xét tiếp goal_state khác

    return paths, visited_states

def iddfs(start_states, goal_states, hint):
    """Thuật toán IDDFS để tìm tất cả các trạng thái từ trạng thái ban đầu đến các trạng thái đích."""
    visited_states = []  # Lưu tất cả các trạng thái đã xét
    paths = []  # Lưu tất cả các đường đi từ trạng thái đầu đến trạng thái đích

    def dls(state, path, depth, goal_states):
        """Hàm tìm kiếm theo chiều sâu với giới hạn (Depth-Limited Search)."""
        flat_state = flatten(state)
        visited_states.append(state)

        # Kiểm tra nếu trạng thái hiện tại là trạng thái đích
        if flat_state in [flatten(g) for g in goal_states]:
            paths.append(path)
            return True

        if depth == 0:
            return False

        for neighbor in get_neighbors_with_hint(state, hint):
            if neighbor not in path:  # Tránh lặp lại trạng thái
                if dls(neighbor, path + [neighbor], depth - 1, goal_states):
                    return True
        return False

    for start_state in start_states:
        for goal_state in goal_states:
            depth = 0
            while True:
                if dls(start_state, [start_state], depth, goal_states):
                    break
                depth += 1

    return paths, visited_states

def simulated_annealing(start_states, goal_states, hint, initial_temp=1000, cooling_rate=0.99):
    """Thuật toán Simulated Annealing để tìm trạng thái đích."""
    visited_states = []  # Lưu tất cả các trạng thái đã xét
    paths = []  # Lưu tất cả các đường đi từ trạng thái đầu đến trạng thái đích

    for start_state in start_states:
        for goal_state in goal_states:
            current_state = start_state
            current_path = [current_state]
            temp = initial_temp

            while temp > 1:
                visited_states.append(current_state)

                # Kiểm tra nếu trạng thái hiện tại là trạng thái đích
                if flatten(current_state) == flatten(goal_state):
                    paths.append(current_path)
                    break

                # Lấy trạng thái lân cận ngẫu nhiên
                neighbors = get_neighbors_with_hint(current_state, hint)
                next_state = random.choice(neighbors)

                # Tính năng lượng (heuristic)
                current_energy = heuristic(current_state, goal_state)
                next_energy = heuristic(next_state, goal_state)

                # Quyết định chấp nhận trạng thái mới
                if next_energy < current_energy:
                    current_state = next_state
                    current_path.append(current_state)
                else:
                    prob = math.exp((current_energy - next_energy) / temp)
                    if random.random() < prob:
                        current_state = next_state
                        current_path.append(current_state)

                # Giảm nhiệt độ
                temp *= cooling_rate

    return paths, visited_states

def uniform_cost_search(start_states, goal_states, hint):
    """Thuật toán Uniform Cost Search: mỗi trạng thái đầu chỉ tìm 1 đường đi đến 1 trạng thái đích."""
    visited_states = []
    paths = []

    for start_state in start_states:
        found = False
        for goal_state in goal_states:
            priority_queue = [(0, start_state, [start_state])]
            visited = set()

            while priority_queue:
                cost, state, path = heapq.heappop(priority_queue)
                flat_state = flatten(state)

                if flat_state in visited:
                    continue
                visited.add(flat_state)
                visited_states.append(state)

                # Kiểm tra nếu trạng thái hiện tại là trạng thái đích
                if flat_state == flatten(goal_state):
                    paths.append(path)
                    found = True
                    break

                # Sinh các trạng thái lân cận
                for neighbor in get_neighbors_with_hint(state, hint):
                    flat_neighbor = flatten(neighbor)
                    if flat_neighbor not in visited:
                        heapq.heappush(priority_queue, (cost + 1, neighbor, path + [neighbor]))
            if found:
                break  # Đã tìm ra đường đi cho start_state này, không xét tiếp goal_state khác

    return paths, visited_states

def stochastic_hill_climbing(start_states, goal_states, hint):
    """Thuật toán Stochastic Hill Climbing để tìm trạng thái đích."""
    visited_states = []  # Lưu tất cả các trạng thái đã xét
    paths = []  # Lưu tất cả các đường đi từ trạng thái đầu đến trạng thái đích

    for start_state in start_states:
        for goal_state in goal_states:
            current_state = start_state
            current_path = [current_state]

            while True:
                visited_states.append(current_state)

                # Kiểm tra nếu trạng thái hiện tại là trạng thái đích
                if flatten(current_state) == flatten(goal_state):
                    paths.append(current_path)
                    break

                # Lấy các trạng thái lân cận
                neighbors = get_neighbors_with_hint(current_state, hint)

                # Chọn ngẫu nhiên một trạng thái lân cận tốt hơn
                better_neighbors = [
                    neighbor for neighbor in neighbors
                    if heuristic(neighbor, goal_state) < heuristic(current_state, goal_state)
                ]

                if better_neighbors:
                    current_state = random.choice(better_neighbors)
                    current_path.append(current_state)
                else:
                    # Không có trạng thái lân cận nào tốt hơn, dừng lại
                    break

    return paths, visited_states

def greedy_search(start_states, goal_states, hint, max_nodes=100000):
    """Thuật toán Greedy Search: mỗi trạng thái đầu chỉ tìm 1 đường đi đến 1 trạng thái đích."""
    visited_states = []
    paths = []

    for start_state in start_states:
        found = False
        for goal_state in goal_states:
            priority_queue = [(heuristic(start_state, goal_state), start_state, [start_state])]
            visited = set()
            node_count = 0

            while priority_queue:
                priority_queue.sort(key=lambda x: x[0])
                _, state, path = priority_queue.pop(0)
                flat_state = flatten(state)

                if flat_state in visited:
                    continue
                visited.add(flat_state)
                visited_states.append(state)
                node_count += 1
                if node_count > max_nodes:
                    break

                if flat_state == flatten(goal_state):
                    paths.append(path)
                    found = True
                    break

                for neighbor in get_neighbors_with_hint(state, hint):
                    flat_neighbor = flatten(neighbor)
                    if flat_neighbor not in visited:
                        h = heuristic(neighbor, goal_state)
                        priority_queue.append((h, neighbor, path + [neighbor]))
            if found:
                break  # Đã tìm ra đường đi cho start_state này, không xét tiếp goal_state khác

    return paths, visited_states

def steepest_hill_climbing(start_states, goal_states, hint):
    """Thuật toán Steepest Hill Climbing để tìm trạng thái đích."""
    visited_states = []  # Lưu tất cả các trạng thái đã xét
    paths = []  # Lưu tất cả các đường đi từ trạng thái đầu đến trạng thái đích

    for start_state in start_states:
        for goal_state in goal_states:
            current_state = start_state
            current_path = [current_state]

            while True:
                visited_states.append(current_state)

                # Kiểm tra nếu trạng thái hiện tại là trạng thái đích
                if flatten(current_state) == flatten(goal_state):
                    paths.append(current_path)
                    break

                # Lấy các trạng thái lân cận
                neighbors = get_neighbors_with_hint(current_state, hint)

                # Tìm trạng thái lân cận tốt nhất
                best_neighbor = None
                best_heuristic = float('inf')
                for neighbor in neighbors:
                    h = heuristic(neighbor, goal_state)
                    if h < best_heuristic:
                        best_heuristic = h
                        best_neighbor = neighbor

                # Nếu không có trạng thái tốt hơn, dừng lại
                if best_neighbor and best_heuristic < heuristic(current_state, goal_state):
                    current_state = best_neighbor
                    current_path.append(current_state)
                else:
                    break

    return paths, visited_states

def hill_climbing(start_states, goal_states, hint):
    """Thuật toán Hill Climbing để tìm trạng thái đích."""
    visited_states = []  # Lưu tất cả các trạng thái đã xét
    paths = []  # Lưu tất cả các đường đi từ trạng thái đầu đến trạng thái đích

    for start_state in start_states:
        for goal_state in goal_states:
            current_state = start_state
            current_path = [current_state]

            while True:
                visited_states.append(current_state)

                # Kiểm tra nếu trạng thái hiện tại là trạng thái đích
                if flatten(current_state) == flatten(goal_state):
                    paths.append(current_path)
                    break

                # Lấy các trạng thái lân cận
                neighbors = get_neighbors_with_hint(current_state, hint)

                # Tìm trạng thái lân cận tốt hơn
                next_state = None
                for neighbor in neighbors:
                    if heuristic(neighbor, goal_state) < heuristic(current_state, goal_state):
                        next_state = neighbor
                        break  # Chọn trạng thái lân cận tốt hơn đầu tiên

                # Nếu không có trạng thái tốt hơn, dừng lại
                if next_state:
                    current_state = next_state
                    current_path.append(current_state)
                else:
                    break

    return paths, visited_states

def and_or_search(start_states, goal_states, hint, max_depth=30, max_nodes=100000):
    """Thuật toán AND-OR Search tối ưu cho 8-puzzle với dấu hiệu."""
    visited_states = []
    paths = []
    node_count = [0]

    def search(state, path, depth):
        if depth > max_depth or node_count[0] > max_nodes:
            return None
        visited_states.append(state)
        node_count[0] += 1
        if any(flatten(state) == flatten(goal) for goal in goal_states):
            return path
        for neighbor in get_neighbors_with_hint(state, hint):
            if neighbor not in path:
                result = search(neighbor, path + [neighbor], depth + 1)
                if result:
                    return result
        return None

    for start_state in start_states:
        node_count[0] = 0
        result = search(start_state, [start_state], 0)
        if result:
            paths.append(result)
    return paths, visited_states

def display_states(paths, visited_states):
    """Hiển thị các trạng thái đã xét và đánh dấu trạng thái không nằm trên đường đi."""
    pages = []
    for path in paths:
        pages.append(path)  # Mỗi đường đi là một trang

    page_idx = 0

    def show_page():
        nonlocal page_idx
        text.delete(1.0, tk.END)
        if page_idx < len(pages):
            path = pages[page_idx]
            text.insert(tk.END, f"Trang {page_idx + 1}/{len(pages)}:\n\n")

            # Hiển thị trạng thái đầu
            text.insert(tk.END, "Trạng thái đầu:\n", "start")
            for row in path[0]:
                text.insert(tk.END, " ".join(map(str, row)) + "\n", "start")
            text.insert(tk.END, "\n", "normal")

            # Hiển thị trạng thái trung gian (nếu có)
            if len(path) > 2:
                text.insert(tk.END, "Trạng thái trung gian:\n", "normal")
                for state in path[1:-1]:
                    for row in state:
                        text.insert(tk.END, " ".join(map(str, row)) + "\n", "normal")
                    text.insert(tk.END, "\n", "normal")

            # Hiển thị trạng thái cuối
            text.insert(tk.END, "Trạng thái cuối:\n", "end")
            for row in path[-1]:
                text.insert(tk.END, " ".join(map(str, row)) + "\n", "end")
            text.insert(tk.END, "\n", "end")

        # Hiển thị các trạng thái đã xét nhưng không nằm trên đường đi
        text.insert(tk.END, "Trạng thái đã xét nhưng không nằm trên đường đi:\n", "highlight")
        for state in visited_states:
            if state not in [s for path in paths for s in path]:  # Nếu trạng thái không nằm trên đường đi
                for row in state:
                    text.insert(tk.END, " ".join(map(str, row)) + "\n", "highlight")
                text.insert(tk.END, "\n", "highlight")

    def next_page():
        nonlocal page_idx
        if page_idx + 1 < len(pages):
            page_idx += 1
            show_page()

    def prev_page():
        nonlocal page_idx
        if page_idx > 0:
            page_idx -= 1
            show_page()

    win = tk.Toplevel()
    win.title("Kết quả tìm kiếm")
    win.geometry("+200+100")
    text = tk.Text(win, font=("Consolas", 14), width=30, bg="lightyellow")
    text.pack()

    # Định nghĩa màu sắc
    text.tag_configure("normal", foreground="black")
    text.tag_configure("highlight", foreground="red")
    text.tag_configure("start", foreground="blue")
    text.tag_configure("end", foreground="blue")

    tk.Button(win, text="Trước", command=prev_page).pack(side=tk.LEFT)
    tk.Button(win, text="Sau", command=next_page).pack(side=tk.RIGHT)
    show_page()
    
def display_goal_states(belief_goal):
    """Hiển thị danh sách trạng thái kết thúc."""
    goal_window = tk.Toplevel()
    goal_window.title("Danh sách trạng thái kết thúc")
    goal_window.geometry("+600+100")
    text = tk.Text(goal_window, font=("Consolas", 14), width=40, bg="lightyellow")
    text.pack()
    text.insert(tk.END, "Danh sách trạng thái kết thúc:\n\n")
    for idx, goal in enumerate(belief_goal):
        text.insert(tk.END, f"Trạng thái kết thúc {idx + 1}:\n")
        for row in goal:
            text.insert(tk.END, " ".join(map(str, row)) + "\n")
        text.insert(tk.END, "\n")

def start_search():
    """Hàm chính để bắt đầu tìm kiếm."""
    try:
        # Lấy dấu hiệu từ giao diện
        hint = [[None]*3 for _ in range(3)]
        # Sinh 3 trạng thái ban đầu
        belief_start = []
        while len(belief_start) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_start]:
                belief_start.append(state)

        # Sinh 3 trạng thái đích ngẫu nhiên, thỏa mãn dấu hiệu
        belief_goal = []
        while len(belief_goal) < 3:
            state = generate_random_state(hint)  # Sinh trạng thái đích thỏa mãn dấu hiệu
            if flatten(state) not in [flatten(s) for s in belief_goal]:
                belief_goal.append(state)
                
        # Hiển thị danh sách trạng thái kết thúc
        display_goal_states(belief_goal)

        # Tìm kiếm đường đi
        paths, visited_states = bfs(belief_start, belief_goal, hint)  # Lấy cả paths và visited_states
        if paths:
            display_states(paths, visited_states)  # Truyền cả paths và visited_states
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy đường đi nào.")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        
def start_search_dfs():
    """Hàm chính để bắt đầu tìm kiếm bằng DFS."""
    try:
        # Lấy dấu hiệu từ giao diện
        hint = [[None]*3 for _ in range(3)]
        # Sinh 3 trạng thái ban đầu
        belief_start = []
        while len(belief_start) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_start]:
                belief_start.append(state)

        # Sinh 3 trạng thái đích ngẫu nhiên, thỏa mãn dấu hiệu
        belief_goal = []
        while len(belief_goal) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_goal]:
                belief_goal.append(state)
        
        display_goal_states(belief_goal)

        # Tìm kiếm đường đi bằng DFS
        paths, visited_states = dfs(belief_start, belief_goal, hint)  # Lấy cả paths và visited_states
        if paths:
            display_states(paths, visited_states)  # Truyền cả paths và visited_states
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy đường đi nào.")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        
def start_search_a_star():
    """Hàm chính để bắt đầu tìm kiếm bằng A*."""
    try:
        # Lấy dấu hiệu từ giao diện
        hint = [[None]*3 for _ in range(3)]
        # Sinh 3 trạng thái ban đầu
        belief_start = []
        while len(belief_start) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_start]:
                belief_start.append(state)

        # Sinh 3 trạng thái đích ngẫu nhiên, thỏa mãn dấu hiệu
        belief_goal = []
        while len(belief_goal) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_goal]:
                belief_goal.append(state)
                
        display_goal_states(belief_goal)

        # Tìm kiếm đường đi bằng A*
        paths, visited_states = a_star(belief_start, belief_goal, hint)  # Lấy cả paths và visited_states
        if paths:
            display_states(paths, visited_states)  # Truyền cả paths và visited_states
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy đường đi nào.")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        
def start_search_beam():
    """Hàm chính để bắt đầu tìm kiếm bằng Beam Search."""
    try:
        # Lấy dấu hiệu từ giao diện
        hint = [[None]*3 for _ in range(3)]
        # Sinh 3 trạng thái ban đầu
        belief_start = []
        while len(belief_start) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_start]:
                belief_start.append(state)

        # Sinh 3 trạng thái đích ngẫu nhiên, thỏa mãn dấu hiệu
        belief_goal = []
        while len(belief_goal) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_goal]:
                belief_goal.append(state)
                
        display_goal_states(belief_goal)

        # Tìm kiếm đường đi bằng Beam Search
        beam_width = 2  # Bạn có thể thay đổi kích thước beam tại đây
        paths, visited_states = beam_search(belief_start, belief_goal, hint, beam_width)
        if paths:
            display_states(paths, visited_states)  # Truyền cả paths và visited_states
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy đường đi nào.")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        
def start_search_idastar():
    """Hàm chính để bắt đầu tìm kiếm bằng IDA*."""
    try:
        # Lấy dấu hiệu từ giao diện
        hint = [[None]*3 for _ in range(3)]
        # Sinh 3 trạng thái ban đầu
        belief_start = []
        while len(belief_start) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_start]:
                belief_start.append(state)

        # Sinh 3 trạng thái đích ngẫu nhiên, thỏa mãn dấu hiệu
        belief_goal = []
        while len(belief_goal) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_goal]:
                belief_goal.append(state)

        # Hiển thị danh sách trạng thái kết thúc
        display_goal_states(belief_goal)

        # Tìm kiếm đường đi bằng IDA*
        paths, visited_states = ida_star(belief_start, belief_goal, hint)
        if paths:
            display_states(paths, visited_states)  # Truyền cả paths và visited_states
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy đường đi nào.")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    
def start_search_iddfs():
    """Hàm chính để bắt đầu tìm kiếm bằng IDDFS."""
    try:
        # Lấy dấu hiệu từ giao diện
        hint = [[None]*3 for _ in range(3)]
        # Sinh 3 trạng thái ban đầu
        belief_start = []
        while len(belief_start) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_start]:
                belief_start.append(state)

        # Sinh 3 trạng thái đích ngẫu nhiên, thỏa mãn dấu hiệu
        belief_goal = []
        while len(belief_goal) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_goal]:
                belief_goal.append(state)

        # Hiển thị danh sách trạng thái kết thúc
        display_goal_states(belief_goal)

        # Tìm kiếm đường đi bằng IDDFS
        paths, visited_states = iddfs(belief_start, belief_goal, hint)
        if paths:
            display_states(paths, visited_states)  # Truyền cả paths và visited_states
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy đường đi nào.")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        
def start_search_simulated_annealing():
    """Hàm chính để bắt đầu tìm kiếm bằng Simulated Annealing."""
    try:
        # Lấy dấu hiệu từ giao diện
        hint = [[None]*3 for _ in range(3)]
        # Sinh 3 trạng thái ban đầu
        belief_start = []
        while len(belief_start) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_start]:
                belief_start.append(state)

        # Sinh 3 trạng thái đích ngẫu nhiên, thỏa mãn dấu hiệu
        belief_goal = []
        while len(belief_goal) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_goal]:
                belief_goal.append(state)

        # Hiển thị danh sách trạng thái kết thúc
        display_goal_states(belief_goal)

        # Tìm kiếm đường đi bằng Simulated Annealing
        paths, visited_states = simulated_annealing(belief_start, belief_goal, hint) 
        if paths:
            display_states(paths, visited_states)  # Truyền cả paths và visited_states
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy đường đi nào.")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        
def start_search_ucs():
    """Hàm chính để bắt đầu tìm kiếm bằng Uniform Cost Search."""
    try:
        # Lấy dấu hiệu từ giao diện
        hint = [[None]*3 for _ in range(3)]
        # Sinh 3 trạng thái ban đầu
        belief_start = []
        while len(belief_start) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_start]:
                belief_start.append(state)

        # Sinh 3 trạng thái đích ngẫu nhiên, thỏa mãn dấu hiệu
        belief_goal = []
        while len(belief_goal) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_goal]:
                belief_goal.append(state)

        # Hiển thị danh sách trạng thái kết thúc
        display_goal_states(belief_goal)

        # Tìm kiếm đường đi bằng Uniform Cost Search
        paths, visited_states = uniform_cost_search(belief_start, belief_goal, hint)
        if paths:
            display_states(paths, visited_states)  # Truyền cả paths và visited_states
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy đường đi nào.")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        
def start_search_stochastic_hill_climbing():
    """Hàm chính để bắt đầu tìm kiếm bằng Stochastic Hill Climbing."""
    try:
        # Lấy dấu hiệu từ giao diện
        hint = [[None]*3 for _ in range(3)]
        # Sinh 3 trạng thái ban đầu
        belief_start = []
        while len(belief_start) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_start]:
                belief_start.append(state)

        # Sinh 3 trạng thái đích ngẫu nhiên, thỏa mãn dấu hiệu
        belief_goal = []
        while len(belief_goal) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_goal]:
                belief_goal.append(state)

        # Hiển thị danh sách trạng thái kết thúc
        display_goal_states(belief_goal)

        # Tìm kiếm đường đi bằng Stochastic Hill Climbing
        paths, visited_states = stochastic_hill_climbing(belief_start, belief_goal, hint)
        if paths:
            display_states(paths, visited_states)  # Truyền cả paths và visited_states
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy đường đi nào.")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        
def start_search_greedy():
    """Hàm chính để bắt đầu tìm kiếm bằng Greedy Search."""
    try:
        # Lấy dấu hiệu từ giao diện
        hint = [[None]*3 for _ in range(3)]
        # Sinh 3 trạng thái ban đầu
        belief_start = []
        while len(belief_start) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_start]:
                belief_start.append(state)

        # Sinh 3 trạng thái đích ngẫu nhiên, thỏa mãn dấu hiệu
        belief_goal = []
        while len(belief_goal) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_goal]:
                belief_goal.append(state)

        # Hiển thị danh sách trạng thái kết thúc
        display_goal_states(belief_goal)

        # Tìm kiếm đường đi bằng Greedy Search
        paths, visited_states = greedy_search(belief_start, belief_goal, hint)
        if paths:
            display_states(paths, visited_states)  # Truyền cả paths và visited_states
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy đường đi nào.")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def start_search_steepest_hill_climbing():
    """Hàm chính để bắt đầu tìm kiếm bằng Steepest Hill Climbing."""
    try:
        # Lấy dấu hiệu từ giao diện
        hint = [[None]*3 for _ in range(3)]
        # Sinh 3 trạng thái ban đầu
        belief_start = []
        while len(belief_start) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_start]:
                belief_start.append(state)

        # Sinh 3 trạng thái đích ngẫu nhiên, thỏa mãn dấu hiệu
        belief_goal = []
        while len(belief_goal) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_goal]:
                belief_goal.append(state)

        # Hiển thị danh sách trạng thái kết thúc
        display_goal_states(belief_goal)

        # Tìm kiếm đường đi bằng Steepest Hill Climbing
        paths, visited_states = steepest_hill_climbing(belief_start, belief_goal, hint)
        if paths:
            display_states(paths, visited_states)  # Truyền cả paths và visited_states
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy đường đi nào.")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        
def start_search_hill_climbing():
    """Hàm chính để bắt đầu tìm kiếm bằng Hill Climbing."""
    try:
        # Lấy dấu hiệu từ giao diện
        hint = [[None]*3 for _ in range(3)]
        # Sinh 3 trạng thái ban đầu
        belief_start = []
        while len(belief_start) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_start]:
                belief_start.append(state)

        # Sinh 3 trạng thái đích ngẫu nhiên, thỏa mãn dấu hiệu
        belief_goal = []
        while len(belief_goal) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_goal]:
                belief_goal.append(state)

        # Hiển thị danh sách trạng thái kết thúc
        display_goal_states(belief_goal)

        # Tìm kiếm đường đi bằng Hill Climbing
        paths, visited_states = hill_climbing(belief_start, belief_goal, hint)
        if paths:
            display_states(paths, visited_states)  # Truyền cả paths và visited_states
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy đường đi nào.")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        
def start_search_and_or():
    """Hàm chính để bắt đầu tìm kiếm bằng AND-OR Search."""
    try:
        hint = [[None]*3 for _ in range(3)]
        belief_start = []
        while len(belief_start) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_start]:
                belief_start.append(state)
        belief_goal = []
        while len(belief_goal) < 3:
            state = generate_random_state(hint)
            if flatten(state) not in [flatten(s) for s in belief_goal]:
                belief_goal.append(state)
        display_goal_states(belief_goal)
        paths, visited_states = and_or_search(belief_start, belief_goal, hint)
        if paths:
            display_states(paths, visited_states)
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy đường đi nào.")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Giao diện chính
def display_logs5():
    global entries
    root = tk.Tk()
    root.title("Niềm tin không có dấu hiệu")
    root.configure(bg="lightblue") 
    
    window_width = 1200
    window_height = 300
    root.geometry(f"{window_width}x{window_height}")
    
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x}+{y}")
    
    
    # Số cột tối đa (lấy số lớn nhất giữa 2 hàng)
    max_col = 7

    # Hàng trên (7 nút)
    tk.Button(root, text="BFS", command=start_search, font=("Arial", 14), bg="lightgreen").grid(row=3, column=0, sticky="nsew")
    tk.Button(root, text="DFS", command=start_search_dfs, font=("Arial", 14), bg="lightgreen").grid(row=3, column=1, sticky="nsew")
    tk.Button(root, text="A*", command=start_search_a_star, font=("Arial", 14), bg="lightgreen").grid(row=3, column=2, sticky="nsew")
    tk.Button(root, text="Beam Search", command=start_search_beam, font=("Arial", 14), bg="lightgreen").grid(row=3, column=3, sticky="nsew")
    tk.Button(root, text="IDA*", command=start_search_idastar, font=("Arial", 14), bg="lightgreen").grid(row=3, column=4, sticky="nsew")
    tk.Button(root, text="IDDFS", command=start_search_iddfs, font=("Arial", 14), bg="lightgreen").grid(row=3, column=5, sticky="nsew")
    tk.Button(root, text="Simulated Annealing", command=start_search_simulated_annealing, font=("Arial", 14), bg="lightgreen").grid(row=3, column=6, sticky="nsew")

    # Hàng dưới (6 nút, bắt đầu từ cột 0, thêm 1 label rỗng ở cuối cho đủ 7 cột)
    tk.Button(root, text="UCS", command=start_search_ucs, font=("Arial", 14), bg="lightgreen").grid(row=4, column=0, sticky="nsew")
    tk.Button(root, text="Stochastic Hill Climbing", command=start_search_stochastic_hill_climbing, font=("Arial", 14), bg="lightgreen").grid(row=4, column=1, sticky="nsew")
    tk.Button(root, text="Greedy Search", command=start_search_greedy, font=("Arial", 14), bg="lightgreen").grid(row=4, column=2, sticky="nsew")
    tk.Button(root, text="Steepest Ascnet Hill Climbing", command=start_search_steepest_hill_climbing, font=("Arial", 14), bg="lightgreen").grid(row=4, column=3, sticky="nsew")
    tk.Button(root, text="Hill Climbing", command=start_search_hill_climbing, font=("Arial", 14), bg="lightgreen").grid(row=4, column=4, sticky="nsew")
    tk.Button(root, text="AND-OR Search", command=start_search_and_or, font=("Arial", 14), bg="lightgreen").grid(row=4, column=5, sticky="nsew")
    tk.Label(root, text="", bg="lightblue").grid(row=4, column=6, sticky="nsew")  # label rỗng cho đủ cột

    # Đặt grid column weight cho đều
    for col in range(max_col):
        root.grid_columnconfigure(col, weight=1)
        
# Chạy giao diện
    root.mainloop()
if __name__ == "__main__":
    display_logs5()