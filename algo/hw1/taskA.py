n = int(input())
L = list(map(int, input().split()))
     
# L.sort()
# print(*L)
# Шутка, шутка)
     
# Сортировка выбором
     
for i in range(n):
    index_of_minimum = i 
    for j in range(i, n):  # Поиск минимума в правом подмассиве
        if L[j] < L[index_of_minimum]:
            index_of_minimum = j
        
    # Меняем i-тый элемент с минимумом правого подмассива местами
    tmp = L[index_of_minimum]
    L[index_of_minimum] = L[i]
    L[i] = tmp
     
print(*L)
