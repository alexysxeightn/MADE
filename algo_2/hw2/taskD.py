def gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    d, x, y = gcd(b % a, a)
    return (d, y - (b // a) * x, x)


def main():
    a, b, c = map(int, input().split())
    c = -c
    d, x, y = gcd(a, b)
    if c % d == 0:
        k = c // d
        x, y = k * x, k * y
        print(x, y)
    else:
        print(-1)

if __name__ == '__main__':
    main()
