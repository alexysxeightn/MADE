class QueueBasedOnVector:
    def __init__(self):
        self.begin = 0
        self.end = 0
        self.capacity = 1
        self.elements = [0]
        
    def update_capacity(self, ensure = True):
        prev_capacity = self.capacity
        prev_size = self.size()
        if ensure:
            self.capacity *= 2
        else:
            self.capacity //= 4
        new_elements = [0] * self.capacity
        for i in range(prev_size):
            new_elements[i] = self.elements[(self.begin + i) % (prev_size + 1)]
        self.elements = new_elements
        self.end = prev_size
        self.begin = 0
        
    def next(self, i):
        return (i + 1) % self.capacity
        
    def size(self):
        return (self.end + self.capacity - self.begin) % self.capacity

    def push(self, x):
        if self.begin == self.next(self.end):
            self.update_capacity()
        self.elements[self.end] = x
        self.end = self.next(self.end)
        
    def pop(self):
        element = self.elements[self.begin]
        if self.size() - 1 < self.capacity // 4:
            self.update_capacity(ensure = False)
        self.begin = self.next(self.begin)
        return element
        
queue = QueueBasedOnVector()
n = int(input())
for _ in range(n):
    operation = input()
    if operation[0] == '+':
        x = int(operation[len('+ '):])
        queue.push(x)
    else:
        print(queue.pop())
