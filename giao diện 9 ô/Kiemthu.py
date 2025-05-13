import random
from itertools import permutations
import tkinter as tk

# Biến: Các ô trong bảng 3x3 (tọa độ hàng, cột)
variables = [(i, j) for i in range(3) for j in range(3)]

# Ràng buộc: Không có ô nào có số trùng nhau và các giá trị tại (1, 0), (1, 1), (1, 2) lần lượt là 4, 5, 6
def all_different_constraint(assignment):
    """
    Kiểm tra ràng buộc:
    1. Tất cả các giá trị trong assignment phải khác nhau.
    2. Các giá trị tại (1, 0), (1, 1), (1, 2) lần lượt là 4, 5, 6.
    """
    values = list(assignment.values())
    # Kiểm tra tất cả các giá trị phải khác nhau
    if len(values) != len(set(values)):
        return False

    # Kiểm tra ràng buộc cụ thể tại các vị trí (1, 0), (1, 1), (1, 2)
    if (1, 0) in assignment and assignment[(1, 0)] != 4:
        return False
    if (1, 1) in assignment and assignment[(1, 1)] != 5:
        return False
    if (1, 2) in assignment and assignment[(1, 2)] != 6:
        return False

    return True

# Tìm kiếm bằng kiểm thử
def generate_and_test(variables, constraint, log_callback):
    """
    Sinh nghiệm hợp lệ đầu tiên cho bài toán CSP bằng thuật toán Generate-and-Test.
    """
    # Danh sách giá trị ban đầu
    values = list(range(9))
    # Trộn ngẫu nhiên danh sách
    random.shuffle(values)
    log_callback(f"Danh sách sau khi trộn ngẫu nhiên: {values}")  # Gửi log đến giao diện
    # Sinh tất cả các hoán vị của [0..8]
    for perm_idx, perm in enumerate(permutations(values), 1):
        # Gán giá trị cho từng biến
        assignment = {var: value for var, value in zip(variables, perm)}
        log_callback(f"Hoán vị {perm_idx}: {perm}")  # Gửi log đến giao diện
        # Kiểm tra ràng buộc
        if constraint(assignment):
            log_callback(f"--> Hoán vị {perm_idx} thỏa mãn ràng buộc: {perm}")  # Gửi log khi thỏa mãn
            return assignment
    return None

# Hiển thị log trên giao diện Tkinter
def display_logs2():
    """
    Tạo giao diện để hiển thị log.
    """
    def log_callback(message):
        text_widget.insert(tk.END, message + "\n")
        text_widget.see(tk.END)  # Tự động cuộn xuống cuối

    # Tạo cửa sổ giao diện
    root = tk.Tk()
    root.title("Thuật toán Kiểm Thử")
    root.configure(bg="lightblue") 
    
    window_width = 700
    window_height = 450
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Widget hiển thị log
    text_widget = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), width=80, height=20, bg="lightyellow")
    text_widget.pack(padx=10, pady=10)

    # Nút bắt đầu tìm nghiệm
    def start_search():
        text_widget.delete(1.0, tk.END)  # Xóa log cũ
        solution = generate_and_test(variables, all_different_constraint, log_callback)
        if solution:
            log_callback("\nNghiệm tìm được:")
            for i in range(3):
                row = [solution[(i, j)] for j in range(3)]
                log_callback(" ".join(map(str, row)))
        else:
            log_callback("\nKhông tìm thấy nghiệm nào thỏa mãn.")

    start_button = tk.Button(root, text="Bắt đầu tìm nghiệm", command=start_search, font=("Arial", 14), bg="lightgreen")
    start_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    display_logs2()