class Node:
    def __init__(self, x):
        self.key = x
        self.left = None
        self.right = None

class BinarySearchTree:
    
    def __init__(self):
        self.head = None
        
    def search(self, x):
        return self._search(self.head, x)
    
    def _search(self, v, x):
        if v is None or v.key == x:
            return v
        elif x < v.key:
            return self._search(v.left, x)
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
        return v
        
    def delete(self, x):
        self.head = self._delete(self.head, x)
    
    def _delete(self, v, x):
        if v is None:
            return None
        elif x < v.key:
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
        return v
        
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

BST = BinarySearchTree()

while True:
    try:
        operation, x = input().split()
        x = int(x)
        if 'insert' == operation:
            BST.insert(x)
        elif 'exists' == operation:
            print(str(BST.exists(x)).lower())
        elif 'delete' == operation:
            BST.delete(x)
        elif 'next' == operation:
            print(str(BST.next(x)).lower())
        elif 'prev' == operation:
            print(str(BST.prev(x)).lower())
    except:
        break
