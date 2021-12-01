from sys import stdin

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.childrens = [[i] for i in range(n)]
        self.r = [0] * n
        self.xp = [0] * n
        
    def get(self, x):
        if self.p[x] != x:
            self.p[x] = self.get(self.p[x])
        return self.p[x]
        
    def get_xp(self, x):
        return self.xp[x]
        
    def join(self, x, y):
        x, y = self.get(x), self.get(y)
        if x != y:
            if self.r[x] > self.r[y]:
                x, y = y, x
            elif self.r[x] == self.r[y]:
                self.r[y] += 1
                
            self.p[x] = y
            self.childrens[y] += self.childrens[x]
            
    def add(self, x, v):
        for i in self.childrens[self.get(x)]:
            self.xp[i] += v

n, m = map(int, stdin.readline().split())
dsu = DSU(n)
for _ in range(m):
    operation = stdin.readline().split()
    if 'join' == operation[0]:
        x, y = int(operation[1]) - 1, int(operation[2]) - 1
        dsu.join(x, y)
    if 'get' == operation[0]:
        x = int(operation[1]) - 1
        print(dsu.get_xp(x))
    if 'add' == operation[0]:
        x, v = int(operation[1]) - 1, int(operation[2])
        dsu.add(x, v)
