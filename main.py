import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
# Функции генерации выборки случайных чисел из различных распределений
def normal_distribution(n):
    return np.random.normal(0, 1, n) # Нормальное распределение (среднее 0, стандартное отклонение 1)

def cauchy_distribution(n):
    return np.random.standard_cauchy(n) # Распределение Коши

def poisson_distribution(n):
    return np.random.poisson(10, n) # Пуассоновское распределение с параметром λ=10

def uniform_distribution(n):
    return np.random.uniform(-math.sqrt(3), math.sqrt(3), n) # Равномерное распределение в диапазоне [-√3, √3]
# Функция подсчета выбросов
def count_outliers(data):
    Q1 = np.percentile(data, 25) # Вычисляем первый (Q1) и третий (Q3) квартили
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1 # Находим межквартильный размах (IQR)
    lower_bound = Q1 - 1.5 * IQR # Определяем нижнюю и верхнюю границы выбросов
    upper_bound = Q3 + 1.5 * IQR
    return np.sum((data < lower_bound) | (data > upper_bound)) # Возвращаем количество значений, выходящих за эти границы
# Функция построения бокс-плотов
def print_boxplot():
    distributions = [
        ('normal', normal_distribution),
        ('cauchy', cauchy_distribution),
        ('poisson', poisson_distribution),
        ('uniform', uniform_distribution),
    ]
    ns = np.array([20, 100, 1000])
    
    outliers_table = [] # Создаем пустую таблицу
    
    for distribution_name, distribution_f in distributions:
        figure, axes = plt.subplots(1, len(ns), figsize=(15, 5))

        for index, n in enumerate(ns):
            values = distribution_f(n)
            
            if distribution_name == 'cauchy':
                values = values[(values > -10) & (values < 10)]  # Ограничение выбросов для лучшей видимости
            
            sns.boxplot(x=values, ax=axes[index], color='skyblue', medianprops=dict(color='orange'), # Создаем бокс-плот для текущего распределения
                        whiskerprops=dict(color='green'),
                        flierprops=dict(marker='o', markersize=5, markerfacecolor='red'))
            
            axes[index].set_title(f'{distribution_name} (n={n})') # Подписываем графики
            axes[index].set_xlabel('x')
            
            outliers_count = count_outliers(values) # Вычисляем количество выбросов
            outliers_table.append([distribution_name, n, outliers_count]) # Добавляем результат в таблицу

        plt.show()
    
    outliers_df = pd.DataFrame(outliers_table, columns=['Распределение', 'Размер выборки', 'Выбросы']) # Создаем таблицу pandas с результатами
    print(outliers_df)

print_boxplot()
