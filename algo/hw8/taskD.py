INF = 10 ** 9

class Node:
    def __init__(self, x):
        self.key = x
        self.left = None
        self.right = None
        self.h = 1
        self.min = x
        self.max = x
        self.sum = 0

class AVLTree:
    
    def __init__(self):
        self.head = None
    
    def insert(self, x):
        if self.head is None:
            self.head = Node(x)
        else:
            self.head = self._insert(self.head, x)
    
    def _insert(self, v, x):
        if v is None:
            return Node(x)
        elif x < v.key:
            v.left = self._insert(v.left, x)
        elif x > v.key:
            v.right = self._insert(v.right, x)
        return self.balance(v)
    
    def get_height(self, v):
        if v is None:
            return 0
        return v.h
        
    def get_sum(self, v):
        if v is None:
            return 0
        return v.sum
        
    def get_min(self, v):
        if v is None:
            return INF
        return v.min
        
    def get_max(self, v):
        if v is None:
            return -INF
        return v.max
    
    def fix_height_sum_min_max(self, v):
        if not (v is None):
            v.h = max(self.get_height(v.left),
                      self.get_height(v.right)) + 1
                      
            v.sum = self.get_sum(v.left) + self.get_sum(v.right)
            if not (v.left is None):
                v.sum += v.left.key
            if not (v.right is None):
                v.sum += v.right.key
                
            v.min = min(self.get_min(v.left), self.get_min(v.right), v.key)
            v.max = max(self.get_max(v.left), self.get_max(v.right), v.key)
            
    def small_rotate_right(self, p):
        q = p.left
        p.left = q.right
        q.right = p
        self.fix_height_sum_min_max(p)
        self.fix_height_sum_min_max(q)
        return q
        
    def small_rotate_left(self, q):
        p = q.right
        q.right = p.left
        p.left = q
        self.fix_height_sum_min_max(q)
        self.fix_height_sum_min_max(p)
        return p
        
    def get_balance(self, v):
        if not (v is None):
            return self.get_height(v.right) - self.get_height(v.left)
        
    def balance(self, p):
        self.fix_height_sum_min_max(p)
        
        if 2 == self.get_balance(p):
            if self.get_balance(p.right) < 0:
                p.right = self.small_rotate_right(p.right)
            return self.small_rotate_left(p)
            
        if -2 == self.get_balance(p):
            if self.get_balance(p.left) > 0:
                p.left = self.small_rotate_left(p.left)
            return self.small_rotate_right(p)
        
        return p
    
    def sum(self, l, r):
        return self._sum(self.head, l, r)
    
    def _sum(self, v, l, r):
        if v is None:
            return 0
        if v.key > r:
            return self._sum(v.left, l, r)
        if v.key < l:
            return self._sum(v.right, l, r)
        if v.left is None and v.right is None:
            return v.key
        if v.min >= l and v.max <= r:
            return v.sum + v.key
        return self._sum(v.left, l, r) + self._sum(v.right, l, r) + v.key
        
AVL = AVLTree()

n = int(input())
prev_operation_is_query = False
for _ in range(n):
    operation = input().split()
    if operation[0] == '+':
        x = int(operation[1])
        if prev_operation_is_query:
            AVL.insert((x + y) % INF)
        else:
            AVL.insert(x)
        prev_operation_is_query = False
    elif operation[0] == '?':
        l, r = int(operation[1]), int(operation[2])
        y = AVL.sum(l, r)
        print(y)
        prev_operation_is_query = True
