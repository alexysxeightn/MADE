class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.max = list(range(n))
        self.min = list(range(n))
        self.size = [1] * n
        
    def get(self, x):
        if self.p[x] != x:
            self.p[x] = self.get(self.p[x])
        return self.p[x]
        
    def join(self, x, y):
        x, y = self.get(x), self.get(y)
        if x != y:
            if self.size[x] > self.size[y]:
                x, y = y, x
            self.p[x] = y
            
            self.size[y] = self.size[x] + self.size[y]
            
            if self.max[x] > self.max[y]:
                self.max[y] = self.max[x]
            else:
                self.max[x] = self.max[y]
                
            if self.min[x] < self.min[y]:
                self.min[y] = self.min[x]
            else:
                self.min[x] = self.min[y]
            
    def print(self, x):
        x = self.get(x)
        print(self.min[x] + 1, self.max[x] + 1, self.size[x])

n = int(input())
dsu = DSU(n)
while True:
    try:
        operation = input().split()
        if 'union' == operation[0]:
            x, y = int(operation[1]) - 1, int(operation[2]) - 1
            dsu.join(x, y)
        if 'get' == operation[0]:
            x = int(operation[1]) - 1
            dsu.print(x)
    except:
        break
