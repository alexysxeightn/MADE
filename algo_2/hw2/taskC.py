def gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    d, x, y = gcd(b % a, a)
    return (d, y - (b // a) * x, x)


def main():
    N = int(input())
    
    for _ in range(N):
        a, b, n, m = map(int, input().split())
        d, k_1, k_2 = gcd(n, m)
        x = a + (k_1 * (b - a)) % m * n
        print(x)


if __name__ == '__main__':
    main()
