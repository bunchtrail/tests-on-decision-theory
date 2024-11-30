import numpy as np

def eliminate_dominated_strategies(matrix):
    matrix = np.array(matrix, dtype=float)
    steps = []
    while True:
        rows, cols = matrix.shape
        removed = False
        # Удаление равных строк
        i = 0
        while i < rows - 1:
            j = i + 1
            while j < rows:
                if np.array_equal(matrix[i], matrix[j]):
                    steps.append(f"Удаляем строку {j+1}, так как она равна строке {i+1}")
                    matrix = np.delete(matrix, j, 0)
                    rows -= 1
                    removed = True
                else:
                    j += 1
            i += 1
        # Проверка на доминирование строк
        i = 0
        while i < rows:
            dominated = False
            for j in range(rows):
                if i != j and all(matrix[i] <= matrix[j]) and any(matrix[i] < matrix[j]):
                    steps.append(f"Удаляем строку {i+1}, так как она доминируется строкой {j+1}")
                    matrix = np.delete(matrix, i, 0)
                    rows -= 1
                    removed = True
                    dominated = True
                    break
            if not dominated:
                i += 1
            else:
                break
        if removed:
            continue
        # Удаление равных столбцов
        i = 0
        while i < cols - 1:
            j = i + 1
            while j < cols:
                if np.array_equal(matrix[:, i], matrix[:, j]):
                    steps.append(f"Удаляем столбец {j+1}, так как он равен столбцу {i+1}")
                    matrix = np.delete(matrix, j, 1)
                    cols -= 1
                    removed = True
                else:
                    j += 1
            i += 1
        # Проверка на доминирование столбцов
        i = 0
        while i < cols:
            dominated = False
            for j in range(cols):
                if i != j and all(matrix[:, i] >= matrix[:, j]) and any(matrix[:, i] > matrix[:, j]):
                    steps.append(f"Удаляем столбец {i+1}, так как он доминируется столбцом {j+1}")
                    matrix = np.delete(matrix, i, 1)
                    cols -= 1
                    removed = True
                    dominated = True
                    break
            if not dominated:
                i += 1
            else:
                break
        if not removed:
            break
    for step in steps:
        print(step)
    print("Упрощенная матрица:")
    print(matrix)

matrix1 = [
    [3, 3, 4],  # A1
    [2, 3, 2],  # A2
    [2, 4, 5] 

]
matrix2 = [
    [3,4,7],
    [6, 5, 7],
    [7,5,5]

]
eliminate_dominated_strategies(matrix1)


eliminate_dominated_strategies(matrix2)
