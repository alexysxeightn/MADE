class Node:
    def __init__(self, x):
        self.key = x
        self.left = None
        self.right = None
        self.h = 1

class AVLTree:
    
    def __init__(self):
        self.head = None
        
    def search(self, x):
        return self._search(self.head, x)
    
    def _search(self, v, x):
        if v is None or v.key == x:
            return v
        elif x < v.key:
            return self._search(v.left, x)
        else:
            return self._search(v.right, x)
        
    def exists(self, x):
        return (not self.search(x) is None)
    
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
        
    def delete(self, x):
        self.head = self._delete(self.head, x)
    
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
        
    def next(self, x):
        v, res = self.head, None
        while not (v is None):
            if v.key > x:
                res = v
                v = v.left
            else:
                v = v.right
        if res is None:
            return None
        return res.key
        
    def prev(self, x):
        v, res = self.head, None
        while not (v is None):
            if v.key < x:
                res = v
                v = v.right
            else:
                v = v.left
        if res is None:
            return None
        return res.key
    
    def get_height(self, v):
        if v is None:
            return 0
        return v.h
    
    def fix_height(self, v):
        if not (v is None):
            v.h = max(self.get_height(v.left),
                      self.get_height(v.right)) + 1
    
    def small_rotate_right(self, p):
        q = p.left
        p.left = q.right
        q.right = p
        self.fix_height(p)
        self.fix_height(q)
        return q
        
    def small_rotate_left(self, q):
        p = q.right
        q.right = p.left
        p.left = q
        self.fix_height(q)
        self.fix_height(p)
        return p
        
    def get_balance(self, v):
        if not (v is None):
            return self.get_height(v.right) - self.get_height(v.left)
        
    def balance(self, p):
        self.fix_height(p)
        
        if 2 == self.get_balance(p):
            if self.get_balance(p.right) < 0:
                p.right = self.small_rotate_right(p.right)
            return self.small_rotate_left(p)
            
        if -2 == self.get_balance(p):
            if self.get_balance(p.left) > 0:
                p.left = self.small_rotate_left(p.left)
            return self.small_rotate_right(p)
            
        return p

AVL = AVLTree()

while True:
    try:
        operation, x = input().split()
        x = int(x)
        if 'insert' == operation:
            AVL.insert(x)
        elif 'exists' == operation:
            print(str(AVL.exists(x)).lower())
        elif 'delete' == operation:
            AVL.delete(x)
        elif 'next' == operation:
            print(str(AVL.next(x)).lower())
        elif 'prev' == operation:
            print(str(AVL.prev(x)).lower())
    except:
        break
