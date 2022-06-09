def sieve_of_eratosthenes(N):
    primes = [*range(N)]
    
    for i in range(2, N):
        if primes[i] == i:
            j = i * i
            while j < N:
                primes[j] = i
                j += i

    return primes
    
    
def factorize(a, primes):
    result = []
    while a != 1:
        result.append(primes[a])
        a //= primes[a]
    return sorted(result)
    
    
def main():
    n = int(input())
    a = [0] * n
    max_a = 0
    
    for i in range(n):
        a[i] = int(input())
        if a[i] > max_a:
            max_a = a[i]
            
    primes = sieve_of_eratosthenes(max_a + 1)
        
    for a_i in a:
        print(*factorize(a_i, primes))

if __name__ == '__main__':
    main()
