def generator_a(a, n):
    for _ in range(n):
        yield a
        a = (23 * a + 21563) % 16714589

n, m, a_1 = map(int, input().split())
u_i, v_i = map(int, input().split())

a = generator_a(a_1, n)

log2_array = [0] * (n + 1)
for i in range(2, n):
    log2_array[i] = log2_array[i - 1]
    if (1 << (log2_array[i] + 1)) <= i:
        log2_array[i] += 1

log_n = log2_array[n - 1] + 1

dp = [[0] * log_n for _ in range(n)]

for i in range(n):
    dp[i][0] = next(a)
for k in range(1, log_n):
    for i in range(n):
        right_index = min(i + (1 << (k - 1)), n - 1)
        dp[i][k] = min(dp[i][k - 1], dp[right_index][k - 1])

for i in range(m):
    if i != 0:
        u_i = ((17 * u_i + 751 + r_i + 2 * i) % n) + 1
        v_i = ((13 * v_i + 593 + r_i + 5 * i) % n) + 1
    if u_i > v_i:
        left, right = v_i, u_i
    else:
        left, right = u_i, v_i
    k = log2_array[right - left + 1]
    r_i = min(dp[left - 1][k], dp[right - (1 << k)][k])
    
print(u_i, v_i, r_i)
