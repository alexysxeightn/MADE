class Node:
    def __init__(self, x):
        self.key = x
        self.left = None
        self.right = None
        self.h = 1
        self.size = 1

class AVLTree:
    
    def __init__(self):
        self.head = None
        self.length = 0
    
    def insert(self, x):
        if self.head is None:
            self.head = Node(x)
            self.length = 1
        else:
            self.head = self._insert(self.head, x)
            self.length += 1
    
    def _insert(self, v, x):
        if v is None:
            return Node(x)
        elif x < v.key:
            v.left = self._insert(v.left, x)
        elif x > v.key:
            v.right = self._insert(v.right, x)
        return self.balance(v)
        
    def delete(self, x):
        self.head = self._delete(self.head, x)
        self.length -= 1
    
    def _delete(self, v, x):
        if v is None:
            return None
        if x < v.key:
            v.left = self._delete(v.left, x)
        elif x > v.key:
            v.right = self._delete(v.right, x)
        elif v.left is None:
            v = v.right
        elif v.right is None:
            v = v.left
        else:
            v.key = self.find_max(v.left).key
            v.left = self._delete(v.left, v.key)
        return self.balance(v)
        
    def find_max(self, v):
        while not (v.right is None):
            v = v.right
        return v
    
    def get_height(self, v):
        if v is None:
            return 0
        return v.h
        
    def get_size(self, v):
        if v is None:
            return 0
        return v.size
    
    def fix_height_and_size(self, v):
        if not (v is None):
            v.h = max(self.get_height(v.left),
                      self.get_height(v.right)) + 1
            v.size = 1 + self.get_size(v.left) + self.get_size(v.right)
    
    def small_rotate_right(self, p):
        q = p.left
        p.left = q.right
        q.right = p
        self.fix_height_and_size(p)
        self.fix_height_and_size(q)
        return q
        
    def small_rotate_left(self, q):
        p = q.right
        q.right = p.left
        p.left = q
        self.fix_height_and_size(q)
        self.fix_height_and_size(p)
        return p
        
    def get_balance(self, v):
        if not (v is None):
            return self.get_height(v.right) - self.get_height(v.left)
        
    def balance(self, p):
        self.fix_height_and_size(p)
        
        if 2 == self.get_balance(p):
            if self.get_balance(p.right) < 0:
                p.right = self.small_rotate_right(p.right)
            return self.small_rotate_left(p)
        
        if -2 == self.get_balance(p):
            if self.get_balance(p.left) > 0:
                p.left = self.small_rotate_left(p.left)
            return self.small_rotate_right(p)
        
        return p
        
    def find_k_max(self, k):
        return self._find_k_max(self.length - k, self.head)
        
    def _find_k_max(self, k, v):
        left_size = self.get_size(v.left)
        if k == left_size:
            return v.key
        elif left_size > k:
            return self._find_k_max(k, v.left)
        else:
            k -= left_size + 1
            return self._find_k_max(k, v.right)

AVL = AVLTree()

n = int(input())
for _ in range(n):
    operation, k = input().split()
    k = int(k)
    if '1' == operation or '+1' == operation:
        AVL.insert(k)
    if '0' == operation:
        print(AVL.find_k_max(k))
    if '-1' == operation:
        AVL.delete(k)
