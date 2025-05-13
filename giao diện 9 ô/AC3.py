import tkinter as tk
from collections import deque

# Các biến và miền ban đầu
variables = [(i, j) for i in range(3) for j in range(3)]
domains = {var: list(range(9)) for var in variables}
constraints = []

# Giá trị cố định
fixed_values = {(1, 0): 4, (1, 1): 5, (1, 2): 6}
for var, val in fixed_values.items():
    domains[var] = [val]

# Tạo các ràng buộc tất cả giá trị khác nhau
def different_constraint(x, y):
    return x != y

# Thêm các cặp ràng buộc khác nhau cho mọi cặp biến khác nhau
for i in range(len(variables)):
    for j in range(i + 1, len(variables)):
        xi = variables[i]
        xj = variables[j]
        constraints.append((xi, xj))
        constraints.append((xj, xi))

def ac3(domains, constraints, log_callback):
    queue = deque(constraints)

    while queue:
        (xi, xj) = queue.popleft()
        log_callback(f"Kiểm tra cung: {xi} -> {xj}")
        if revise(domains, xi, xj, log_callback):
            if not domains[xi]:
                log_callback(f"Miền rỗng tại {xi}, không thể giải được.")
                return False
            for xk in [v for v in variables if v != xi and (v, xi) in constraints]:
                queue.append((xk, xi))
    return True

def revise(domains, xi, xj, log_callback):
    revised = False
    for x in domains[xi][:]:
        if not any(different_constraint(x, y) for y in domains[xj]):
            domains[xi].remove(x)
            revised = True
            log_callback(f"Loại bỏ {x} khỏi miền của {xi}")
    return revised

def print_domains(domains, log_callback):
    grid = [[domains.get((i, j), []) for j in range(3)] for i in range(3)]
    for row in grid:
        log_callback(" ".join(f"{str(val):>8}" for val in row))
    log_callback("")

# Giao diện
def display_logs4():
    def log_callback(message):
        text_widget.insert(tk.END, message + "\n")
        text_widget.see(tk.END)

    root = tk.Tk()
    root.title("AC-3 Algorithm")
    root.configure(bg="lightblue")
    
    window_width = 600
    window_height = 550
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    text_widget = tk.Text(root, wrap=tk.WORD, font=("Courier New", 12), width=60, height=25, bg="lightyellow")
    text_widget.pack(padx=10, pady=10)

    def start_ac3():
        text_widget.delete(1.0, tk.END)
        log_callback("Bắt đầu AC-3...\n")

        # Khởi tạo lại miền vì sẽ bị thay đổi
        domain_copy = {var: list(values) for var, values in domains.items()}
        print_domains(domain_copy, log_callback)

        result = ac3(domain_copy, constraints, log_callback)

        if result:
            log_callback("\nAC-3 hoàn tất. Miền hợp lệ:")
            print_domains(domain_copy, log_callback)
        else:
            log_callback("\nKhông tìm được miền hợp lệ.")

    start_button = tk.Button(root, text="Chạy AC-3", command=start_ac3, font=("Arial", 14), bg="lightgreen")
    start_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    display_logs4()
