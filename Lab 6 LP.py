import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from scipy.optimize import linprog


def create_interface(num_vars, num_constraints):
    # Очистка окна перед созданием нового интерфейса
    for widget in root.winfo_children():
        widget.destroy()

    global coeffs_entries, bounds_entries, ineq_entries, ineq_types_entries, bounds_checkboxes, optimize_button, optimization_goal
    coeffs_entries = [tk.Entry(root, width=10) for _ in range(num_vars)]
    bounds_entries = [[tk.Entry(root, width=5) for _ in range(2)] for _ in range(num_vars)]
    bounds_checkboxes = [[tk.IntVar() for _ in range(2)] for _ in range(num_vars)]
    ineq_entries = [[tk.Entry(root, width=5) for _ in range(num_vars + 1)] for _ in range(num_constraints)]
    ineq_types_entries = [ttk.Combobox(root, values=["≤", "=", "≥"], width=3) for _ in range(num_constraints)]
    optimization_goal = ttk.Combobox(root, values=["Минимизация", "Максимизация"], width=15)

    # Раздел заголовков и описаний
    tk.Label(root, text="Функция цели: введите коэффициенты").grid(row=0, column=1, columnspan=num_vars)
    tk.Label(root, text="Ограничения:").grid(row=num_vars + 2, column=0)
    tk.Label(root, text="Тип").grid(row=num_vars + 2, column=1)
    for j in range(num_vars):
        tk.Label(root, text=f"x{j + 1}").grid(row=num_vars + 3, column=2 + j)
    tk.Label(root, text="Правая сторона").grid(row=num_vars + 3, column=2 + num_vars)

    # Ввод коэффициентов целевой функции и выпадающее меню для выбора цели
    for i, entry in enumerate(coeffs_entries):
        entry.grid(row=1, column=1 + i)
    optimization_goal.grid(row=num_vars + 3, column=0)
    optimization_goal.set("Минимизация")

    # Ввод ограничений и их типов
    for i in range(num_constraints):
        for j in range(num_vars + 1):
            ineq_entries[i][j].grid(row=num_vars + 4 + i, column=2 + j)
        ineq_types_entries[i].grid(row=num_vars + 4 + i, column=1)
        ineq_types_entries[i].set("≤")

    # Ввод и чекбоксы для границ переменных
    for i in range(num_vars):
        tk.Label(root, text=f"x{i + 1}").grid(row=i + 1, column=0)
        coeffs_entries[i].grid(row=i + 1, column=1)
        for j in range(2):
            chk = tk.Checkbutton(root, variable=bounds_checkboxes[i][j])
            chk.grid(row=i + 1, column=5 + j * 2)
            bounds_entries[i][j].grid(row=i + 1, column=6 + j * 2)
            bounds_entries[i][j].config(state='disabled')
            chk.config(command=lambda idx=i, jdx=j: toggle_entry_state(bounds_entries[idx][jdx]))

    # Кнопка для оптимизации, добавляется после создания интерфейса
    optimize_button = tk.Button(root, text="Рассчитать", command=optimize)
    optimize_button.grid(row=50, column=1, columnspan=2)


def toggle_entry_state(entry):
    entry.config(state='normal' if entry.cget('state') == 'disabled' else 'disabled')


def optimize():
    try:
        # Считываем коэффициенты целевой функции
        c = np.array([float(coeff.get()) for coeff in coeffs_entries if coeff.get() != ''])
        # Изменяем знак коэффициентов для максимизации
        if optimization_goal.get() == "Maximize":
            c = -c

        A = []
        b = []
        A_eq = []
        b_eq = []
        for i, row in enumerate(ineq_entries):
            current_row = [float(x.get()) if x.get() != '' else 0 for x in row[:-1]]
            right_side = float(row[-1].get()) if row[-1].get() != '' else 0
            if ineq_types_entries[i].get() == "≥":
                A.append([-x for x in current_row])
                b.append(-right_side)
            elif ineq_types_entries[i].get() == "≤":
                A.append(current_row)
                b.append(right_side)
            else:  # Equality
                A_eq.append(current_row)
                b_eq.append(right_side)

        bounds = []
        for i, bound in enumerate(bounds_entries):
            lower_bound = float(bound[0].get()) if bounds_checkboxes[i][0].get() and bound[0].get() != '' else None
            upper_bound = float(bound[1].get()) if bounds_checkboxes[i][1].get() and bound[1].get() != '' else None
            # Проверяем, что хотя бы одна из границ была введена
            if lower_bound is not None or upper_bound is not None:
                bounds.append((lower_bound, upper_bound))

        res = linprog(c, A_ub=A, b_ub=b, A_eq=A_eq if A_eq else None, b_eq=b_eq if b_eq else None, bounds=bounds if bounds else None, method='highs')
        messagebox.showinfo("Результат оптимизации",
                            f"Оптимальное значение: {res.fun if optimization_goal.get() == 'Minimize' else -res.fun:.2f}\n"
                            f"Статус: {res.message}\n"
                            f"Параметры оптимизации: {', '.join([f'x{i + 1}={val:.2f}' for i, val in enumerate(res.x)])}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")



root = tk.Tk()
root.title("Метод линейного программирования")

# Кнопка для создания интерфейса после ввода параметров
num_vars = tk.IntVar(value=2)
num_constraints = tk.IntVar(value=2)
tk.Label(root, text="Количество переменных:").grid(row=0, column=0)
tk.Entry(root, textvariable=num_vars).grid(row=0, column=1)
tk.Label(root, text="Количество ограничений:").grid(row=1, column=0)
tk.Entry(root, textvariable=num_constraints).grid(row=1, column=1)
tk.Button(root, text="Создать интерфейс", command=lambda: create_interface(num_vars.get(), num_constraints.get())).grid(
    row=2, column=0, columnspan=2)

root.mainloop()
