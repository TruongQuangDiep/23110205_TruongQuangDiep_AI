import tkinter as tk
import random
from tkinter import Label, Canvas, PhotoImage, Frame, Scrollbar, Text
from bfs1 import *
from dfs1 import *
from iddfs1 import *
from ucs1 import *
from astar import *
from idastar import *
from SHC import *
from SAHC import *
from StoHC import *
from greedy_search import *
from beam_search import *
from SA import *
from Kiemthu import *
from backtracking import *
from Q_learning import *
from AC3 import *
from niemtin_co_dau_hieu import *
from niemtin_ko_co_dau_hieu import *
from and_or_graph import *
from genetic_algorithm import *
from utils import print_board

# Trạng thái bắt đầu
start = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
x, y = 1, 0  # Vị trí ô trống (0)

def generate_random_state():
    """Tạo trạng thái ngẫu nhiên hợp lệ cho bài toán 8-Puzzle"""
    numbers = list(range(9))  # Các số từ 0 đến 8
    random.shuffle(numbers)  # Xáo trộn ngẫu nhiên
    random_state = [numbers[i:i+3] for i in range(0, 9, 3)]  # Chia thành ma trận 3x3
    return random_state

# Hàm cập nhật giao diện để hiển thị trạng thái
def update_display(text):
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, text + "\n")
    output_text.config(state=tk.DISABLED)
    output_text.yview(tk.END)  # Tự động cuộn xuống cuối
 
# Hàm gọi BFS
def run_bfs():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)  # Xóa nội dung cũ
    output_text.config(state=tk.DISABLED)
    solve_puzzle_bfs(start, x, y, update_display)
    
# Hàm gọi DFS
def run_dfs():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    solve_puzzle_dfs(start, x, y, update_display)

# Hàm gọi IDDFS
def run_iddfs():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    solve_puzzle_iddfs(start, x, y, update_display)
    
def run_ucs():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    solve_puzzle_ucs(start, x, y, update_display)
    
def run_astar():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    solve_puzzle_astar(start, x, y, update_display)
    
def run_idastar():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    solve_puzzle_idastar(start, x, y, update_display)

def run_greedy():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    solve_puzzle_greedy(start, x, y, update_display)
    
def run_hill_climbing():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    solve_puzzle_hill_climbing(start, x, y, update_display)
    
def run_steepest_ascent():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    solve_puzzle_steepest_ascent(start, x, y, update_display)

def run_simulated_annealing():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    solve_puzzle_simulated_annealing(start, x, y, update_display)
    
def run_beam_search():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    solve_puzzle_beam_search(start, x, y, 3, update_display)
    
def run_stochastic_hill_climbing():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    solve_puzzle_stochastic(start, x, y, update_display)
    
def run_and_or_graph():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    solve_puzzle_and_or(start, x, y, update_display)
    
def run_q_learning():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    solve_puzzle_q_learning(start, x, y, update_display)
    
text_widgets = []

root = tk.Tk()
root.title("8 Puzzle Solver")
window_width = 1200
window_height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_x = (screen_width // 2) - (window_width // 2)
position_y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

root.configure(bg="lightblue")

label = Label(root, text="Chọn thuật toán để giải bài toán 8-Puzzle", font=("Arial", 14))
label.configure(bg="lightblue")
label.pack()

output_text = None
frame_main = None
output_scrollbar = None
canvas_frame = None  # Khai báo canvas_frame là None ban đầu
scrollbar = None  # Khai báo scrollbar là None ban đầu

def create_frame_main(root):
    global frame_main
    if frame_main:  # Nếu đã có Frame cũ, xóa nó trước
        frame_main.destroy()
    frame_main = tk.Frame(root)
    frame_main.pack(fill=tk.BOTH, expand=True)

def create_main_text_widget(root, width=50, height=20):
    """Tạo Text widget và Scrollbar bên trong frame_main"""
    global output_text, output_scrollbar,start_cells

    remove_main_text_widget()  # Xóa cái cũ nếu có
    create_frame_main(root)  # Tạo Frame trước
    
    # Tạo khung trống bên phải
    dummy_frame = tk.Frame(frame_main, bg="lightgray", width=600)
    dummy_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
        # Label "Trạng thái đầu"
    label_start = tk.Label(dummy_frame, text="Trạng thái đầu", font=("Arial", 14, "bold"))
    label_start.pack(pady=(10, 0))

    # Frame chứa 9 ô đầu
    start_frame = tk.Frame(dummy_frame, bg="white")
    start_frame.pack(pady=5)
    
    start_cells = []
    for i in range(3):
        for j in range(3):
            value = start[i][j]
            if value == 0:
                color = "lightgray"  # Màu cho ô trống
            else:
                color = "pink"
            btn = tk.Button(start_frame, text=str(value) if value != 0 else "", width=5, height=2, font=("Arial", 16), bg=color)
            btn.grid(row=i, column=j, padx=2, pady=2)
            start_cells.append(btn)

    # Label "Trạng thái cuối"
    label_goal = tk.Label(dummy_frame, text="Trạng thái cuối", font=("Arial", 14, "bold"))
    label_goal.pack(pady=(10, 0))

    # Frame chứa 9 ô cuối
    goal_frame = tk.Frame(dummy_frame, bg="white")
    goal_frame.pack(pady=5)
    
    goal_cells = []
    for i in range(3):
        for j in range(3):
            value = goal[i][j]
            if value == 0:
                color = "lightgray"  # Màu cho ô trống
            else:
                color = "lightgreen"
            btn = tk.Button(goal_frame, text=str(value) if value != 0 else "", width=5, height=2, font=("Arial", 16), bg=color)
            btn.grid(row=i, column=j, padx=2, pady=2)
            goal_cells.append(btn)


    # Tạo Text Widget trước
    output_text = Text(frame_main, wrap=tk.WORD, height=height, width=width)
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    output_text.config(state=tk.DISABLED)
    output_text.config(font=("Arial", 16))

    # Tạo Scrollbar sau khi đã có Text
    output_scrollbar = Scrollbar(frame_main, command=output_text.yview)
    output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output_text.config(yscrollcommand=output_scrollbar.set)
    
def update_start_display(start):
    """Cập nhật giao diện hiển thị trạng thái đầu"""
    global start_cells
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            value = start[i][j]
            start_cells[idx].config(text=str(value) if value != 0 else "")
            if value == 0:
                color = "lightgray"  # Màu cho ô trống
            else:
                color = "pink"  # Màu cho ô có giá trị khác 0
                
            start_cells[idx].config(bg=color)
    
def remove_main_text_widget():
    """Xóa toàn bộ Frame chứa Text và Scrollbar"""
    global output_text, output_scrollbar, frame_main
    if frame_main:
        frame_main.destroy()
        frame_main = None  # Đặt lại biến
    if output_text:
        output_text.destroy()  # Xóa cả Frame, Text và Scrollbar
        output_text = None  # Đặt lại biến
    if output_scrollbar:
        output_scrollbar.destroy()
        output_scrollbar = None

create_main_text_widget(root)
        
def remove_text_widgets():
    """Xóa tất cả Text widget phụ"""
    global text_widgets, canvas_frame, scrollbar
    for widget in text_widgets:
        widget.destroy()
    text_widgets = []  # Đặt lại danh sách
    
    # Xóa canvas_frame nếu tồn tại
    if canvas_frame:
        canvas_frame.destroy()
        canvas_frame = None

    # Xóa scrollbar nếu tồn tại
    if scrollbar:
        scrollbar.destroy()
        scrollbar = None
    
text_widgets_output = []       

def create_text_widget(parent, width=25, height=15, x_offset=0,algorithm_name=""):
    remove_main_text_widget()
    """Tạo Text widget với thanh cuộn và đặt ở góc trái trên cùng"""
    """Tạo Text widget với thanh cuộn và đặt trong parent"""
    frame = tk.Frame(parent)
    frame.grid(row=0, column=x_offset // 210, padx=10, pady=10, sticky="nw")  # Sắp xếp theo cột

    # Tạo Text widget
    text_widget = tk.Text(frame, wrap=tk.WORD, width=width, height=height, font=("Arial", 14))
    text_widget.grid(row=0, column=0, sticky="nw")

    # Thanh cuộn
    scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    text_widget.config(yscrollcommand=scrollbar.set)
    
    # Tạo Label bên dưới Text widget
    label = tk.Label(frame, text=algorithm_name, font=("Arial", 20), bg="lightgray")
    label.grid(row=1, column=0, columnspan=2, pady=5)  # Đặt Label bên dưới Text widget

    text_widgets.append(frame)
    return text_widget

def on_compare_click():
    """Xóa text lớn và tạo nhiều text widget phụ trên 1 hàng"""
    global text_widgets_output, canvas_frame
    remove_main_text_widget()  # Xóa text lớn
    remove_text_widgets()  # Xóa các widget phụ cũ
    
    # Tạo Canvas để chứa các frame
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(canvas_frame)
    scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
    canvas.configure(xscrollcommand=scrollbar.set)

    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    # Tạo một frame bên trong Canvas
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    
    # Danh sách tên thuật toán
    algorithm_names = [
        "BFS", "IDDFS", "UCS", "A*", "Greedy", "IDA*", "Hill Climbing", "Steepest Ascent", "Simulated Annealing"," Beam Search", "Genetic Algorithm"," Stochastic Hill Climbing", "And-Or Graph"
    ]
    
    text_widgets_output = []
    for i, name in enumerate(algorithm_names):  # Số lượng có thể thay đổi
        x_offset = i * 210  # Mỗi Text widget cách nhau 250 pixel
        text_widget = create_text_widget(inner_frame, x_offset=x_offset, algorithm_name=name)
        text_widgets_output.append(text_widget)
        
    # Cập nhật kích thước của Canvas
    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def compare_click():
    solve_puzzle_bfs(start, x, y, lambda text: (text_widgets_output[0].insert(tk.END, text + "\n"),text_widgets_output[0].see(tk.END)))
    solve_puzzle_iddfs(start, x, y, lambda text: (text_widgets_output[1].insert(tk.END, text + "\n"),text_widgets_output[1].see(tk.END)))
    solve_puzzle_ucs(start, x, y, lambda text: (text_widgets_output[2].insert(tk.END, text + "\n"),text_widgets_output[2].see(tk.END)))
    solve_puzzle_astar(start, x, y, lambda text: (text_widgets_output[3].insert(tk.END, text + "\n"),text_widgets_output[3].see(tk.END)))
    solve_puzzle_greedy(start, x, y, lambda text: (text_widgets_output[4].insert(tk.END, text + "\n"),text_widgets_output[4].see(tk.END)))
    solve_puzzle_idastar(start, x, y, lambda text: (text_widgets_output[5].insert(tk.END, text + "\n"),text_widgets_output[5].see(tk.END)))
    solve_puzzle_hill_climbing(start, x, y, lambda text: (text_widgets_output[6].insert(tk.END, text + "\n"),text_widgets_output[6].see(tk.END)))
    solve_puzzle_steepest_ascent(start, x, y, lambda text: (text_widgets_output[7].insert(tk.END, text + "\n"),text_widgets_output[7].see(tk.END)))
    solve_puzzle_simulated_annealing(start, x, y, lambda text: (text_widgets_output[8].insert(tk.END, text + "\n"),text_widgets_output[8].see(tk.END)))
    solve_puzzle_beam_search(start, x, y, 3, lambda text: (text_widgets_output[9].insert(tk.END, text + "\n"),text_widgets_output[9].see(tk.END)))
    solve_puzzle_stochastic(start, x, y, lambda text: (text_widgets_output[10].insert(tk.END, text + "\n"),text_widgets_output[10].see(tk.END)))
    solve_puzzle_and_or(start, x, y, lambda text: (text_widgets_output[11].insert(tk.END, text + "\n"),text_widgets_output[11].see(tk.END)))
    #solve_puzzle_dfs(start, x, y, lambda text: (text_widgets_output[6].insert(tk.END, text + "\n"),text_widgets_output[6].see(tk.END)))
        
def restore_main_text_widget():
    """Xóa các text widget phụ và hiển thị lại text widget chính"""
    remove_text_widgets()

    global output_text, frame_main, output_scrollbar, start_cells, goal_cells
    if frame_main is None:  # Nếu frame_main không tồn tại, tạo lại nó
        create_frame_main(root)
        
    dummy_frame_exists = False
    for widget in frame_main.winfo_children():
        if isinstance(widget, tk.Frame) and widget.cget("bg") == "lightgray":
            dummy_frame_exists = True
            break
        
    if not dummy_frame_exists:
        # Nếu dummy_frame chưa được tạo, vẽ lại các thành phần của nó
        dummy_frame = tk.Frame(frame_main, bg="lightgray", width=600)
        dummy_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Label "Trạng thái đầu"
        label_start = tk.Label(dummy_frame, text="Trạng thái đầu", font=("Arial", 14, "bold"))
        label_start.pack(pady=(10, 0))

        # Frame chứa 9 ô đầu
        start_frame = tk.Frame(dummy_frame, bg="white")
        start_frame.pack(pady=5)

        start_cells = []
        for i in range(3):
            for j in range(3):
                value = start[i][j]
                if value == 0:
                    color = "lightgray"  # Màu cho ô trống
                else:
                    color = "pink"
                btn = tk.Button(start_frame, text=str(value) if value != 0 else "", width=5, height=2, font=("Arial", 16), bg = color)
                btn.grid(row=i, column=j, padx=2, pady=2)
                start_cells.append(btn)

        # Label "Trạng thái cuối"
        label_goal = tk.Label(dummy_frame, text="Trạng thái cuối", font=("Arial", 14, "bold"))
        label_goal.pack(pady=(10, 0))

        # Frame chứa 9 ô cuối
        goal_frame = tk.Frame(dummy_frame, bg="white")
        goal_frame.pack(pady=5)

        goal_cells = []
        for i in range(3):
            for j in range(3):
                value = goal[i][j]
                if value == 0:
                    color = "lightgray"  # Màu cho ô trống
                else:
                    color = "lightgreen"
                btn = tk.Button(goal_frame, text=str(value) if value != 0 else "", width=5, height=2, font=("Arial", 16), bg = color)
                btn.grid(row=i, column=j, padx=2, pady=2)
                goal_cells.append(btn)

    if output_text is None:  # Nếu output_text không tồn tại, tạo lại nó
        output_text = Text(frame_main, wrap=tk.WORD, height=20, width=50)
        output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        output_text.config(state=tk.DISABLED)
        output_text.config(font=("Arial", 16))

    if output_scrollbar is None:  # Nếu output_scrollbar không tồn tại, tạo lại nó
        output_scrollbar = Scrollbar(frame_main, command=output_text.yview)
        output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        output_text.config(yscrollcommand=output_scrollbar.set)

    frame_main.pack(pady=10, fill=tk.BOTH, expand=True)

def update_display(text):
    """Cập nhật hiển thị nội dung thuật toán"""
    restore_main_text_widget()  # Khôi phục text chính trước khi hiển thị nội dung
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, text + "\n")
    output_text.config(state=tk.DISABLED)
    output_text.yview(tk.END)
    
def open_input_window():
    """Mở cửa sổ nhập trạng thái đầu"""
    def confirm_input():
        """Xác nhận trạng thái đầu và cập nhật"""
        global start, x, y
        try:
            # Lấy dữ liệu từ các ô nhập
            new_start = [
                [int(entry_00.get()), int(entry_01.get()), int(entry_02.get())],
                [int(entry_10.get()), int(entry_11.get()), int(entry_12.get())],
                [int(entry_20.get()), int(entry_21.get()), int(entry_22.get())]
            ]
            # Tìm vị trí ô trống (0)
            for i in range(3):
                for j in range(3):
                    if new_start[i][j] == 0:
                        x, y = i, j
                        break
            # Cập nhật trạng thái đầu
            start = new_start
            input_window.destroy()  # Đóng cửa sổ nhập liệu
            update_display("Trạng thái đầu đã được cập nhật!")
        except ValueError:
            update_display("Lỗi: Vui lòng nhập số nguyên hợp lệ!")

    def randomize_input():
        """Tạo trạng thái ngẫu nhiên và điền vào các ô nhập"""
        random_state = generate_random_state()
        entry_00.delete(0, tk.END)
        entry_00.insert(0, random_state[0][0])
        entry_01.delete(0, tk.END)
        entry_01.insert(0, random_state[0][1])
        entry_02.delete(0, tk.END)
        entry_02.insert(0, random_state[0][2])
        entry_10.delete(0, tk.END)
        entry_10.insert(0, random_state[1][0])
        entry_11.delete(0, tk.END)
        entry_11.insert(0, random_state[1][1])
        entry_12.delete(0, tk.END)
        entry_12.insert(0, random_state[1][2])
        entry_20.delete(0, tk.END)
        entry_20.insert(0, random_state[2][0])
        entry_21.delete(0, tk.END)
        entry_21.insert(0, random_state[2][1])
        entry_22.delete(0, tk.END)
        entry_22.insert(0, random_state[2][2])

    # Tạo cửa sổ con
    input_window = tk.Toplevel(root)
    input_window.title("Nhập trạng thái đầu")
    input_window.configure(bg="lightblue")
    input_window.grab_set()  # Chặn tương tác với cửa sổ chính

    # Tính toán vị trí để cửa sổ xuất hiện ở giữa màn hình
    window_width = 450  # Tăng kích thước cửa sổ
    window_height = 400
    screen_width = input_window.winfo_screenwidth()
    screen_height = input_window.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    input_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Tạo Frame để căn giữa nội dung
    content_frame = tk.Frame(input_window, bg="lightblue")
    content_frame.pack(expand=True)  # Sử dụng `expand=True` để căn giữa nội dung

    # Tiêu đề
    title_label = tk.Label(content_frame, text="Nhập trạng thái đầu (0-8)", font=("Arial", 18), bg="lightblue")
    title_label.grid(row=0, column=0, columnspan=3, pady=20)

    # Tạo các ô nhập liệu lớn hơn
    entry_font = ("Arial", 24)  # Font chữ lớn hơn
    entry_width = 4  # Chiều rộng của ô nhập liệu

    entry_00 = tk.Entry(content_frame, width=entry_width, font=entry_font, justify="center")
    entry_00.grid(row=1, column=0, padx=10, pady=10)
    entry_01 = tk.Entry(content_frame, width=entry_width, font=entry_font, justify="center")
    entry_01.grid(row=1, column=1, padx=10, pady=10)
    entry_02 = tk.Entry(content_frame, width=entry_width, font=entry_font, justify="center")
    entry_02.grid(row=1, column=2, padx=10, pady=10)

    entry_10 = tk.Entry(content_frame, width=entry_width, font=entry_font, justify="center")
    entry_10.grid(row=2, column=0, padx=10, pady=10)
    entry_11 = tk.Entry(content_frame, width=entry_width, font=entry_font, justify="center")
    entry_11.grid(row=2, column=1, padx=10, pady=10)
    entry_12 = tk.Entry(content_frame, width=entry_width, font=entry_font, justify="center")
    entry_12.grid(row=2, column=2, padx=10, pady=10)

    entry_20 = tk.Entry(content_frame, width=entry_width, font=entry_font, justify="center")
    entry_20.grid(row=3, column=0, padx=10, pady=10)
    entry_21 = tk.Entry(content_frame, width=entry_width, font=entry_font, justify="center")
    entry_21.grid(row=3, column=1, padx=10, pady=10)
    entry_22 = tk.Entry(content_frame, width=entry_width, font=entry_font, justify="center")
    entry_22.grid(row=3, column=2, padx=10, pady=10)
    
    if start:
        entries = [
            [entry_00, entry_01, entry_02],
            [entry_10, entry_11, entry_12],
            [entry_20, entry_21, entry_22]
        ]
        for i in range(3):
            for j in range(3):
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, start[i][j])

    # Nút xác nhận
    confirm_button = tk.Button(content_frame, text="Xác nhận", font=("Arial", 16), bg="lightgreen", command=lambda: (remove_main_text_widget() ,confirm_input(), update_start_display(start)))
    confirm_button.grid(row=4, column=0, columnspan=3, pady=20)

    # Nút Random
    random_button = tk.Button(content_frame, text="Random", font=("Arial", 16), bg="lightyellow", command=randomize_input)
    random_button.grid(row=5, column=0, columnspan=3, pady=10)
    
# Tạo Canvas để chứa các nút
button_canvas = tk.Canvas(root, bg="lightgray", height=100)
button_canvas.pack(side=tk.BOTTOM, fill=tk.X)

# Thêm Scrollbar ngang
button_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=button_canvas.xview)
button_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

button_canvas.configure(xscrollcommand=button_scrollbar.set)

# Tạo Frame bên trong Canvas để chứa các nút
button_frame = tk.Frame(button_canvas, bg="lightgray")
button_canvas.create_window((0, 0), window=button_frame, anchor="nw")

# Hàm cập nhật kích thước của Canvas
def update_button_canvas():
    button_frame.update_idletasks()
    button_canvas.config(scrollregion=button_canvas.bbox("all"))
    
# Nút nhập trạng thái đầu
btn_input_state = tk.Button(button_frame, text="Nhập trạng thái đầu", bg="lightblue", command=open_input_window)
btn_input_state.pack(side=tk.LEFT, padx=10)

# Nút BFS từ ảnh
img_bfs = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\BFS.png")
btn_bfs = tk.Button(button_frame, image=img_bfs,  command=lambda: (restore_main_text_widget(), run_bfs(), solve_puzzle_bfs_giao_dien(start, x, y)))
btn_bfs.pack(side=tk.LEFT, padx=10)

# Nút DFS từ ảnh
img_dfs = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\DFS.png")
btn_dfs = tk.Button(button_frame, image=img_dfs, command=lambda: (restore_main_text_widget(), run_dfs(), solve_puzzle_dfs_giao_dien(start, x, y)))
btn_dfs.pack(side=tk.LEFT, padx=10)

# Nút IDDFS từ ảnh
img_iddfs = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\IDDFS.png")
btn_iddfs = tk.Button(button_frame, image=img_iddfs, command=lambda: (restore_main_text_widget(), run_iddfs(), solve_puzzle_iddfs_giao_dien(start, x, y)))
btn_iddfs.pack(side=tk.LEFT, padx=10)

# Nút UCS từ ảnh
img_ucs = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\\UCS.png")
btn_ucs = tk.Button(button_frame, image=img_ucs, command=lambda: (restore_main_text_widget(), run_ucs(), solve_puzzle_ucs_giao_dien(start, x, y)))
btn_ucs.pack(side=tk.LEFT, padx=10)

# Nút A* từ ảnh
img_astar = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\A STAR.png")
btn_astar = tk.Button(button_frame, image=img_astar, command=lambda: (restore_main_text_widget(), run_astar(), solve_puzzle_astar_giao_dien(start, x, y)))
btn_astar.pack(side=tk.LEFT, padx=10)

# Nút IDA* từ ảnh
img_idastar = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\IDA STAR.png")
btn_idastar = tk.Button(button_frame, image=img_idastar, command=lambda: (restore_main_text_widget(), run_idastar(), solve_puzzle_idastar_giao_dien(start, x, y)))
btn_idastar.pack(side=tk.LEFT, padx=10)

# Nút Greedy từ ảnh
img_greedy = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\\GREEDY SEARCH.png")
btn_greedy = tk.Button(button_frame, image=img_greedy, command=lambda: (restore_main_text_widget(), run_greedy(), solve_puzzle_greedy_giao_dien(start, x, y)))
btn_greedy.pack(side=tk.LEFT, padx=10)

img_hill_climbing = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\SHC.png")
btn_hill_climbing = tk.Button(button_frame, image=img_hill_climbing, command=lambda: (restore_main_text_widget(), run_hill_climbing(), solve_puzzle_hill_climbing_giao_dien(start, x, y)))
btn_hill_climbing.pack(side=tk.LEFT, padx=10)

img_steepest_ascent = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\SAHC.png")
btn_steepest_ascent = tk.Button(button_frame, image=img_steepest_ascent, command=lambda: (restore_main_text_widget(), run_steepest_ascent(), solve_puzzle_steepest_ascent_giao_dien(start, x, y)))
btn_steepest_ascent.pack(side=tk.LEFT, padx=10)

img_stochastic_hill_climbing = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\StoHC.png")
btn_stochastic_hill_climbing = tk.Button(button_frame, image=img_stochastic_hill_climbing, command=lambda: (restore_main_text_widget(), run_stochastic_hill_climbing(), solve_puzzle_stochastic_giao_dien(start, x, y)))
btn_stochastic_hill_climbing.pack(side=tk.LEFT, padx=10)

img_beam_search = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\Beam Search.png")
btn_beam_search = tk.Button(button_frame, image=img_beam_search, command=lambda: (restore_main_text_widget(), run_beam_search(), solve_puzzle_beam_search_giao_dien(start, x, y, beam_width=3)))
btn_beam_search.pack(side=tk.LEFT, padx=10)

img_simulated_annealing = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\SA.png")
btn_simulated_annealing = tk.Button(button_frame, image=img_simulated_annealing, command=lambda: (restore_main_text_widget(), run_simulated_annealing(), solve_puzzle_simulated_annealing_giao_dien(start, x, y)))
btn_simulated_annealing.pack(side=tk.LEFT, padx=10)

img_genetic_algorithm = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\Genetic Algorithm.png")
btn_genetic_algorithm = tk.Button(button_frame, image=img_genetic_algorithm, command=lambda: (restore_main_text_widget(), run_generatic_annealing()))
btn_genetic_algorithm.pack(side=tk.LEFT, padx=10)

img_Kiemthu = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\Kiemthu.png")
btn_Kiemthu = tk.Button(button_frame, image=img_Kiemthu, command=lambda: (restore_main_text_widget(), display_logs2()))
btn_Kiemthu.pack(side=tk.LEFT, padx=10)

img_backtracking = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\Backtracking.png")
btn_backtracking = tk.Button(button_frame, image=img_backtracking, command=lambda: (restore_main_text_widget(), display_logs()))
btn_backtracking.pack(side=tk.LEFT, padx=10)

img_and_or_graph = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\AND-OR_GRAPH.png")
btn_and_or_graph = tk.Button(button_frame, image=img_and_or_graph, command=lambda: (restore_main_text_widget(), run_and_or_graph(), solve_puzzle_and_or_giao_dien(start, x, y)))
btn_and_or_graph.pack(side=tk.LEFT, padx=10)

img_q_learning = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\Q_Learning.png")
btn_q_learning = tk.Button(button_frame, image=img_q_learning, command=lambda: (restore_main_text_widget(), run_q_learning(), solve_puzzle_q_learning_giao_dien(start, x, y)))
btn_q_learning.pack(side=tk.LEFT, padx=10)

img_AC3 = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\AC3.png")
btn_AC3 = tk.Button(button_frame, image=img_AC3, command=lambda: (restore_main_text_widget(), display_logs4()))
btn_AC3.pack(side=tk.LEFT, padx=10)

img_niemtincodauhieu = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\Niemtincodauhieu.png")
btn_niemtincodauhieu = tk.Button(button_frame, image=img_niemtincodauhieu, command=lambda: (restore_main_text_widget(), display_logs3()))
btn_niemtincodauhieu.pack(side=tk.LEFT, padx=10)

img_niemtinkocodauhieu = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\Niemtinkocodauhieu.png")
btn_niemtinkocodauhieu = tk.Button(button_frame, image=img_niemtinkocodauhieu, command=lambda: (restore_main_text_widget(), display_logs5()))
btn_niemtinkocodauhieu.pack(side=tk.LEFT, padx=10)

# Nút so sánh
img_compare = PhotoImage(file=r"D:\đồ án trí tuệ nhân tạo cá nhân\giao diện 9 ô\giao diện 8 puzzle png\Compare.png")
btn_compare = tk.Button(button_frame, image=img_compare, command=lambda: (on_compare_click(), compare_click()))
btn_compare.pack(side=tk.LEFT, padx=10)

update_button_canvas()

# Chạy giao diện
root.mainloop()
