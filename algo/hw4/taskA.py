from sys import stdin

class Node:
    def __init__(self, value = None):
        self.value = value
        self.min_prev = value
        self.next_node = None
        
class Stack:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def push(self, x):
        new_node = Node(x)
        if self.size == 0:
            self.head = new_node
            self.tail = new_node
        else:
            if new_node.value > self.head.min_prev:
                new_node.min_prev = self.head.min_prev
            new_node.next_node = self.head
            self.head = new_node
        self.size += 1
        
    def pop(self):
        if self.head == None or self.head.next_node == None:
            self.head = None
        else:
            self.head = self.head.next_node
        self.size -= 1

    def get_min(self):
        return self.head.min_prev
        
n = int(stdin.readline())
stack = Stack()
for _ in range(n):
    operation = stdin.readline()
    if operation[0] == '1':
        x = int(operation[len('1 '):])
        stack.push(x)
    elif operation == '2\n':
        stack.pop()
    else:
        print(stack.get_min())
