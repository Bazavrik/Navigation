import tkinter as tk
import time

# Размер карты и клетки
ROWS, COLS = 20, 20
CELL_SIZE = 20
neighbr = [(1, 0), (0, 1), (-1, 0), (0, -1)]    #координаты соседних клеток относительно текущей



#авторская карта:
grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 3, 0, 1],
[1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

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
        elif grid[r][c] == 3:
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

grid = [[1 if i == 0 or j == 0 or i == COLS-1 or j == ROWS-1 else 0 for i in range(COLS)] for j in range(ROWS)] #создаём карту
# Создание окна и холста
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


def A_start():
    open = []
    closed = []
    current = []
    parents = {}
    path_length = {}
    
    for i in range(ROWS):                                           #определяем старт и конечную цель
        for j in range(COLS):
            if grid[i][j] == 3:
                start = (i, j)
            if grid[i][j] == 2:
                fin = (i, j)
    current = start
    closed.append(current)
    for i in neighbr:                                               #определяем соседей стартовой точки
        if grid[start[0] + i[0]][start[1] + i[1]] == 0:
            open.append((start[0] + i[0], start[1] + i[1]))
            parents[(start[0] + i[0], start[1] + i[1])] = (start[0], start[1])
            path_length[(start[0] + i[0], start[1] + i[1])] = 1
    for i in open:
        canvas.itemconfig(rectangles[i[0]][i[1]], fill='Blue')
    root.update()
    while open and fin != current:
        f_buffer = {}
        for i in open:
            f_buffer[i] = f_counter(path_length[i], i, fin)
        current = get_key(min(f_buffer.values()), f_buffer)
        closed.append(current)
        open.remove(current)
        for i in neighbr:
            if grid[current[0] + i[0]][current[1] + i[1]] != 1 and (current[0] + i[0], current[1] + i[1]) not in closed and (current[0] + i[0], current[1] + i[1]) not in open:
                open.append((current[0] + i[0], current[1] + i[1]))
                parents[(current[0] + i[0], current[1] + i[1])] = (current[0], current[1])
                path_length[(current[0] + i[0], current[1] + i[1])] = path_length[(current[0], current[1])] + 1
                if (current[0] + i[0], current[1] + i[1]) != fin:
                    canvas.itemconfig(rectangles[current[0] + i[0]][current[1] + i[1]], fill='Blue')
        if current != fin:
            canvas.itemconfig(rectangles[current[0]][current[1]], fill='Gray')
        root.update()
        time.sleep(0.05)
    if current == fin:
        while current != start:
            current = parents[current]
            if current != start and current != fin:
                canvas.itemconfig(rectangles[current[0]][current[1]], fill='Yellow')
        
    root.update()

def empti_map():
    grid = [[1 if i == 0 or j == 0 or i == COLS-1 or j == ROWS-1 else 0 for i in range(COLS)] for j in range(ROWS)] #создаём карту
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


button = tk.Button(root, text="Поехали", command=A_start)
button1 = tk.Button(root, text="Пустая карта", command=empti_map)
button.pack()

# Привязываем обработчик клика
canvas.bind("<Button-1>", swap_cell_lkm)
canvas.bind("<Button-3>", swap_cell_pkm)
root.mainloop()