class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0] * n
        
    def get(self, x):
        if self.p[x] != x:
            self.p[x] = self.get(self.p[x])
        return self.p[x]
        
    def join(self, x, y):
        x, y = self.get(x), self.get(y)
        if x != y:
            if self.r[x] > self.r[y]:
                x, y = y, x
            if self.r[x] == self.r[y]:
                self.r[y] += 1
            self.p[x] = y

n, m = map(int, input().split())
dsu = DSU(n)
graph = [None] * m
answer = 0
for i in range(m):
    b, e, w = map(int, input().split())
    graph[i] = (b - 1, e - 1, w)
graph = sorted(graph, key=lambda x: x[2])
for u, v, w in graph:
    if dsu.get(u) != dsu.get(v):
        answer += w
        dsu.join(u, v)
print(answer)
