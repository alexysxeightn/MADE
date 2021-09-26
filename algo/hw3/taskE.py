def can_scan(n, x, y, time):
    return time // x + time // y >= n - 1

n, x, y = map(int, input().split())

first_scan = min(x, y)

left, right = 1, (n - 1) * first_scan

while left < right - 1:
    m = (left + right) // 2
    if can_scan(n, x, y, m):
        right = m
    else:
        left = m
        
print(first_scan + right)
