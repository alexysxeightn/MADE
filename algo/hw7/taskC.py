class FenwickTree:
    def __init__(self, a):
        self.a = a
        self.n = len(a)
        self.T = [0] * len(a)
        for i in range(self.n):
            self.add(i, self.a[i])

    def F(self, i):
        return i & (i + 1)

    def add(self, i, x):
        j = i
        while j < self.n:
            self.T[j] += x
            j = j | (j + 1)

    def set(self, i, x):
        d = x - self.a[i]
        self.a[i] = x
        self.add(i, d)

    def get(self, i):
        res = 0
        while i >= 0:
            res += self.T[i]
            i = self.F(i) - 1
        return res
    
    def rsq(self, left, right):
        if 0 == left:
            return self.get(right)
        return self.get(right) - self.get(left - 1)

n = int(input())
a = [*map(int, input().split())]
tree = FenwickTree(a)

while True:
    try:
        operation, a, b = input().split()
        a, b = int(a), int(b)
        if 'sum' == operation:
            print(tree.rsq(a - 1, b - 1))
        else:
            tree.set(a - 1, b)
    except:
        break
