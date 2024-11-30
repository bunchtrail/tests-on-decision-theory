# Программа для нахождения седловой точки в платежной матрице с выводом всех шагов решения.

def find_saddle_point(matrix, variant):
    print(f"\n--- Поиск седловой точки без использования метода доминирования для Варианта {variant} ---")
    print("Исходная матрица:")
    for row in matrix:
        print(row)
    
    # Находим минимальные элементы в строках (минимумы строк)
    row_mins = [min(row) for row in matrix]
    print(f"Минимальные элементы в строках (минимумы строк): {row_mins}")
    
    # Находим максимальный из минимумов строк (значение максимина)
    max_of_row_mins = max(row_mins)
    print(f"Максимальный из минимумов строк (значение максимина): {max_of_row_mins}")
    
    # Транспонируем матрицу для удобства работы с столбцами
    transposed_matrix = list(zip(*matrix))
    
    # Находим максимальные элементы в столбцах (максимумы столбцов)
    col_maxs = [max(col) for col in transposed_matrix]
    print(f"Максимальные элементы в столбцах (максимумы столбцов): {col_maxs}")
    
    # Находим минимальный из максимумов столбцов (значение минимакса)
    min_of_col_maxs = min(col_maxs)
    print(f"Минимальный из максимумов столбцов (значение минимакса): {min_of_col_maxs}")
    
    # Проверяем наличие седловой точки
    if max_of_row_mins == min_of_col_maxs:
        print(f"Седловая точка найдена! Значение седловой точки: {max_of_row_mins}")
        # Находим позиции седловой точки
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                if value == max_of_row_mins:
                    print(f"Седловая точка находится в строке {i+1}, столбце {j+1}")
    else:
        print("Седловая точка отсутствует.")

def simplify_matrix(matrix, variant):
    print(f"\n--- Упрощение матрицы методом доминирования для Варианта {variant} ---")
    print("Исходная матрица:")
    for row in matrix:
        print(row)
    
    # Копируем матрицу для упрощения
    simplified_matrix = [row[:] for row in matrix]
    rows_to_remove = set()
    cols_to_remove = set()
    
    # Проверяем доминирование строк
    for i in range(len(simplified_matrix)):
        for k in range(len(simplified_matrix)):
            if i != k and k not in rows_to_remove:
                if all(x >= y for x, y in zip(simplified_matrix[i], simplified_matrix[k])):
                    print(f"Строка {i+1} доминирует строку {k+1}. Удаляем строку {k+1}.")
                    rows_to_remove.add(k)
    
    # Удаляем доминируемые строки
    simplified_matrix = [row for idx, row in enumerate(simplified_matrix) if idx not in rows_to_remove]
    
    # Проверяем доминирование столбцов
    transposed_matrix = list(zip(*simplified_matrix))
    for j in range(len(transposed_matrix)):
        for l in range(len(transposed_matrix)):
            if j != l and l not in cols_to_remove:
                if all(x <= y for x, y in zip(transposed_matrix[j], transposed_matrix[l])):
                    print(f"Столбец {j+1} доминируется столбцом {l+1}. Удаляем столбец {j+1}.")
                    cols_to_remove.add(j)
    
    # Удаляем доминируемые столбцы
    simplified_matrix = [
        [value for idx, value in enumerate(row) if idx not in cols_to_remove]
        for row in simplified_matrix
    ]
    
    print("Упрощенная матрица:")
    for row in simplified_matrix:
        print(row)
    
    return simplified_matrix

def find_saddle_point_with_dominance(matrix, variant):
    simplified_matrix = simplify_matrix(matrix, variant)
    find_saddle_point(simplified_matrix, f"{variant} после упрощения")

# Определяем платежные матрицы для двух вариантов
matrix_variant_1 = [
    [3, 3, 4],  # A1
    [2, 3, 2],  # A2
    [2, 4, 5]   # A3
]

matrix_variant_2 = [
    [3, 3, 4],  # A1
    [2, 3, 2],  # A2
    [2, 4, 5]   # A3
]

# Поиск седловой точки без доминирования для Варианта 1
find_saddle_point(matrix_variant_1, 1)

# Поиск седловой точки с использованием метода доминирования для Варианта 1
find_saddle_point_with_dominance(matrix_variant_1, 1)

