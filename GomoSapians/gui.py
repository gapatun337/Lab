import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from calculator import fit_curve, predict_value

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("МНК Аппроксимация")

        self.tree = ttk.Treeview(root, columns=('X', 'Y'), show='headings')
        self.tree.heading('X', text='X')
        self.tree.heading('Y', text='Y')
        self.tree.grid(row=0, column=0, padx=10, pady=10)

        ttk.Button(root, text="Добавить точку", command=self.add_point).grid(row=1, column=0, pady=5)
        ttk.Button(root, text="Удалить выделенную точку", command=self.delete_selected_point).grid(row=2, column=0, pady=5)

        ttk.Label(root, text="Выберите функцию аппроксимации:").grid(row=3, column=0, sticky="w")
        self.function_var = tk.StringVar()
        functions = ['linear', 'quadratic']  # Добавьте другие типы функций по необходимости
        function_dropdown = ttk.Combobox(root, values=functions, textvariable=self.function_var)
        function_dropdown.grid(row=3, column=0, pady=5)
        function_dropdown.current(0)

        ttk.Button(root, text="Рассчитать коэффициенты", command=self.calculate_coefficients).grid(row=4, column=0, pady=10)

        self.plot_frame = ttk.Frame(root)
        self.plot_frame.grid(row=0, column=1, rowspan=5, padx=10, pady=10)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack()

        # Виджеты для отображения коэффициентов
        ttk.Label(root, text="Коэффициенты:").grid(row=5, column=0, sticky="w")
        self.coefficient_labels = []
        for i in range(3):  # В зависимости от типа функции измените количество коэффициентов
            label = ttk.Label(root, text=f"a{i}:")
            label.grid(row=i+6, column=0, sticky="w")
            self.coefficient_labels.append(label)

    def add_point(self):
        x = tk.simpledialog.askfloat("Добавление точки", "Введите значение X:")
        y = tk.simpledialog.askfloat("Добавление точки", "Введите значение Y:")

        if x is not None and y is not None:
            self.tree.insert("", tk.END, values=(x, y))

    def delete_selected_point(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)

    def calculate_coefficients(self):
        try:
            x_values = np.array([float(self.tree.item(item, 'values')[0]) for item in self.tree.get_children()])
            y_values = np.array([float(self.tree.item(item, 'values')[1]) for item in self.tree.get_children()])

            function_type = self.function_var.get()
            self.coefficients = fit_curve(x_values, y_values, function_type)

            # Очистим предыдущие значения коэффициентов
            for label in self.coefficient_labels:
                label.config(text="")

            # Выведем новые значения коэффициентов
            for i, coefficient in enumerate(self.coefficients):
                self.coefficient_labels[i].config(text=f"a{i}: {coefficient}")

            self.ax.clear()
            self.ax.scatter(x_values, y_values, label='Исходные данные', marker='o')

            x_range = np.linspace(min(x_values), max(x_values), 100)
            self.ax.plot(x_range, predict_value(x_range, self.coefficients, function_type), label='Аппроксимация', linestyle='-', color='red')

            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.legend()
            self.ax.grid(True)

            self.canvas.draw()

        except ValueError as e:
            tk.messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()