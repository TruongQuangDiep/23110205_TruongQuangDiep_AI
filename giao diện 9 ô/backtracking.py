import tkinter as tk
import random
# Biến: Các ô trong bảng 3x3
variables = [(i, j) for i in range(3) for j in range(3)]

# Ràng buộc: tất cả giá trị khác nhau + (1,0)=4, (1,1)=5, (1,2)=6
def all_different_constraint(assignment):
    values = list(assignment.values())
    if len(values) != len(set(values)):
        return False
    if (1, 0) in assignment and assignment[(1, 0)] != 4:
        return False
    if (1, 1) in assignment and assignment[(1, 1)] != 5:
        return False
    if (1, 2) in assignment and assignment[(1, 2)] != 6:
        return False
    return True

# Hàm hiển thị ma trận từ assignment
def print_grid(assignment, log_callback):
    grid = [[assignment.get((i, j), 0) for j in range(3)] for i in range(3)]
    for row in grid:    
        log_callback(" ".join(f"{val:>2}" for val in row))
    log_callback("")  # dòng trống

def backtracking(variables, assignment, constraint, log_callback):
    fixed_values = {(1, 0): 4, (1, 1): 5, (1, 2): 6}
    if len(assignment) == len(variables):
        if constraint(assignment):
            log_callback("Tìm được nghiệm hợp lệ:")
            print_grid(assignment, log_callback)
            return assignment
        return None

    var = next(v for v in variables if v not in assignment)
    for value in random.sample(range(9), 9):  # Duyệt ngẫu nhiên từ 0 đến 8
        # Không cho phép gán giá trị cố định vào vị trí khác
        if var not in fixed_values and value in fixed_values.values():
            continue
        # Kiểm tra nếu giá trị đã tồn tại trong bảng (ngoài các giá trị cố định)
        # if value != 0 and value in assignment.values():
        #     continue

        assignment[var] = value
        log_callback(f"Thử gán {var} = {value}")
        print_grid(assignment, log_callback)

        if constraint(assignment):
            result = backtracking(variables, assignment.copy(), constraint, log_callback)
            if result:
                return result
        else:
            log_callback(f"Gán {var} = {value} vi phạm ràng buộc. Quay lui.")

        del assignment[var]

    return None

# Giao diện
def display_logs():
    def log_callback(message):
        text_widget.insert(tk.END, message + "\n")
        text_widget.see(tk.END)

    root = tk.Tk()
    root.title("Backtracking")
    root.configure(bg="lightblue")
    
    window_width = 550
    window_height = 530
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    text_widget = tk.Text(root, wrap=tk.WORD, font=("Courier New", 12), width=50, height=25, bg="lightyellow")
    text_widget.pack(padx=10, pady=10)

    def start_search():
        text_widget.delete(1.0, tk.END)
        log_callback(" Bắt đầu tìm kiếm...\n")
        solution = backtracking(variables, {}, all_different_constraint, log_callback)
        if not solution:
            log_callback("\nKhông tìm thấy nghiệm thỏa mãn.")

    start_button = tk.Button(root, text="Bắt đầu tìm nghiệm", command=start_search, font=("Arial", 14), bg="lightgreen")
    start_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    display_logs()
