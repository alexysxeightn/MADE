from math import log, ceil

EPS = 10e-5
NUM_ITER = ceil(-log(EPS, 3 / 2))

def sum_time(Vp, Vf, a, x):
    return ((1 - a) ** 2 + x ** 2) ** 0.5 / Vp + (a ** 2 + (1 - x) ** 2) ** 0.5 / Vf

Vp, Vf = map(int, input().split())
a = float(input())

left, right = 0, 1
for _ in range(NUM_ITER):
    m1 = left + (right - left) / 3
    m2 = right - (right - left) / 3
    if sum_time(Vp, Vf, a, m1) < sum_time(Vp, Vf, a, m2):
        right = m2
    else:
        left = m1
        
print(right)
