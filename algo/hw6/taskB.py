n, m = map(int, input().split())
coins = [[*map(int, input().split())] for _ in range(n)]

MAX_ABS_COINS = 10

dp = [[0] * (m + 1) for _ in range(n + 1)]
for i in range(n + 1):
    dp[i][0] = -MAX_ABS_COINS * (n + m) - 1
for j in range(m + 1):
    dp[0][j] = -MAX_ABS_COINS * (n + m) - 1
    
for i in range(1, n + 1):
    for j in range(1, m + 1):
        if i == 1 and j == 1:
            dp[i][j] = coins[0][0]
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]) + coins[i - 1][j - 1]

way = []
i, j = n, m
while i != 1 or j != 1:
    if dp[i][j - 1] > dp[i - 1][j]:
        j -= 1
        way.append('R')
    else:
        i -= 1
        way.append('D')

way = ''.join(way[::-1])

print(dp[n][m])
print(way)
