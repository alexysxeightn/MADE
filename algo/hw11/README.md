# Графы-2. Кратчайшие пути

## A. Приключения шахматного коня

Ограничение по времени на тест: 2 секунды

Ограничение по памяти на тест: 256 мегабайт

ввод: стандартный ввод

вывод: стандартный вывод

На шахматной доске _N_ × _N_ в клетке (_x1, y1_) стоит голодный шахматный конь. Он хочет попасть в клетку (_x2, y2_),
где растет вкусная шахматная трава. Какое наименьшее количество ходов он должен для этого сделать?

### Входные данные

На вход программы поступает пять чисел: _N, x1, y1, x2, y2 (5 ≤ N ≤ 20, 1 ≤ x1, y1, x2, y2 ≤ N)_. Левая верхняя
клетка доски имеет координаты (1, 1), правая нижняя — (_N, N_).

### Выходные данные

В первой строке выведите единственное число _K_ — количество посещенных клеток. В каждой из следующих _K_ строк
должно быть записано 2 числа — координаты очередной клетки в пути коня.

### Пример

**Входные данные**
```
5
1 1
3 2
```

**Выходные данные**
```
2
1 1
3 2
```

### [Решение](taskA.py)

## B. Кратчайший путь -- 2

Ограничение по времени на тест: 2 секунды

Ограничение по памяти на тест: 256 мегабайт

ввод: стандартный ввод

вывод: стандартный вывод

Дан неориентированный связный взвешенный граф. Найдите кратчайшее расстояние от первой вершины до всех вершин.

### Входные данные

В первой строке входного файла два числа: _n_ и _m_ (2≤ _n_ ≤30000,1≤ _m_ ≤400000), где _n_ — количество вершин
графа, а _m_ — количество ребер.

Следующие _m_ строк содержат описание ребер. Каждое ребро задается стартовой вершиной, конечной вершиной и
весом ребра. Вес каждого ребра — неотрицательное целое число, не превосходящее 10^4.

### Выходные данные

Выведите _n_ чисел — для каждой вершины кратчайшее расстояние до нее.

### Пример

**Входные данные**
```
4 5
1 2 1
1 3 5
2 4 8
3 4 1
2 3 3
```

**Выходные данные**
```
0 1 4 5
```

### [Решение](taskB.py)

## C. Цикл отрицательного веса

Ограничение по времени на тест: 2 секунды

Ограничение по памяти на тест: 256 мегабайт

ввод: стандартный ввод

вывод: стандартный вывод

Дан ориентированный граф. Определите, есть ли в нем цикл отрицательного веса, и если да, то выведите его.

### Входные данные

Во входном файле в первой строке число _N_ (1 ≤ _N_ ≤ 100) — количество вершин графа. В следующих _N_ строках
находится по _N_ чисел — матрица смежности графа. Все веса ребер не превышают по модулю 10 000. Если ребра нет,
то соответствующее число равно 100 000.

### Выходные данные

В первой строке выходного файла выведите «YES», если цикл существует или «NO» в противном случае. При его наличии
выведите во второй строке количество вершин в искомом цикле и в третьей строке — вершины входящие в этот цикл в
порядке обхода.

### Пример

**Входные данные**
```
2
0 -1
-1 0
```

**Выходные данные**
```
YES
2
2 1
```

### [Решение](taskC.py)

## D. Кратчайшие пути

Ограничение по времени на тест: 2 секунды

Ограничение по памяти на тест: 256 мегабайт

ввод: стандартный ввод

вывод: стандартный вывод

Вам дан взвешенный ориентированный граф и вершина _s_ в нём. Для каждой вершины графа _u_ выведите длину 
кратчайшего пути от вершины _s_ до вершины _u_.

### Входные данные

Первая строка входного файла содержит три целых числа _n, m, s_ — количество вершин и ребёр в графе и номер
начальной вершины соответственно (2 ≤ _n_ ≤ 2 000, 1 ≤ _m_ ≤ 5 000).

Следующие _m_ строчек описывают рёбра графа. Каждое ребро задаётся тремя числами — начальной вершиной, конечной
вершиной и весом ребра соответственно. Вес ребра — целое число, не превосходящее 10^15 по абсолютной величине.
В графе могут быть кратные рёбра и петли.

### Выходные данные

Выведите _n_ строчек — для каждой вершины _u_ выведите длину кратчайшего пути из _s_ в _u_. Если не существует
пути между _s_ и _u_, выведите «\*». Если не существует кратчайшего пути между _s_ и _u_, выведите «-».

### Пример

**Входные данные**
```
6 7 1
1 2 10
2 3 5
1 3 100
3 5 7
5 4 10
4 3 -18
6 1 -1
```

**Выходные данные**
```
0
10
-
-
-
*
```

### [Решение](taskD.py)