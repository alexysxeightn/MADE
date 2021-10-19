n = int(input())
a = [*map(int, input().split())]

dp = [1] * n
prev = [-1] * n

for i in range(n):
    for j in range(i):
        if a[j] < a[i] and dp[i] - 1 < dp[j]:
            prev[i] = j
            dp[i] = dp[j] + 1
    
print(max(dp))

way = []

i = dp.index(max(dp))
while i >= 0:
    way.append(a[i])
    i = prev[i]

way = way[::-1]

print(*way)
