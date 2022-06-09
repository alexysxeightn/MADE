def gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    d, x, y = gcd(b % a, a)
    return (d, y - (b // a) * x, x)


def modular_multiplicative_inverse(a, n):
    d, x, y = gcd(a, n)
    return (x + n) % n


def factorization(n):
    for i in range(2, n):
        if n % i == 0:
            return i, n // i


def pow(a, n, m):
    result = 1 if n % 2 == 0 else a
    if n <= 1:
        return result % m
    result *= pow(a, n // 2, m) ** 2
    return result % m


def main():
    n, e, C = int(input()), int(input()), int(input())
    
    p, q = factorization(n)
    phi_n = (p - 1) * (q - 1)
    d = modular_multiplicative_inverse(e, phi_n)
    
    print(pow(C, d, n))
    
    
if __name__ == '__main__':
    main()
