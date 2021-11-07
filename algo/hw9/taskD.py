from sys import stdin
from random import randint

INF = 10 ** 6

class Node:
    def __init__(self, x):
        self.value = x
        self.y = randint(0, INF)
        self.left = None
        self.right = None
        self.size = 1
        self.reverse = False

class Treap:
    
    def __init__(self):
        self.head = None
    
    def get_size(self, v):
        if v is None:
            return 0
        return v.size
    
    def fix_size(self, v):
        v.size = self.get_size(v.left) + self.get_size(v.right) + 1

    def push(self, v):
        if v is None or not v.reverse:
            return
        v.left, v.right = v.right, v.left
        v.reverse = False
        if not(v.left is None):
            v.left.reverse = not v.left.reverse
        if not(v.right is None):
            v.right.reverse = not v.right.reverse

    def split(self, x):
        return self._split(self.head, x)
        
    def _split(self, v, x):
        self.push(v)
        if v is None:
            return None, None
        if self.get_size(v.left) > x:
            t1, t2 = self._split(v.left, x)
            v.left = t2
            self.fix_size(v)
            return t1, v
        else:
            t1, t2 = self._split(v.right, x - self.get_size(v.left) - 1)
            v.right = t1
            self.fix_size(v)
            return v, t2
    
    def merge(self, t1, t2):
        self.push(t1)
        self.push(t2)
        if t1 is None:
            return t2
        if t2 is None:
            return t1
        if t1.y > t2.y:
            t1.right = self.merge(t1.right, t2)
            self.fix_size(t1)
            return t1
        else:
            t2.left = self.merge(t1, t2.left)
            self.fix_size(t2)
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
        
    def reverse(self, l, r):
        t1, t2 = self.split(l - 1)
        t2, t3 = self._split(t2, r - l)
        t2.reverse = not t2.reverse
        t = self.merge(t1, t2)
        t = self.merge(t, t3)
        self.head = t
    
    def print_tree(self):
        return self._print_tree(self.head)
    
    def _print_tree(self, v):
        if not (v is None):
            self.push(v)
            self._print_tree(v.left)
            print(v.value, end = ' ')
            self._print_tree(v.right)

tree = Treap()

n, m = map(int, stdin.readline().split())
for i in range(n):
    tree.insert(i + 1)
for _ in range(m):
    l, r = map(lambda x: int(x) - 1, stdin.readline().split())
    tree.reverse(l, r)
tree.print_tree()
