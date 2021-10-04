class Heap:
    def __init__(self):
        self.elements = []
        self.size = 0
        self.order = [] # Array with operation numbers
        self.operation_count = 0 # The number of operations
    
    def swap(self, i, j):
        self.elements[i], self.elements[j] = self.elements[j], self.elements[i]
        self.order[i], self.order[j] = self.order[j], self.order[i]
    
    def sift_up(self, i):
        while i > 0 and self.elements[i] < self.elements[(i - 1) // 2]:
            self.swap(i, (i - 1) // 2)
            i = (i - 1) // 2
            
    def sift_down(self, i):
        while 2 * i + 1 < self.size:
            left = 2 * i + 1
            right = 2 * i + 2
            j = left
            if right < self.size and self.elements[right] < self.elements[left]:
                j = right
            if self.elements[i] <= self.elements[j]:
                break
            self.swap(i, j)
            i = j
        
    def insert(self, x):
        i = self.size
        if len(self.elements) > i: # If there is space in the array, then insert the element
            self.elements[i] = x
            self.order[i] = self.operation_count
        else: # Otherwise we add it to the right
            self.elements.append(x)
            self.order.append(self.operation_count)
        self.operation_count += 1 # Increasing the number of operations
        self.size += 1
        self.sift_up(i)
        
    def extract_min(self):
        self.operation_count += 1 # Increasing the number of operations
        if not self.size:
            return '*'
        min_value, min_order = self.elements[0], self.order[0] + 1
        self.swap(0, self.size - 1)
        self.size -= 1
        i = 0
        self.sift_down(i)
        return (min_value, min_order)
        
    def find_index(self, x): # Function for searching the index of an element by operation number
        for i in range(self.operation_count):
            if self.order[i] == x:
                return i
        
    def decrease_key(self, x, v):
        self.operation_count += 1 # Increasing the number of operations
        i = self.find_index(x)
        self.elements[i] = v
        self.sift_up(i)

heap = Heap()

while True:
    try:
        operation = input()
        if operation[:len('push')] == 'push':
            x = int(operation[len('push '):])
            heap.insert(x)
        elif operation == 'extract-min':
            print(*heap.extract_min())
        else:
            x, v = map(int, operation[len('decrease-key'):].split())
            heap.decrease_key(x - 1, v)
    except:
        break
