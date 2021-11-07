from random import randint

INF = 10 ** 9

class Node:
    def __init__(self, x):
        self.value = x
        self.y = randint(0, INF)
        self.left = None
        self.right = None
        self.size = 1

class Treap:
    
    def __init__(self):
        self.head = None
    
    def get_size(self, v):
        if v is None:
            return 0
        return v.size
    
    def size_of_tree(self):
        return self.get_size(self.head)
    
    def fix_size(self, v):
        v.size = self.get_size(v.left) + self.get_size(v.right) + 1

    def split(self, x):
        return self._split(self.head, x)
        
    def _split(self, v, x):
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
    
    def insert(self, i, x):
        if self.head is None:
            self.head = Node(x)
        else:
            self.head = self._insert(self.head, i, x)
    
    def _insert(self, v, i, x):
        new_node = Node(x)
        t1, t2 = self._split(v, i)
        t1 = self.merge(t1, new_node)
        t = self.merge(t1, t2)
        return t
        
    def delete(self, i):
        self.head = self._delete(self.head, i)
        
    def _delete(self, v, i):
        t1, t2 = self._split(v, i)
        t11, t1 = self._split(t1, i - 1)
        t = self.merge(t11, t2)
        return t
        
    def print_tree(self):
        return self._print_tree(self.head)
    
    def _print_tree(self, v):
        if not (v is None):
            self._print_tree(v.left)
            print(v.value, end = ' ')
            self._print_tree(v.right)

tree = Treap()

n_0, m = map(int, input().split())
a = [*map(int, input().split())]

for i, a_i in enumerate(a):
    tree.insert(i, a_i)
    
for _ in range(m):
    operation = input().split()
    if 'del' == operation[0]:
        i = int(operation[1]) - 1
        tree.delete(i)
    if 'add' == operation[0]:
        i, x = int(operation[1]) - 1, int(operation[2])
        tree.insert(i, x)

print(tree.size_of_tree())
tree.print_tree()
