from scipy.optimize import linprog
import tkinter as tk
from tkinter import messagebox


class LinearProgrammingProblem:
    count = 0

    def __init__(self, c, A, b, bounds):
        self.c = c  # коэффициенты целевой функции
        self.A = A  # матрица коэффициентов ограничений
        self.b = b  # вектор правой стороны ограничений
        self.bounds = bounds  # границы переменных
        self.x = None  # решение задачи
        self.fun = None  # значение целевой функции при оптимальном решении
        LinearProgrammingProblem.count += 1

    def __str__(self):
        return (f"Задача оптимизации с коэффициентами функции цели {self.c}, матрицей ограничений {self.A} и "
                f"границами переменных {self.bounds}.")

    def solve(self):
        res = linprog(self.c, A_ub=self.A, b_ub=self.b, bounds=self.bounds, method='highs')
        if res.success:
            self.x = res.x
            self.fun = res.fun
            return self.x, self.fun
        else:
            return None, None

    def __len__(self):
        return len(self.c)

    def __del__(self):
        LinearProgrammingProblem.count -= 1
        print(f"Экземпляр LinearProgrammingProblem удалён. Оставшиеся экземпляры: {LinearProgrammingProblem.count}")


class LinearProgrammingInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Линейное программирование")

        # Установка шрифта
        self.font = ('Arial', 12)

        # Элементы управления
        tk.Label(root, text="Коэффициенты функции цели (c) [разделённые пробелами]:", font=self.font).grid(row=0, column=0, sticky="w")
        self.c_entry = tk.Entry(root, font=self.font)
        self.c_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(root, text="Матрица ограничений (A) [строки разделённые запятой]:", font=self.font).grid(row=1, column=0, sticky="w")
        self.A_entry = tk.Text(root, height=5, font=self.font)
        self.A_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(root, text="Вектор правых частей (b) [разделённые пробелами]:", font=self.font).grid(row=2, column=0, sticky="w")
        self.b_entry = tk.Entry(root, font=self.font)
        self.b_entry.grid(row=2, column=1, sticky="ew")

        tk.Label(root, text="Границы переменных [(нижняя, верхняя) для каждой переменной, пример: 0 None, 0 None]:", font=self.font).grid(row=3, column=0, sticky="w")
        self.bounds_entry = tk.Entry(root, font=self.font)
        self.bounds_entry.grid(row=3, column=1, sticky="ew")

        # Радиокнопки для выбора максимизации или минимизации
        self.opt_var = tk.IntVar()
        self.opt_var.set(1)  # Установка минимизации по умолчанию
        tk.Radiobutton(root, text="Минимизация", variable=self.opt_var, value=1, font=self.font).grid(row=4, column=0)
        tk.Radiobutton(root, text="Максимизация", variable=self.opt_var, value=-1, font=self.font).grid(row=4, column=1)

        submit_button = tk.Button(root, text="Решить", command=self.solve, font=self.font)
        submit_button.grid(row=5, column=1, sticky="ew")

        self.root.grid_columnconfigure(1, weight=1)

    def solve(self):
        try:
            c = list(map(float, self.c_entry.get().split()))
            if self.opt_var.get() == -1:
                c = [-ci for ci in c]  # Инвертируем коэффициенты для максимизации

            A = [list(map(float, row.split())) for row in self.A_entry.get("1.0", tk.END).strip().split('\n')]
            b = list(map(float, self.b_entry.get().split()))
            bounds = [self.parse_bounds(bound) for bound in self.bounds_entry.get().split(",")]

            problem = LinearProgrammingProblem(c, A, b, bounds)
            x, fun = problem.solve()
            if x is not None:
                result_str = f"Решение: {x}, Значение функции цели: {fun}"
            else:
                result_str = "Не удалось найти решение."
            messagebox.showinfo("Результат", result_str)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def parse_bounds(self, bound_str):
        lower, upper = bound_str.strip().split()
        lower = None if lower.lower() == "none" else float(lower)
        upper = None if upper.lower() == "none" else float(upper)
        return (lower, upper)

if __name__ == "__main__":
    root = tk.Tk()
    app = LinearProgrammingInterface(root)
    root.mainloop()