def prefix_function(s):
    n = len(s)
    p = [0] * n
    for i in range(1, n):
        k = p[i - 1]
        while k > 0 and s[i] != s[k]:
            k = p[k - 1]
        if s[i] == s[k]:
            k += 1
        p[i] = k
    return p
    
def knuth_morris_pratt(P, T, spec_symbol='#'):
    p = prefix_function(P + spec_symbol + T)
    len_P = len(P)
    res = []
    for i in range(len(p)):
        if p[i] == len_P:
            res.append(i - 2 * len_P + 1)
    return res
    
P = input()
T = input()
answer = knuth_morris_pratt(P, T)
print(len(answer))
print(*answer)
