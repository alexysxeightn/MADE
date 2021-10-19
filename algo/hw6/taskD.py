s1, s2 = str(input()), str(input())
n, m = len(s1), len(s2)

dp = [[0] * (m + 1) for _ in range(n + 1)]

for i in range(1, n + 1):
    dp[i][0] = i
for j in range(1, m + 1):
    dp[0][j] = j
    
for i in range(1, n + 1):
    for j in range(1, m + 1):
        dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + int(s1[i - 1] != s2[j - 1]))
        
print(dp[n][m])
