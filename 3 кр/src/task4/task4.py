from tabulate import tabulate

def input_distance_matrix():
    print("Введите матрицу расстояний между городами построчно, разделяя числа пробелами (5 строк по 5 чисел):")
    cities = ['1', '2', '3', '4', '5']
    matrix = []
    for i in range(5):
        while True:
            try:
                row_input = input(f"Строка {i + 1}: ")
                row = list(map(int, row_input.strip().split()))
                if len(row) != 5:
                    print("Пожалуйста, введите ровно 5 чисел.")
                    continue
                if row[i] != 0:
                    print("Расстояние от города до самого себя должно быть 0.")
                    continue
                matrix.append(row)
                break
            except ValueError:
                print("Пожалуйста, введите целые числа.")
    print("\nМатрица расстояний:")
    headers = [''] + cities
    table = [[cities[i]] + matrix[i] for i in range(5)]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
    return matrix

def display_results(table_data, distance_matrix, offspring, city_indices):
    headers = [
        "№",
        "Родитель (генотип)",
        "Расчет родителя",
        "Значение родителя",
        "Потомок",
        "Расчет потомка",
        "Значение потомка"
    ]

    print("Полный расчет задачи коммивояжера в виде таблицы")
    print("Инициализация и расчет потомков после кроссинговера")
    print("В этой таблице отображается полный процесс — от выбора родительских маршрутов, их значений, получения потомков после кроссинговера и значений маршрутов этих потомков по матрице смежности.\n")
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", stralign='center'))

    # Вывод ответа
    best_offspring = min(offspring, key=lambda route: calculate_route_cost(route, distance_matrix, city_indices)[0])
    best_cost, _ = calculate_route_cost(best_offspring, distance_matrix, city_indices)
    print("\nЛучший найденный маршрут среди потомков:")
    print(f"Маршрут: {' -> '.join(best_offspring)} -> {best_offspring[0]}")
    print(f"Стоимость маршрута: {best_cost}")
import random

def calculate_route_cost(route, distance_matrix, city_indices):
    cost = 0
    detailed_calculation = ""
    num_cities = len(route)
    for i in range(num_cities):
        from_city = route[i]
        to_city = route[(i + 1) % num_cities]
        dist = distance_matrix[city_indices[from_city]][city_indices[to_city]]
        cost += dist
        detailed_calculation += f"{dist}"
        if i < num_cities - 1:
            detailed_calculation += " + "
    detailed_calculation += f" = {cost}"
    return cost, detailed_calculation

def initialize_parents(num_parents, cities):
    parents = []
    generated = set()
    while len(parents) < num_parents:
        parent = cities[:]
        random.shuffle(parent)
        parent_tuple = tuple(parent)
        if parent_tuple not in generated:
            generated.add(parent_tuple)
            parents.append(parent)
    return parents

def advanced_crossover(parent1, parent2):
    """
    Performs an advanced crossover (Order Crossover - OX) between two parents and returns two offspring along with crossover points.
    """
    size = len(parent1)
    cp1, cp2 = sorted(random.sample(range(size), 2))
    
    def ox_crossover(p1, p2, cp1, cp2):
        child = [None]*size
        # Copy the segment from p1 to child
        child[cp1:cp2+1] = p1[cp1:cp2+1]
        # Fill the rest from p2 in order
        p2_idx = (cp2 + 1) % size
        c_idx = (cp2 + 1) % size
        while None in child:
            if p2[p2_idx] not in child:
                child[c_idx] = p2[p2_idx]
                c_idx = (c_idx + 1) % size
            p2_idx = (p2_idx + 1) % size
        return child

    offspring1 = ox_crossover(parent1, parent2, cp1, cp2)
    offspring2 = ox_crossover(parent2, parent1, cp1, cp2)

    return offspring1, offspring2, cp1, cp2

def run_genetic_algorithm(distance_matrix, cities, city_indices):
    num_parents = 4
    parents = initialize_parents(num_parents, cities)

    offspring = []
    crossover_info = []
    for i in range(0, num_parents, 2):
        parent1 = parents[i]
        parent2 = parents[i + 1] if i + 1 < num_parents else parents[0]
        child1, child2, cp1, cp2 = advanced_crossover(parent1, parent2)
        offspring.append(child1)
        offspring.append(child2)
        crossover_info.append((cp1, cp2))

    table_data = []
    for idx in range(num_parents):
        parent = parents[idx]
        child = offspring[idx]
        cp1, cp2 = crossover_info[idx // 2]

        parent_cost, parent_detail = calculate_route_cost(parent, distance_matrix, city_indices)
        child_cost, child_detail = calculate_route_cost(child, distance_matrix, city_indices)

        parent_genotype = ''.join(parent[:cp1]) + '*' + ''.join(parent[cp1:cp2+1]) + '*' + ''.join(parent[cp2+1:])
        child_genotype = ' -> '.join(child) + ' -> ' + child[0]

        table_data.append([
            idx + 1,
            parent_genotype,
            parent_detail,
            f"{parent_cost}",
            child_genotype,
            child_detail,
            f"{child_cost}"
        ])

    display_results(table_data, distance_matrix, offspring, city_indices)

def genetic_algorithm():
    distance_matrix = input_distance_matrix()
    cities = ['1', '2', '3', '4', '5']
    city_indices = {city: idx for idx, city in enumerate(cities)}

    while True:
        run_genetic_algorithm(distance_matrix, cities, city_indices)
        repeat = input("Хотите решить задачу еще раз на тех же входных данных? (+/-): ").strip().lower()
        if repeat != '+':
            break
if __name__ == "__main__":
    genetic_algorithm()