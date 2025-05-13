import tkinter as tk

class PuzzleGUI:
    def __init__(self, root, initial_state):
        self.root = root
        self.root.title("9 Ô")
        
        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack()
        
        # Vẽ lưới 3x3
        for i in range(1, 3):
            self.canvas.create_line(i * 100, 0, i * 100, 300, width=2)
            self.canvas.create_line(0, i * 100, 300, i * 100, width=2)
        
        button_frame_top = tk.Frame(root)
        button_frame_top.pack(pady=2)

        button_frame_bottom = tk.Frame(root)
        button_frame_bottom.pack(pady=2)
        
        # Tạo nút "Start"
        self.start_button = tk.Button(
                button_frame_top,
                text="Start", 
                command=self.start_animation, 
                font=("Arial", 16, "bold"),  # Phông chữ lớn hơn
                width=10,  # Chiều rộng nút
                height=2,  # Chiều cao nút
                bg="lightblue",  # Màu nền
                fg="black"  # Màu chữ
            )
        self.start_button.pack(side=tk.LEFT, pady=10)
        
        # Nút "Reset"
        self.reset_button = tk.Button(
                button_frame_top, 
                text="Reset", 
                command=self.reset_to_initial_state, 
                font=("Arial", 16, "bold"),  # Phông chữ lớn hơn
                width=10,  # Chiều rộng nút
                height=2,  # Chiều cao nút
                bg="lightcoral",  # Màu nền
                fg="black"  # Màu chữ
            )
        self.reset_button.pack(pady=10)
        
        # Tạo nút "Pause"
        self.pause_button = tk.Button(
                button_frame_bottom, 
                text="Pause", 
                command=self.pause_animation, 
                font=("Arial", 16, "bold"),
                width=10,
                height=2,
                bg="orange",
                fg="black"
            )
        self.pause_button.pack(side=tk.LEFT, pady=10)
        
        # Tạo nút "Resume"
        self.resume_button = tk.Button(
                button_frame_bottom, 
                text="Resume", 
                command=self.resume_animation, 
                font=("Arial", 16, "bold"),
                width=10,
                height=2,
                bg="lightgreen",
                fg="black"
            )
        self.resume_button.pack(side=tk.LEFT, pady=10)
        
        # Thêm Label để hiển thị bước hiện tại
        self.step_label = tk.Label(
            root, 
            text="Bước hiện tại: 0", 
            font=("Arial", 14),
            bg="white",
            fg="black"
        )
        self.step_label.pack(pady=10)

        self.state_queue = []  # Lưu danh sách trạng thái cần hiển thị
        self.current_step = 0
        self.is_running = False  # Kiểm tra xem animation có đang chạy không
        self.initial_state = initial_state
        
        self.draw_state(initial_state)

    def draw_state(self, state):
    
        self.canvas.delete("all")  # Xóa trạng thái cũ

        # Vẽ lưới và các ô
        for i in range(3):
            for j in range(3):
                x0, y0 = j * 100, i * 100
                x1, y1 = x0 + 100, y0 + 100

                # Màu nền cho ô
                if state[i][j] == 0:  # Ô trống
                    color = "lightgray"
                else:  # Ô có số
                    color = "orange"

                # Vẽ hình chữ nhật với màu nền
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black", width=2)

                # Vẽ số trong ô
                if state[i][j] != 0:  # Không vẽ số cho ô trống
                    self.canvas.create_text(
                        (x0 + x1) // 2, (y0 + y1) // 2,  # Tọa độ trung tâm ô
                        text=str(state[i][j]),
                        font=("Arial", 24, "bold"),  # Phông chữ lớn và đậm
                        fill="darkblue"  # Màu chữ
                    )
                    
    def pause_animation(self):
        """Tạm dừng animation"""
        self.is_running = False

    def resume_animation(self):
        """Tiếp tục animation"""
        if not self.is_running and self.current_step < len(self.state_queue):
            self.is_running = True
            self.animate_states()
                    
    def reset_to_initial_state(self):
        """Đặt lại trạng thái về trạng thái ban đầu"""
        self.is_running = False  # Dừng animation nếu đang chạy
        self.current_step = 0
        self.step_label.config(text="Bước hiện tại: 0")
        self.draw_state(self.initial_state)  # Hiển thị trạng thái ban đầu

    def update_display(self, state_list):
        """ Nhận danh sách trạng thái từ thuật toán """
        self.state_queue = state_list
        self.current_step = 0

    def start_animation(self):
        """ Bắt đầu hiển thị trạng thái khi nhấn nút Start """
        if not self.is_running and self.state_queue:
            self.is_running = True
            self.current_step = 1
            self.animate_states()

    def animate_states(self):
        """Hiển thị từng trạng thái theo thời gian thực"""
        if not self.is_running:
            return  # Dừng animation nếu is_running là False
        if self.current_step < len(self.state_queue):
            self.draw_state(self.state_queue[self.current_step])
            self.step_label.config(text=f"Bước hiện tại: {self.current_step}")
            self.current_step += 1
            self.root.after(1, self.animate_states)  # Hiển thị trạng thái tiếp theo sau 500ms
        else:
            self.is_running = False  # Kết thúc animation

def run_gui(state_list):
    root = tk.Tk()
    initial_state = state_list[0] if state_list else [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    app = PuzzleGUI(root, initial_state)
    app.update_display(state_list)
    window_width = 300
    window_height = 530  # Chiều cao bao gồm cả nút "Start"
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2) - 30
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    root.mainloop()
