from sys import stdin # Таки заставили перейти на темную сторону

def lower_bound(array, n, x):
    left, right = -1, n
    while left < right - 1:
        m = (left + right) // 2
        if x <= array[m]:
            right = m
        else:
            left = m
    return right

n = int(input())
array = [*map(int, stdin.readline().split())]

array.sort()

answer = []

k = int(input())
for _ in range(k):
    l, r = map(int, stdin.readline().split())
    answer.append(lower_bound(array, n, r + 1) - lower_bound(array, n, l))

print(*answer)
