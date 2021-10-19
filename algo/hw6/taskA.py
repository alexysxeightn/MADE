n, k = map(int, input().split())
coins = [0] + [*map(int, input().split())] + [0]
dp = [0] * n
max_prev = [-1] * n
way = []

for i in range(1, n):
    index_of_max_coin = i - 1
    if i - k > 0:
        left_j = i - k
    else:
        left_j = 0
    for j in range(left_j, i):
        if dp[index_of_max_coin] < dp[j]:
            index_of_max_coin = j
    dp[i] = dp[index_of_max_coin] + coins[i]
    max_prev[i] = index_of_max_coin

j = n - 1
len_way = 0
while j > 0:
  way.append(max_prev[j] + 1)
  j = max_prev[j]
  len_way += 1

way = way[::-1] + [n]

print(dp[n - 1])
print(len_way)
print(*way)
