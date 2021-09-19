from random import randint
     
n = int(input())
L = list(map(int, input().split()))
     
# Быстрая сортировка
     
def qsort(arr):
    n = len(arr)
    if n <= 1:
        return arr
        
    left_arr, mid_arr, right_arr = [], [], []
    x = arr[randint(0, n - 1)]
        
    for i in arr:
        if i < x:
            left_arr.append(i)
        elif i == x:
            mid_arr.append(i)
        else:
            right_arr.append(i)
     
    return qsort(left_arr) + mid_arr + qsort(right_arr)
        
L = qsort(L)
     
print(*L)
