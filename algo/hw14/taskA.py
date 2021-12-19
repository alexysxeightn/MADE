p = 31
M = 10 ** 9 + 7

def chr_to_num(c):
    return ord(c) - ord('a') + 1

def init_hash_and_pow_p(s, p, M):
    n = len(s)
    hash, pow_p = [0] * n, [0] * n
    hash[0], pow_p[0] = chr_to_num(s[0]), 1
    for i in range(1, n):
        pow_p[i] = (pow_p[i - 1] * p) % M
        hash[i] = (hash[i - 1] * p + chr_to_num(s[i])) % M
    return hash, pow_p

def get_hash(left, right, hash, pow_p, M):
    if left:
        return (hash[right] - (hash[left - 1] * pow_p[right - left + 1]) % M) % M
    return hash[right]

def strings_are_equal(l1, r1, l2, r2, hash, pow_p, M):
    return r1 - l1 == r2 - l2 and get_hash(l1, r1, hash, pow_p, M) == get_hash(l2, r2, hash, pow_p, M)
    
s = input()
m = int(input())
hash, pow_p = init_hash_and_pow_p(s, p, M)
for _ in range(m):
    a, b, c, d = map(lambda x: int(x) - 1, input().split())
    print('Yes' if strings_are_equal(a, b, c, d, hash, pow_p, M) else 'No')
