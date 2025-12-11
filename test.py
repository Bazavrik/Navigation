import tkinter as tk
import numpy as np
import time
from scipy.optimize import linear_sum_assignment

# Размер карты и клетки
ROWS, COLS = 12, 12
CELL_SIZE = 30
neighbr = [(1, 0), (0, 1), (-1, 0), (0, -1)]    #координаты соседних клеток относительно текущей

grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
[1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 1],
[1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1],
[1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
[1, 0, 0, 0, 1, 1, 0, 0, 2, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
[1, 3, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
[1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1],
[1, 0, 0, 3, 1, 0, 0, 0, 0, 3, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

def swap_cell_pkm(event):   #старт/конец
    c = event.x // CELL_SIZE
    r = event.y // CELL_SIZE
    if 0 <= r < ROWS and 0 <= c < COLS:
        if grid[r][c] == 1 or grid[r][c] == 0:
            grid[r][c] = 2
            color = "green"
        elif grid[r][c] == 2:
            grid[r][c] = 3
            color = "red"
        else:
            grid[r][c] = 0
            color = "white"
        # Обновляем цвет на Canvas
        canvas.itemconfig(rectangles[r][c], fill=color)
        print(*grid, sep='\n', end='\n')

def swap_cell_lkm(event):   #препятствие/свободно
    c = event.x // CELL_SIZE
    r = event.y // CELL_SIZE
    if 0 <= r < ROWS and 0 <= c < COLS:
        if grid[r][c] == 0:
            grid[r][c] = 1
            color = "black"
        else:
            grid[r][c] = 0
            color = "white"
        # Обновляем цвет на Canvas
        canvas.itemconfig(rectangles[r][c], fill=color)
        print(*grid, sep='\n', end='\n')

def Manheten(current, fin): #эвристическое растояние
    return abs(current[0] - fin[0]) + abs(current[1] - fin[1])

def f_counter(path_length, current, fin):   #эвристическое расстояние + расстояние от начала движения до этой точки
    return path_length + Manheten(current, fin)

def get_key(val, my_dict):                  #получение ключа по значению
    for key, value in my_dict.items():
        if value == val:
            return key

root = tk.Tk()
root.title("map")

canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, highlightthickness=0)
canvas.pack()

rectangles = []

for r in range(ROWS):
        row_rects = []
        for c in range(COLS):
            x0, y0 = c*CELL_SIZE, r*CELL_SIZE
            x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
            if grid[r][c] == 0:
                rect = canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="gray")
            elif grid[r][c] == 1:
                rect = canvas.create_rectangle(x0, y0, x1, y1, fill="black", outline="gray")
            elif grid[r][c] == 2:
                rect = canvas.create_rectangle(x0, y0, x1, y1, fill="green", outline="gray")
            else:
                rect = canvas.create_rectangle(x0, y0, x1, y1, fill="red", outline="gray")
            row_rects.append(rect)
        rectangles.append(row_rects)


def hung():
    robots = []
    targets = []
    for i in range(ROWS):                                           #определяем старт и конечную цель
        for j in range(COLS):
            if grid[i][j] == 3:
                robots.append((i, j))
            if grid[i][j] == 2:
                targets.append((i, j))
    mat = [[0 for _ in range(max(len(robots), len(targets)))] for _ in range(max(len(robots), len(targets)))]
    for r in range(len(robots)):
        for t in range(len(targets)):
            mat[r][t] = A_start(robots[r], targets[t])
    print(*mat, sep='\n', end='\n\n')
    row_ind, col_ind = linear_sum_assignment(mat)
    print(row_ind, col_ind)


    paths = path_maker(robots, targets, row_ind, col_ind)
    if len(robots) < len(targets):
        for target in targets:
            if target not in [i[-1] for i in paths]:
                fin = target
        for i in range(len(col_ind)):
            if targets[col_ind[i]] == fin:
                mat[len(robots)][col_ind[i]] = 1000
            else:
                mat[len(robots)][col_ind[i]] = mat[row_ind[i]][col_ind[i]] + A_start(targets[col_ind[i]], fin)
        #print(mat[len(robots)].index(min(mat[len(robots)])))       paths[mat[len(robots)].index(min(mat[len(robots)]))]
        new_start = targets[mat[len(robots)].index(min(mat[len(robots)]))]
        new_path = A_start(new_start, fin, True)
        for i in paths:
            if i[-1] == new_start:
                i += new_path[1:]
    print(*mat, sep='\n')
    robots_start(robots)


    walker(paths)

def A_start(start, target, pathfinder=False):
    open = []
    closed = []
    parents = {}
    path_length = {}
    current = start
    closed.append(current)
    for i in neighbr:                                               #определяем соседей стартовой точки
        if grid[start[0] + i[0]][start[1] + i[1]] == 0:
            open.append((start[0] + i[0], start[1] + i[1]))
            parents[(start[0] + i[0], start[1] + i[1])] = (start[0], start[1])
            path_length[(start[0] + i[0], start[1] + i[1])] = 1

    while open and target != current:
        f_buffer = {}
        for i in open:
            f_buffer[i] = f_counter(path_length[i], i, target)
        current = get_key(min(f_buffer.values()), f_buffer)
        closed.append(current)
        open.remove(current)
        for i in neighbr:
            if grid[current[0] + i[0]][current[1] + i[1]] != 1 and (current[0] + i[0], current[1] + i[1]) not in closed and (current[0] + i[0], current[1] + i[1]) not in open:
                open.append((current[0] + i[0], current[1] + i[1]))
                parents[(current[0] + i[0], current[1] + i[1])] = (current[0], current[1])
                path_length[(current[0] + i[0], current[1] + i[1])] = path_length[(current[0], current[1])] + 1
    path = [current]
    walker = current
    while start != walker:
        walker = parents[walker]
        if pathfinder:
            path.append(walker)
    if pathfinder:
        path.reverse()
        return path
    else:
        return path_length[current[0], current[1]]

def robots_start(robots):
    for i in robots:
        x0, y0 = i[1]*CELL_SIZE, i[0]*CELL_SIZE
        x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
        canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="gray")
        canvas.create_oval(x0, y0, x1, y1, fill="red", outline="black")

def path_maker(robots, targets, row_ind, col_ind):
    paths = []
    for row in row_ind:
        if row < len(robots) and col_ind[row] < len(targets):
            path = A_start(robots[row], targets[col_ind[row]], True)
            paths.append(path)
    print(*paths, sep='\n')
    return paths

def walker(paths):
    for _ in range(max([len(i) for i in paths])):
        for path in paths:
            if path:
                step = path[0]
                x0, y0 = step[1]*CELL_SIZE + 1, step[0]*CELL_SIZE + 1
                x1, y1 = x0 + CELL_SIZE - 2, y0 + CELL_SIZE - 2
                canvas.create_oval(x0, y0, x1, y1, fill="red", outline="black")
        root.update()
        time.sleep(0.3)
        for path in paths:
            if path:
                step = path.pop(0)
                if path:
                    x0, y0 = step[1]*CELL_SIZE + 1, step[0]*CELL_SIZE + 1
                    x1, y1 = x0 + CELL_SIZE - 2, y0 + CELL_SIZE - 2
                    canvas.create_oval(x0, y0, x1, y1, fill="white", outline="white")
                    canvas.create_oval(x0+10, y0+10, x1-10, y1-10, fill="black", outline="white")
        root.update()


button = tk.Button(root, text="Венгерский", command=hung)
button.pack()

# Привязываем обработчик клика
canvas.bind("<Button-1>", swap_cell_lkm)
canvas.bind("<Button-3>", swap_cell_pkm)
root.mainloop()