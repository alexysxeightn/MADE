from random import randint

def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)
    
    
def pow(a, n, m):
    result = 1 if n % 2 == 0 else a
    if n <= 1:
        return result % m
    result *= pow(a, n // 2, m) ** 2
    return result % m
    
    
def is_prime(n, num_tests=10):
    if n == 1:
        return False
    if n == 2:
        return True
    
    f, s = 0, n - 1
    while s % 2 == 0:
        s //= 2
        f += 1
    
    for _ in range(num_tests):
        a = randint(2, n-1)
        
        if gcd(a, n) != 1:
            return False
        if pow(a, n-1, n) != 1:
            return False
            
        x = pow(a, s, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(f - 1):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                break
        
    return True


def main():
    n = int(input())
    
    a = [0] * n
    for i in range(n):
        a[i] = int(input())
        
    for a_i in a:
        print('YES' if is_prime(a_i) else 'NO')

main()
