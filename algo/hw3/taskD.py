def can_do_clotheslines(clotheslines, k, x):
    count_of_clotheslines = 0
    for len_clothesline in clotheslines:
        count_of_clotheslines += len_clothesline // x
    return count_of_clotheslines >= k

n, k = map(int, input().split())

clotheslines = [int(input()) for _ in range(n)]

left, right = 0, sum(clotheslines) // k + 1

while left < right - 1:
    m = (left + right) // 2
    if can_do_clotheslines(clotheslines, k, m):
        left = m
    else:
        right = m
        
print(left)
