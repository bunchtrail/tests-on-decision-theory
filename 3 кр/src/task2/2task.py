import matplotlib.pyplot as plt
import networkx as nx
from fractions import Fraction
from itertools import count
from tabulate import tabulate

def main1(P):
    print("Используется введенная матрица переходов.")

    # Вычисление P^1
    P1 = P
    print_matrix(P1, "P^1")

    # Вывод исходной матрицы P
    print_matrix(P, "P")

    # Вычисление P^2
    print("\n" + "=" * 50)
    print("Вычисление матрицы P^2:")
    print("=" * 50)
    P2 = multiply_matrices(P, P, 2)

    # Проверка суммы строк P^2
    verify_row_sums(P2, "P^2")

    # Вывод матрицы P^2
    print_matrix(P2, "P^2")

    # Вычисление P^3
    print("\n" + "=" * 50)
    print("Вычисление матрицы P^3:")
    print("=" * 50)
    P3 = multiply_matrices(P2, P, 3)

    # Проверка суммы строк P^3
    verify_row_sums(P3, "P^3")

    # Вывод матрицы P^3
    print_matrix(P3, "P^3")

def get_transition_matrix():
    print("\n=== Ввод матрицы переходов 3x3 ===\n")
    print("Введите каждую строку матрицы по 3 элемента, разделенных пробелом (например, '1/3 0 2/3').\n")
    matrix = []
    for i in range(3):
        while True:
            try:
                row_input = input(f"Введите строку {i+1}: ").strip().split()
                if len(row_input) != 3:
                    raise ValueError("Необходимо ввести ровно 3 элемента.")
                row = [Fraction(elem) for elem in row_input]
                row_sum = sum(row)
                if row_sum != Fraction(1):
                    print(f"Сумма элементов строки {i+1} равна {row_sum}, должна быть 1. Пожалуйста, введите строку заново.\n")
                    continue
                matrix.append(row)
                break
            except ValueError as ve:
                print(f"Ошибка ввода: {ve}. Попробуйте снова.\n")
            except ZeroDivisionError:
                print("Ошибка ввода: знаменатель не может быть нулем. Попробуйте снова.\n")
    return matrix

def validate_matrix(matrix):
    print("\n=== Проверка суммы элементов каждой строки матрицы переходов ===\n")
    valid = True
    for idx, row in enumerate(matrix):
        row_sum = sum(row)
        print(f"Сумма элементов строки {idx+1}: {row_sum}")
        if row_sum != Fraction(1,1):
            print(f"Ошибка: Сумма элементов строки {idx+1} не равна 1.\n")
            valid = False
    if valid:
        print("Все строки корректны. Сумма элементов каждой строки равна единице.\n")
    return valid

def multiply_matrices(A, B, power):
    print(f"\n{'='*50}\nВычисление P^{power} = P^{power-1} x P\n{'='*50}\n")
    size = len(A)
    result = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    print(f"\nВычисление P^{power}:")
    for i in range(size):
        for j in range(size):
            terms = []
            for k in range(size):
                term = A[i][k] * B[k][j]
                terms.append(f"{A[i][k]}*{B[k][j]}")
                result[i][j] += term
            expression = " + ".join(terms)
            print(f"P^{power}[{i+1}][{j+1}] = {expression} = {result[i][j]}")
    return result

def print_matrix(matrix, name):
    print(f"\nМатрица {name}:")
    headers = [""] + [f"a{i+1}" for i in range(len(matrix))]
    table = [[f"a{idx+1}"] + [str(elem) for elem in row] for idx, row in enumerate(matrix)]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

def verify_row_sums(matrix, name):
    print(f"\n=== Проверка суммы элементов строк для {name} ===\n")
    valid = True
    for idx, row in enumerate(matrix):
        row_sum = sum(row)
        status = "(Верно)" if row_sum == Fraction(1,1) else "(Ошибка)"
        print(f"Сумма строки {idx+1}: {row_sum} {status}")
        if row_sum != Fraction(1,1):
            valid = False
    if valid:
        print(f"\nВсе строки матрицы {name} корректны. Сумма элементов каждой строки равна единице.\n")
    else:
        print(f"\nНекоторые строки матрицы {name} имеют суммы, отличные от единицы.\n")

def matrix_to_float(matrix):
    return [[float(entry) for entry in row] for row in matrix]

def plot_state_diagram(P_float, states):
    G = nx.DiGraph()
    for i, state_from in enumerate(states):
        for j, state_to in enumerate(states):
            prob = P_float[i][j]
            if prob > 0:
                G.add_edge(state_from, state_to, weight=f"{prob:.2f}")

    pos = nx.circular_layout(G)
    plt.figure(figsize=(8,6))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', arrowsize=20)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
    plt.title("Диаграмма состояний Марковской цепи")
    plt.show()

def main():
    print("\n=== Программа для анализа цепи Маркова с матрицей переходов 3x3 ===\n")
    states = ['a1', 'a2', 'a3']

    # Шаг 1: Ввод матрицы переходов
    matrix = get_transition_matrix()
    
    # Шаг 2: Проверка корректности матрицы
    if not validate_matrix(matrix):
        print("Программа завершена из-за некорректной матрицы переходов.\n")
        return

    # Шаг 3: Построение и вывод диаграммы состояний
    print_matrix(matrix, "Исходная матрица переходов P")
    P_float = matrix_to_float(matrix)
    plot_state_diagram(P_float, states)

    # Шаг 4: Проверка суммы элементов строк начальной матрицы
    verify_row_sums(matrix, "P")

    # Шаг 5: Пояснение
    print("В данной матрице сумма элементов каждой строки равна единице, что соответствует требованиям цепей Маркова.\n")

    # Вызов main1 с переданной матрицей
    choice = input("Введите '+' чтобы запустить последующий анализ, или любую другую клавишу для выхода: ")
    if choice.strip() == '+':
        print("\nЗапуск дополнительного анализа...\n")
        main1(matrix)
    else:
        print("\nРабота программы завершена.\n")

if __name__ == "__main__":
    main()