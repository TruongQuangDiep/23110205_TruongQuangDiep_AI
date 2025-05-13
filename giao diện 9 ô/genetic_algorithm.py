import random
import os
import tkinter as tk
from tkinter import messagebox

GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Hàm tính độ fitness
def fitness(individual):
    distance = 0
    for i in range(9):
        if individual[i] != 0:
            goal_index = GOAL_STATE.index(individual[i])
            x1, y1 = i % 3, i // 3
            x2, y2 = goal_index % 3, goal_index // 3
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def calculate_fitness_range(generations_data):
    all_fitness = [fitness(individual) for generation in generations_data for individual in generation]
    return min(all_fitness), max(all_fitness)

# Hàm tạo cá thể ngẫu nhiên
def create_individual():
    individual = GOAL_STATE[:]
    while True:
        random.shuffle(individual)
        if fitness(individual) != 0:
            return individual

# Hàm lai ghép hai cá thể
def crossover(parent1, parent2):
    cut = random.randint(1, 7)
    child = parent1[:cut] + [x for x in parent2 if x not in parent1[:cut]]
    return child

# Hàm đột biến cá thể
def mutate(individual):
    i, j = random.sample(range(9), 2)
    individual[i], individual[j] = individual[j], individual[i]
    return individual

# Hàm chọn lọc quần thể
def select(population):
    return sorted(population, key=fitness)

# Hàm in bảng trạng thái của cá thể
def print_board(state):
    return '\n'.join(str(state[i:i+3]) for i in range(0, 9, 3))

# Hàm xóa các file cũ
def delete_old_generation_files():
    for file_name in os.listdir():
        if file_name.startswith("generation") and file_name.endswith(".txt"):
            try:
                os.remove(file_name)
            except Exception as e:
                print(f"Không thể xóa file {file_name}: {e}")

# Hàm lưu quần thể vào file
def save_generation_to_file(generation, population, file_name):
    with open(file_name, "w") as f:
        f.write(f"Gen {generation} - Total individuals: {len(population)}\n")
        for individual in population:
            f.write(print_board(individual) + "\n")
            f.write(f"Best fitness: {fitness(individual)}\n\n")

# Hàm chính thuật toán di truyền
def genetic_algorithm(generations=1000, population_size=40):
    delete_old_generation_files()

    population = [create_individual() for _ in range(population_size)]
    all_generations = []

    for generation in range(generations):
        population = select(population)
        best = population[0]

        best_fitness = fitness(best)
        new_population = [best]

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population, 2)
            child = crossover(parent1, parent2)
            if random.random() < 0.3:
                child = mutate(child)
                
            if fitness(child) <= best_fitness:
                new_population.append(child)

        while len(new_population) < population_size:
            new_population.append(create_individual())

        population = select(new_population)
        all_generations.append(population[:])  # Lưu toàn bộ quần thể

        save_generation_to_file(generation, population, f"generation{generation}.txt")
        print(f"Gen {generation} - fitness: {fitness(best)}")

        if fitness(best) == 0:
            print("\nĐã tìm ra lời giải ở thế hệ", generation)
            print(print_board(best))
            return all_generations  # Trả về toàn bộ dữ liệu thế hệ

    print("Không tìm được lời giải sau", generations, "thế hệ.")
    return all_generations

class PaginationApp:
    def __init__(self, root, generations_data):
        self.root = root
        self.root.title("Thuật Toán Di Truyền - Trực Quan Hóa")
        self.generations_data = generations_data
        self.current_page = 0
        
        # Tạo khung chứa Label "Thế hệ"
        self.header_frame = tk.Frame(root)
        self.header_frame.pack(fill=tk.X)

        # Label "Thế hệ"
        self.generation_label = tk.Label(self.header_frame, text="Thế hệ 1", font=("Arial", 16, "bold"), fg="black")
        self.generation_label.pack(pady=10)

        self.container = tk.Frame(root)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Canvas + Scrollbar
        self.canvas = tk.Canvas(self.container)
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Nút chuyển trang
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.prev_button = tk.Button(self.button_frame, text="Trang trước", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.button_frame, text="Trang tiếp", command=self.next_page)
        self.next_button.pack(side=tk.RIGHT, padx=10)

        self.display_generation(self.current_page)

    def display_generation(self, generation_index):
        # Cập nhật nội dung của Label "Thế hệ"
        self.generation_label.config(text=f"Thế hệ {generation_index}")

        # Đặt con lăn về vị trí trên cùng
        self.canvas.yview_moveto(0)

        # Xóa tất cả các widget cũ trong frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Lấy dữ liệu của thế hệ hiện tại
        generation = self.generations_data[generation_index]
        
        min_fitness, max_fitness = calculate_fitness_range(self.generations_data)
        
        def get_color(fit):
            # Tạo thang màu từ xanh lá cây (tốt nhất) đến đỏ (tệ nhất)
            green = int(150 * (1 - (fit - min_fitness) / (max_fitness - min_fitness + 1e-5))) + 50
            red = int(150 * ((fit - min_fitness) / (max_fitness - min_fitness + 1e-5))) + 50
            return f"#{red:02x}{green:02x}00"

        # Hiển thị từng cá thể trong thế hệ
        for i, individual in enumerate(generation):
            frame = tk.Frame(self.scrollable_frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
            row = i // 6
            col = i % 6
            frame.grid(row=row, column=col, padx=10, pady=10)
            
            fit = fitness(individual)
            color = get_color(fit) 

            # Hiển thị ma trận 3x3
            for r in range(3):
                for c in range(3):
                    val = individual[r * 3 + c]
                    cell = tk.Label(
                        frame,
                        text=str(val) if val != 0 else "",
                        width=4,
                        height=2,
                        bg=color,
                        relief=tk.RIDGE,
                        font=("Arial", 12)
                    )
                    cell.grid(row=r, column=c)

            # Hiển thị fitness bên dưới ma trận
            tk.Label(
                frame,
                text=f"Fitness: {fit}",
                fg="blue",
                font=("Arial", 10)
            ).grid(row=3, column=0, columnspan=3)

        # Cập nhật trạng thái của các nút chuyển trang
        self.update_buttons()

    def update_buttons(self):
        self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_page < len(self.generations_data) - 1 else tk.DISABLED)

    def next_page(self):
        if self.current_page < len(self.generations_data) - 1:
            self.current_page += 1
            self.display_generation(self.current_page)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_generation(self.current_page)

def run_generatic_annealing():
    """Hàm chạy thuật toán Simulated Annealing và hiển thị giao diện"""
    root = tk.Tk()
    root.geometry("1000x700")
    root.withdraw()

    import threading
    def center_window(window):
        window.update_idletasks()  # Cập nhật kích thước cửa sổ
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 50
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def run_and_show_gui():
        all_generations = genetic_algorithm()
        root.deiconify()
        center_window(root)
        app = PaginationApp(root, all_generations)

    thread = threading.Thread(target=run_and_show_gui)
    thread.start()

    root.mainloop()

if __name__ == "__main__":
    run_generatic_annealing()