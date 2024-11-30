# -*- coding: utf-8 -*-

# Определяем платежные матрицы
variant1 = [
    [2, 4, 7],
    [6, 5, 4]
]

variant2 = [
    [2, 4, 8],
    [8, 6, 4]
]

def calculate_lower_upper(matrix, variant_number):
    print(f"\nВариант {variant_number}:")

    # Выводим платежную матрицу
    print("Платежная матрица:")
    for row in matrix:
        print(row)

    # 1 шаг: ищем нижнюю цену игры
    print("\n1 шаг: Находим нижнюю цену игры.")
    row_minima = [min(row) for row in matrix]
    print("Минимальные элементы строк:")
    for i, val in enumerate(row_minima):
        print(f"Минимум в строке {i+1}: {val}")
    lower_value = max(row_minima)
    print(f"Нижняя цена игры (максимум среди минимальных элементов строк): {lower_value}")

    # 2 шаг: ищем верхнюю цену игры
    print("\n2 шаг: Находим верхнюю цену игры.")
    # Транспонируем матрицу для удобства
    transposed_matrix = list(zip(*matrix))
    column_maxima = [max(col) for col in transposed_matrix]
    print("Максимальные элементы столбцов:")
    for j, val in enumerate(column_maxima):
        print(f"Максимум в столбце {j+1}: {val}")
    upper_value = min(column_maxima)
    print(f"Верхняя цена игры (минимум среди максимальных элементов столбцов): {upper_value}")

    return lower_value, upper_value

# Для варианта 1
lower1, upper1 = calculate_lower_upper(variant1, 1)

# Для варианта 2
lower2, upper2 = calculate_lower_upper(variant2, 2)
