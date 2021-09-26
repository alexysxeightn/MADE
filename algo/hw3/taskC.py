from math import log2, ceil

EPS = 10e-7

def f(x):
    return x ** 0.5 + x ** 2

def bin_search(y, left, right):
    num_iter = ceil(log2((right - left) / EPS))
    
    for i in range(num_iter):
        m = (left + right) / 2
        if f(m) < y:
            left = m
        else:
            right = m
            
    return right

C = float(input())
left, right = 0, C
print(bin_search(C, left, right))
