import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

class GameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Стратегическая игра")
        master.geometry("950x800")
        master.configure(bg="#2b2b2b")

        # Изначальные ресурсы
        self.resources = {'wood': 100, 'stone': 50, 'food': 100}
        # Рабочие и их профессии
        self.workers = []
        # Здания и уровни
        self.buildings = {'Lumber Mill': 1, 'Quarry': 1, 'Farm': 0}
        self.upgrades = {'Lumber Mill': 1, 'Quarry': 1, 'Farm': 1}
        # Доступные профессии
        self.professions = ['Lumberjack', 'Miner', 'Farmer']
        # Таймер до следующего расхода еды
        self.time_to_eat = 60
        # Фиксированный расход еды
        self.food_consumption_per_worker = 1
        # Увеличение прибыли фермером
        self.farmer_bonus = 2

        self.create_widgets()
        self.update_ui()

        # Таймер
        self.master.after(1000, self.update_timer)
        # Автоматический сбор ресурсов
        self.master.after(5000, self.automatic_production)
        # Расход еды
        self.master.after(60000, self.consume_food)

    def create_widgets(self):
        # Заголовок
        self.title_label = tk.Label(self.master, text="Стратегическая игра", font=("Arial", 20), fg="white", bg="#2b2b2b")
        self.title_label.pack(pady=10)

        # Таймер до расхода еды
        self.timer_label = tk.Label(self.master, text="До следующего расхода еды: 60 сек", font=("Arial", 14), fg="white", bg="#2b2b2b")
        self.timer_label.pack(pady=5)

        # Ресурсы
        self.resources_frame = tk.Frame(self.master, bg="#3b3b3b")
        self.resources_frame.pack(pady=10, fill='x')
        self.wood_label = tk.Label(self.resources_frame, text="", font=("Arial", 12), fg="white", bg="#3b3b3b")
        self.wood_label.pack(side='left', padx=20)
        self.stone_label = tk.Label(self.resources_frame, text="", font=("Arial", 12), fg="white", bg="#3b3b3b")
        self.stone_label.pack(side='left', padx=20)
        self.food_label = tk.Label(self.resources_frame, text="", font=("Arial", 12), fg="white", bg="#3b3b3b")
        self.food_label.pack(side='left', padx=20)

        # Панель действий
        self.actions_frame = tk.Frame(self.master, bg="#2b2b2b")
        self.actions_frame.pack(pady=10)
        tk.Button(self.actions_frame, text="Собрать ресурсы", command=self.gather_resources, width=20, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.actions_frame, text="Найм рабочих", command=self.hire_worker, width=20, bg="#2196F3", fg="white").grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.actions_frame, text="Улучшить здание", command=self.upgrade_building_dialog, width=20, bg="#FFC107", fg="white").grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.actions_frame, text="Выучить профессию", command=self.learn_profession, width=20, bg="#9C27B0", fg="white").grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.actions_frame, text="Построить ферму", command=self.build_farm, width=20, bg="#8BC34A", fg="white").grid(row=2, column=0, padx=10, pady=10)
        tk.Button(self.actions_frame, text="Назначить работу", command=self.assign_worker, width=20, bg="#009688", fg="white").grid(row=2, column=1, padx=10, pady=10)
        tk.Button(self.actions_frame, text="Выход", command=self.master.quit, width=20, bg="#f44336", fg="white").grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Таблица рабочих
        self.workers_frame = tk.Frame(self.master, bg="#2b2b2b")
        self.workers_frame.pack(pady=10, fill='x')
        tk.Label(self.workers_frame, text="Рабочие:", font=("Arial", 12), fg="white", bg="#2b2b2b").pack(anchor='w', padx=20)

        self.workers_tree = ttk.Treeview(self.workers_frame, columns=("Profession"), show='headings', height=5)
        self.workers_tree.heading("Profession", text="Профессия")
        self.workers_tree.pack(padx=20, fill='x')

        # Информация о зданиях
        self.buildings_info_frame = tk.Frame(self.master, bg="#2b2b2b")
        self.buildings_info_frame.pack(pady=10, fill='both', expand=True)
        tk.Label(self.buildings_info_frame, text="Здания:", font=("Arial", 12), fg="white", bg="#2b2b2b").pack(anchor='w', padx=20)

        self.building_buttons = {}
        for building_name in self.buildings:
            frame = tk.Frame(self.buildings_info_frame, bg="#2b2b2b")
            frame.pack(pady=2, fill='x')
            btn = tk.Button(frame, text="", width=40, bg="#90CAF9", fg="black")
            btn.pack(side='left', padx=5)
            self.building_buttons[building_name] = btn
            self.update_building_button(building_name)

    def update_ui(self):
        # Обновление ресурсов
        self.wood_label.config(text=f"Дерево: {self.resources['wood']}")
        self.stone_label.config(text=f"Камень: {self.resources['stone']}")
        self.food_label.config(text=f"Еда: {self.resources['food']}")
        # Обновление таблицы рабочих
        self.workers_tree.delete(*self.workers_tree.get_children())
        for idx, worker in enumerate(self.workers):
            self.workers_tree.insert('', 'end', iid=idx, values=(worker['profession']))
        # Обновление таймера
        self.timer_label.config(text=f"До следующего расхода еды: {self.time_to_eat} сек")
        # Обновление кнопок зданий
        for building_name in self.buildings:
            self.update_building_button(building_name)
        self.master.after(1000, self.update_timer)

    def gather_resources(self):
        total_wood = 0
        total_stone = 0
        total_food = 0
        for worker in self.workers:
            prof = worker['profession']
            if prof == 'Lumberjack':
                total_wood += 5 * self.upgrades['Lumber Mill']
            elif prof == 'Miner':
                total_stone += 3 * self.upgrades['Quarry']
            elif prof == 'Farmer':
                total_food += 4 * self.upgrades['Farm']
        # Увеличение прибыли фермером
        for worker in self.workers:
            if worker['profession'] == 'Farmer':
                total_food += self.farmer_bonus
        self.resources['wood'] += total_wood
        self.resources['stone'] += total_stone
        self.resources['food'] += total_food
        self.update_ui()

    def hire_worker(self):
        if self.resources['food'] >= 10:
            self.resources['food'] -= 10
            self.workers.append({'profession': 'Без работы'})
            self.update_ui()
        else:
            self.show_message("Недостаточно еды для найма рабочего.")

    def assign_worker(self):
        selected = self.workers_tree.selection()
        if not selected:
            self.show_message("Выберите рабочего для назначения.")
            return
        idx = int(selected[0])
        worker = self.workers[idx]
        profession = simpledialog.askstring("Назначение", "Введите профессию (Lumberjack, Miner, Farmer, Без работы):")
        if profession in self.professions or profession == 'Без работы':
            worker['profession'] = profession
            self.update_ui()
        else:
            self.show_message("Некорректная профессия.")

    def upgrade_building_dialog(self):
        building_name = simpledialog.askstring("Улучшение здания", "Введите название здания (Lumber Mill, Quarry, Farm):")
        if building_name and building_name in self.buildings:
            self.upgrade_building(building_name)
        else:
            self.show_message("Некорректное название здания.")

    def upgrade_building(self, building_name):
        cost = 50 * self.upgrades[building_name]
        if self.resources['stone'] >= cost:
            self.resources['stone'] -= cost
            self.upgrades[building_name] += 1
            self.buildings[building_name] = self.upgrades[building_name]
            self.update_ui()
        else:
            self.show_message("Недостаточно ресурсов для улучшения.")

    def learn_profession(self):
        new_prof = simpledialog.askstring("Новая профессия", "Введите название новой профессии:")
        if new_prof and new_prof not in self.professions:
            self.professions.append(new_prof)
            self.show_message(f"Профессия {new_prof} добавлена!")
        else:
            self.show_message("Профессия уже существует или не введена.")

    def build_farm(self):
        if self.buildings['Farm'] == 0:
            if self.resources['wood'] >= 50 and self.resources['stone'] >= 20:
                self.resources['wood'] -= 50
                self.resources['stone'] -= 20
                self.buildings['Farm'] = 1
                self.upgrades['Farm'] = 1
                self.update_ui()
            else:
                self.show_message("Недостаточно ресурсов для строительства фермы.")
        else:
            self.show_message("У вас уже есть ферма.")

    def update_building_button(self, building_name):
        btn = self.building_buttons[building_name]
        level = self.upgrades[building_name]
        cost = 50 * level
        text = f"{building_name} (Уровень {level})\nСтоимость: {cost} камня"
        btn.config(text=text)

        def on_enter(e):
            tooltip_text = f"{building_name} уровень {level}\nСтоимость улучшения: {cost} камня"
            self.show_tooltip(e.widget, tooltip_text)
        def on_leave(e):
            self.hide_tooltip()

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        def on_click():
            self.upgrade_building(building_name)
        btn.config(command=on_click)

    def show_tooltip(self, widget, text):
        x = widget.winfo_rootx() + 20
        y = widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel()
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=text, bg="yellow", fg="black")
        label.pack()

    def hide_tooltip(self):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

    def update_timer(self):
        if self.time_to_eat > 0:
            self.time_to_eat -= 1
        else:
            self.consume_food()
            self.time_to_eat = 60
        self.timer_label.config(text=f"До следующего расхода еды: {self.time_to_eat} сек")
        self.master.after(1000, self.update_timer)

    def consume_food(self):
        total_workers = len(self.workers)
        total_food_needed = total_workers * self.food_consumption_per_worker
        if self.resources['food'] >= total_food_needed:
            self.resources['food'] -= total_food_needed
        else:
            self.resources['food'] = 0
        self.update_ui()

    def automatic_production(self):
        self.gather_resources()
        self.master.after(5000, self.automatic_production)

    def show_message(self, message):
        messagebox.showinfo("Информация", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()