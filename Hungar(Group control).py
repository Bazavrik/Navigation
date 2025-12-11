import numpy as np



def hungarian_algorithm(cost_matrix):

    # Создаем копию матрицы, чтобы не изменять исходную
    C = cost_matrix.copy().astype(float)
    n, m = C.shape
    if n != m:
        raise ValueError("Для этой реализации ожидается квадратная матрица.")

    # Шаг 1: Редукция строк
    for i in range(n):
        C[i] -= C[i].min()

    # Шаг 2: Редукция столбцов
    for j in range(m):
        C[:, j] -= C[:, j].min()

    print(C)
    
def extract_assignment(marked_matrix):
    """Извлекает назначения из матрицы, где 1 обозначает назначение."""
    n = marked_matrix.shape[0]
    row_ind = []
    col_ind = []
    for i in range(n):
        for j in range(n):
            if marked_matrix[i, j] == 1:
                row_ind.append(i)
                col_ind.append(j)
                break
    return row_ind, col_ind

# --- Применение к вашей матрице ---
cost_matrix = np.array([
    [13, 7, 15, 10],
    [15, 9, 17, 12],
    [13, 15, 15, 10],
    [0, 0, 0, 0]
])

print("Исходная матрица стоимостей:")
print(cost_matrix)
hungarian_algorithm(cost_matrix)