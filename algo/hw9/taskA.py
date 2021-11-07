from random import randint

INF = 10 ** 9

class Node:
    def __init__(self, x):
        self.x = x
        self.y = randint(0, INF)
        self.left = None
        self.right = None

class Treap:
    
    def __init__(self):
        self.head = None
        
    def find(self, x):
        return self._find(self.head, x)
    
    def _find(self, v, x):
        if v is None or v.x == x:
            return v
        elif x < v.x:
            return self._find(v.left, x)
        return self._find(v.right, x)

    def exists(self, x):
        return (not self.find(x) is None)

    def split(self, x):
        return self._split(self.head, x)
        
    def _split(self, v, x):
        if v is None:
            return None, None
        if v.x > x:
            t1, t2 = self._split(v.left, x)
            v.left = t2
            return t1, v
        else:
            t1, t2 = self._split(v.right, x)
            v.right = t1
            return v, t2
    
    def merge(self, t1, t2):
        if t1 is None:
            return t2
        if t2 is None:
            return t1
        if t1.y > t2.y:
            t1.right = self.merge(t1.right, t2)
            return t1
        else:
            t2.left = self.merge(t1, t2.left)
            return t2
    
    def insert(self, x):
        if self.head is None:
            self.head = Node(x)
        else:
            self.head = self._insert(self.head, x)
    
    def _insert(self, v, x):
        new_node = Node(x)
        t1, t2 = self._split(v, x)
        t1 = self.merge(t1, new_node)
        t = self.merge(t1, t2)
        return t
        
    def delete(self, x):
        self.head = self._delete(self.head, x)
        
    def _delete(self, v, x):
        t1, t2 = self._split(v, x)
        t11, t1 = self._split(t1, x - 1)
        t = self.merge(t11, t2)
        return t
        
    def next(self, x):
        v, res = self.head, None
        while not (v is None):
            if v.x > x:
                res = v
                v = v.left
            else:
                v = v.right
        if res is None:
            return None
        return res.x
        
    def prev(self, x):
        v, res = self.head, None
        while not (v is None):
            if v.x < x:
                res = v
                v = v.right
            else:
                v = v.left
        if res is None:
            return None
        return res.x
        
tree = Treap()

while True:
    try:
        operation, x = input().split()
        x = int(x)
        if 'insert' == operation:
            tree.insert(x)
        elif 'exists' == operation:
            print(str(tree.exists(x)).lower())
        elif 'delete' == operation:
            tree.delete(x)
        elif 'next' == operation:
            print(str(tree.next(x)).lower())
        elif 'prev' == operation:
            print(str(tree.prev(x)).lower())
    except:
        break
