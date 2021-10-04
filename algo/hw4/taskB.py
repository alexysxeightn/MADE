class StackBasedOnVector:
    def __init__(self):
        self.size = 0
        self.capacity = 1
        self.elements = [0]
    
    def update_capacity(self, ensure = True):
        if ensure:
            self.capacity *= 2
        else:
            self.capacity //= 4
        new_elements = [0] * self.capacity
        for i in range(self.size):
            new_elements[i] = self.elements[i]
        self.elements = new_elements

    def push(self, x):
        if self.size + 1 > self.capacity:
            self.update_capacity()
        self.elements[self.size] = x
        self.size += 1
        
    def pop(self):
        element = self.elements[self.size - 1]
        if self.size - 1 < self.capacity // 4:
            self.update_capacity(ensure = False)
        self.size -= 1
        return element
        
stack = StackBasedOnVector()
for i in input().split():
    if i in ('+', '*', '-'):
        b = stack.pop()
        a = stack.pop()
        if i == '+':
            stack.push(a + b)
        elif i == '-':
            stack.push(a - b)
        else:
            stack.push(a * b)
    else:
        stack.push(int(i))

print(stack.pop())
