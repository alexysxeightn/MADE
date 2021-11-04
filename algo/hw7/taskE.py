from functools import cmp_to_key

INF = (1 << 31) - 1
LOG2_MAX_N = 17

class query: # used as struct from c++
    def __init__(self, l, r, x, ind):
        self.l = l
        self.r = r
        self.x = x
        self.ind = ind

# dsu - disjoint set union
def get(dsu, v):
    if dsu[v] == v:
        return v
    dsu[v] = get(dsu, dsu[v])
    return dsu[v]
    
def compare(a, b):
    if (a.x > b.x) or ((a.x == b.x) and (a.ind < b.ind)):
        return -1
    return 1

f = open('rmq.in', 'r')
g = open('rmq.out', 'w')

n, q = map(int, f.readline().split())

querys = [0] * q

for i in range(q):
    l, r, x = map(int, f.readline().split())
    querys[i] = query(l - 1, r - 1, x, i)

querys = sorted(querys, key = cmp_to_key(compare))

dsu = [i for i in range(n + 1)]
answer = [INF] * n
log2 = [0] * (n + 1)

if n > 1:
    log2[2] = 1
    
for i in range(3, n + 1):
    if (i - 1) & i:
        log2[i] = log2[i - 1]
    else:
        log2[i] = log2[i - 1] + 1

dp = [[0] * LOG2_MAX_N for _ in range(n)]

for i in range(q):
    l, r, x = querys[i].l, querys[i].r, querys[i].x
    try:
        j = get(dsu, l)
        while j <= r:
            dsu[j] = j + 1
            answer[j] = x
            j = get(dsu, j)
    except:
        pass

for i in range(n):
    dp[i][0] = answer[i]

for j in range(1, LOG2_MAX_N):
    for i in range(n):
        if (i + (1 << (j - 1)) < n):
            dp[i][j] = min(dp[i][j - 1], dp[i + (1 << (j - 1))][j - 1])
        else:
            dp[i][j] = min(dp[i][j - 1], INF + 1)

for i in range(q):
    l, r, x = querys[i].l, querys[i].r, querys[i].x
    if min(dp[l][log2[r - l + 1]], dp[r - (1 << log2[r - l + 1]) + 1][log2[r - l + 1]]) != x:
        g.write('inconsistent')
        break
else:
    g.write('consistent\n')
    g.write(' '.join(map(str, answer)))

f.close()
g.close()
