import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Функция генерации выборки случайных чисел из различных распределений
def generate_samples(distribution, size):
    if distribution == "normal":
        return np.random.normal(0, 1, size) # Нормальное распределение (среднее 0, стандартное отклонение 1)
    elif distribution == "cauchy":
        return np.random.standard_cauchy(size) # Распределение Коши
    elif distribution == "poisson":
        return np.random.poisson(10, size) # Пуассоновское распределение с параметром λ=10
    elif distribution == "uniform":
        return np.random.uniform(-np.sqrt(3), np.sqrt(3), size) # Равномерное распределение в диапазоне [-√3, √3]

# Функция построения гистограммы и плотности распределения
def plot_distribution(distribution, sizes):
    x = np.linspace(-5, 5, 1000)
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))  # Создаем 3 подграфика в одном ряду
    colors = ['blue', 'cyan', 'magenta'] 
    
    for i, size in enumerate(sizes):
        samples = generate_samples(distribution, size)
        if distribution == "cauchy":
            samples = samples[(samples > -10) & (samples < 10)]  # Ограничиваем выбросы
        
        ax = axes[i]  # Выбираем текущий подграфик
        ax.hist(samples, bins=30, density=True, alpha=0.5, color=colors[i], label=f'n={size}')
        
        # Добавление теоретической плотности распределения
        if distribution == "normal":
            ax.plot(x, stats.norm.pdf(x, 0, 1), label="Теоретическая плотность", color='black')
        elif distribution == "cauchy":
            x = np.linspace(-10, 10, 1000)  
            ax.plot(x, stats.cauchy.pdf(x, 0, 1), label="Теоретическая плотность", color='black')
        elif distribution == "poisson":
            x = np.arange(0, 20)
            ax.plot(x, stats.poisson.pmf(x, 10), label="Теоретическая масса вероятностей", color='black')
        elif distribution == "uniform":
            ax.plot(x, stats.uniform.pdf(x, -np.sqrt(3), 2*np.sqrt(3)), label="Теоретическая плотность", color='black')
        
        ax.set_xlabel("значения случайной величины")
        ax.set_ylabel("плотность вероятности" if distribution != "poisson" else "масса вероятности")
        ax.set_title(f'{distribution.capitalize()}, n={size}')
        ax.legend()
    
    plt.tight_layout()  # Уплотняем расположение графиков
    plt.show()

# Функция вычисления статистических характеристик
def compute_statistics(distribution, sizes, repetitions=1000):
    results = {size: {'mean': [], 'median': [], 'quartile': []} for size in sizes} # Создание структуры хранения результатов
    for size in sizes:
        for _ in range(repetitions): # 1000 повторений для оценки характеристик
            sample = generate_samples(distribution, size)
            results[size]['mean'].append(np.mean(sample)) # Среднее значение
            results[size]['median'].append(np.median(sample)) # Медиана
            q1, q3 = np.percentile(sample, [25, 75]) # Квартильные значения (25% и 75%)
            results[size]['quartile'].append((q1 + q3) / 2) # Усредненное значение квартилей
    
    stats_table = {}
    for size in sizes:
        stats_table[size] = {
            'E(mean)': np.mean(results[size]['mean']), # Математическое ожидание среднего
            'E(median)': np.mean(results[size]['median']), # Математическое ожидание медианы
            'E(quartile)': np.mean(results[size]['quartile']), # Математическое ожидание квартильного среднего
            'D(mean)': np.var(results[size]['mean']), # Дисперсия среднего
            'D(median)': np.var(results[size]['median']), # Дисперсия медианы
            'D(quartile)': np.var(results[size]['quartile'])  # Дисперсия квартильного среднего
        }
    return stats_table

# Выполнение лабораторной работы
sizes1 = [10, 50, 1000] # Размеры выборок для построения гистограмм
sizes2 = [10, 100, 1000] # Размеры выборок для вычисления статистик
distributions = ["normal", "cauchy", "poisson", "uniform"]

# Часть 1: Гистограммы и плотности распределения
for dist in distributions:
    plot_distribution(dist, sizes1)

# Часть 2: Вычисление статистических характеристик
for dist in distributions:
    stats_table = compute_statistics(dist, sizes2)
    print(f"\nСтатистики для {dist} распределения:")
    for size, values in stats_table.items():
        print(f"Размер выборки {size}: {values}")
