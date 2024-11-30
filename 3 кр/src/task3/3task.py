import random
from tabulate import tabulate

class Individual:
    def __init__(self, id, genotype):
        self.id = id
        self.genotype = genotype
        self.x = None
        self.fitness = None

def get_function_choice():
    while True:
        choice = input("Введите '1' для использования стандартной функции f(x)=(2*x+3)**2 или '2' для ввода собственной функции: ")
        if choice == '1':
            return lambda x: (2 * x + 3) ** 2
        elif choice == '2':
            func_input = input("Введите функцию от x (например, 'x**2 + 2*x + 1'): ")
            try:
                return lambda x: eval(func_input)
            except Exception as e:
                print(f"Ошибка в функции: {e}. Попробуйте снова.")
        else:
            print("Некорректный ввод. Пожалуйста, введите '1' или '2'.")

def get_range():
    while True:
        try:
            x_min = int(input("Минимальное значение x (например, 1): "))
            x_max = int(input("Максимальное значение x (например, 29): "))
            if x_min >= x_max:
                print("Минимальное значение должно быть меньше максимального. Попробуйте снова.")
                continue
            return x_min, x_max
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите целые числа.")

def get_population_size():
    while True:
        try:
            size = int(input("Введите размер популяции (например, 4): "))
            if size <= 0:
                print("Размер популяции должен быть положительным числом.")
                continue
            return size
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите целое число.")

def get_generation_count():
    while True:
        try:
            count = int(input("Введите количество поколений (например, 30): "))
            if count <= 0:
                print("Количество поколений должно быть положительным числом.")
                continue
            return count
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите целое число.")

def get_elitism_choice():
    while True:
        choice = input("Использовать элитизм? (+/-): ").lower()
        if choice in ['+', '-']:
            return choice == '+'
        else:
            print("Некорректный ввод. Пожалуйста, введите '+' или '-'.")

def initialize_population(size, bit_length):
    population_set = set()
    individuals = []
    id_counter = 1
    while len(individuals) < size:
        genotype = ''.join(random.choice('01') for _ in range(bit_length))
        if genotype in population_set:
            continue  # Обеспечиваем уникальность генотипов
        population_set.add(genotype)
        individual = Individual(id_counter, genotype)
        individuals.append(individual)
        id_counter += 1
    print(f"Начальная популяция: {[ind.genotype for ind in individuals]}")
    return individuals

def genotype_to_phenotype(genotype, x_min, x_max, bit_length):
    max_int = 2 ** bit_length - 1
    int_value = int(genotype, 2)
    x = x_min + (x_max - x_min) * int_value / max_int
    return round(x)

def evaluate_population(individuals, fitness_func, x_min, x_max, bit_length):
    table = []
    for ind in individuals:
        x = genotype_to_phenotype(ind.genotype, x_min, x_max, bit_length)
        ind.x = x
        ind.fitness = fitness_func(x)
        table.append([ind.id, ind.genotype, x, ind.fitness])
    headers = ["№", "Генотип", "Фенотип (x)", "Значение функции"]
    print(f"\nПоколение:")
    print(tabulate(table, headers=headers, tablefmt="fancy_grid", numalign="center", stralign="center"))
    return table

def crossover(parent1_genotype, parent2_genotype):
    # Исключаем первые и последние позиции для точки кроссовера
    if len(parent1_genotype) <= 2:
        point = 1
    else:
        point = random.randint(1, len(parent1_genotype) - 2)
    offspring1 = parent1_genotype[:point] + parent2_genotype[point:]
    offspring2 = parent2_genotype[:point] + parent1_genotype[point:]
    return offspring1, offspring2, point

def mutate(genotype):
    index = random.randint(0, len(genotype) - 1)
    mutated = list(genotype)
    mutated[index] = '1' if genotype[index] == '0' else '0'
    return ''.join(mutated)

def apply_elitism(individuals, population_size):
    # Сортируем особей по убыванию пригодности
    individuals.sort(key=lambda ind: ind.fitness, reverse=True)
    return individuals[:population_size]

def display_crossover(genotype, point):
    return genotype[:point] + '*' + genotype[point:]

def genetic_algorithm():
    # Инициализация счетчика ID
    id_counter = 1

    # Этап 1: Ввод параметров пользователем
    fitness_func = get_function_choice()
    x_min, x_max = get_range()
    population_size = get_population_size()
    generation_count = get_generation_count()
    use_elitism = get_elitism_choice()
    bit_length = 5  # Длина генотипа в битах

    # Этап 2: Инициализация и первое поколение
    individuals = initialize_population(population_size, bit_length)
    id_counter = len(individuals) + 1

    for generation in range(generation_count):
        print(f"\nПоколение {generation + 1}:")
        # Вычисление значений функции для текущей популяции
        evaluation = evaluate_population(individuals, fitness_func, x_min, x_max, bit_length)
        fitness_values = [ind.fitness for ind in individuals]

        # Этап 3: Кроссовер и мутация
        parents = individuals.copy()
        random.shuffle(parents)  # Перемешиваем родителей
        offspring = []
        print("\nКроссовер и мутация:")
        crossover_table = []
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            if i + 1 < len(parents):
                parent2 = parents[i + 1]
            else:
                parent2 = parents[0]  # Если нечетное число, последний родитель спаривается с первым

            child1_genotype, child2_genotype, point = crossover(parent1.genotype, parent2.genotype)
            child1_genotype = mutate(child1_genotype)
            child2_genotype = mutate(child2_genotype)

            # Создаем новых особей
            child1 = Individual(id_counter, child1_genotype)
            id_counter += 1
            child2 = Individual(id_counter, child2_genotype)
            id_counter += 1

            # Вычисляем фенотипы и значения функции
            child1.x = genotype_to_phenotype(child1.genotype, x_min, x_max, bit_length)
            child2.x = genotype_to_phenotype(child2.genotype, x_min, x_max, bit_length)
            child1.fitness = fitness_func(child1.x)
            child2.fitness = fitness_func(child2.x)

            offspring.extend([child1, child2])

            # Добавление звездочки в родительские генотипы
            marked_parent1 = display_crossover(parent1.genotype, point)
            marked_parent2 = display_crossover(parent2.genotype, point)

            crossover_table.append([parent1.id, marked_parent1, child1.id, child1.genotype, child1.fitness])
            crossover_table.append([parent2.id, marked_parent2, child2.id, child2.genotype, child2.fitness])

        headers = ["ID Родителя", "Генотип Родителя", "ID Потомка", "Генотип Потомка", "Значение функции"]
        print(tabulate(crossover_table, headers=headers, tablefmt="fancy_grid", numalign="center", stralign="center"))

        # Этап 4: Элитизм и отбор особей
        combined_population = individuals + offspring
        if use_elitism:
            # Применяем элитизм
            individuals = apply_elitism(combined_population, population_size)
        else:
            # Случайный отбор без повторений
            individuals = random.sample(combined_population, population_size)

    # Этап 5: Финальное поколение и результат
    best_individual = max(individuals, key=lambda ind: ind.fitness)
    print("\nФинальное поколение:")
    print(f"Лучшее значение функции: f({best_individual.x}) = {best_individual.fitness} при генотипе '{best_individual.genotype}'")

if __name__ == "__main__":
    genetic_algorithm()
