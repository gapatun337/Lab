import numpy as np
from scipy.optimize import curve_fit

def fit_curve(x, y, function_type):
    try:
        if function_type == 'linear':
            func = lambda x, a0, a1: a0 + a1*x
        elif function_type == 'quadratic':
            func = lambda x, a0, a1, a2: a0 + a1*x + a2*x**2
        # Добавьте другие типы функций по необходимости

        params, covariance = curve_fit(func, x, y)
        return params
    except Exception as e:
        raise ValueError(f"Ошибка при расчете коэффициентов: {e}")

def predict_value(x, params, function_type):
    try:
        if function_type == 'linear':
            func = lambda x, a0, a1: a0 + a1*x
        elif function_type == 'quadratic':
            func = lambda x, a0, a1, a2: a0 + a1*x + a2*x**2
        # Добавьте другие типы функций по необходимости

        return func(x, *params)
    except Exception as e:
        raise ValueError(f"Ошибка при прогнозе значения: {e}")