INF = 1000 * 300 + 1
COST = 100

def DP(i, j):
    if j > i:
        return INF
    if j <= 0:
        if i >= 1:
            if dinners[i - 1] <= COST:
                result = min(DP(i - 1, j) + dinners[i - 1], DP(i - 1, j + 1))
            else:
                return DP(i - 1, j + 1)
        else:
            return 0
    else:
        if dp[i][j] != -1:
            return dp[i][j]
        if dinners[i - 1] <= COST:
            result = min(DP(i - 1, j) + dinners[i - 1], DP(i - 1, j + 1))
        else:
            result = min(DP(i - 1, j - 1) + dinners[i - 1], DP(i - 1, j + 1))
    dp[i][j] = result
    return result

def WAY(way, i, j):
    if j < i:
        if j <= 0 and i >= 1:
            if dinners[i - 1] <= COST and DP(i, j) != DP(i - 1, j + 1):
                WAY(way, i - 1, j)
            else:
                way.append(i)
                WAY(way, i - 1, j + 1)
        else:
            if DP(i, j) == DP(i - 1, j + 1):
                way.append(i)
                WAY(way, i - 1, j + 1)
            elif dinners[i - 1] <= COST:
                WAY(way, i - 1, j)
            else:
                WAY(way, i - 1, j - 1)

n = int(input())
dinners = [int(input()) for _ in range(n)]

dp = [[-1] * (n + 2) for _ in range(n + 1)]
way = []
answer = INF

for i in range(n + 1):
    if answer >= DP(n, i):
        answer = DP(n, i)
        k1 = i

WAY(way, n, k1)

k2 = len(way)

print(answer)
print(k1, k2)
print(*way[::-1], sep = '\n')
