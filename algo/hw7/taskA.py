def generator_a(a, x, y, n):
    for _ in range(n):
        yield a
        a = (x * a + y) % (1 << 16)
        
def generator_b(b, z, t, m):
    for _ in range(2 * m):
        yield b
        b = (z * b + t) % (1 << 30)

n, x, y, a_0 = map(int, input().split())
m, z, t, b_0 = map(int, input().split())

a, b = generator_a(a_0, x, y, n), generator_b(b_0, z, t, m)

sum_a = [0] * n
sum_a[0] = next(a)
for i in range(1, n):
    sum_a[i] = sum_a[i - 1] + next(a)

result_sum = 0

for b_i in b:
    left, right = b_i % n, next(b) % n
    if left > right:
        left, right = right, left
    if 0 == left:
        result_sum += sum_a[right]
    else:
        result_sum += sum_a[right] - sum_a[left - 1]

print(result_sum)
