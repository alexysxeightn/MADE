LEN_ALPHABET = 26

def chr_to_num(c):
    return ord(c) - ord('a')
    
class Vertex:
    def __init__(self, id, alpha, parent, pchar):
        self.id = id
        self.next = [None] * alpha
        self.is_terminal = False
        self.parent = parent
        self.pchar = pchar
        self.sufflink = None
        self.up = None
        self.go = [None] * alpha
        self.idx = -1

class Trie:
    def __init__(self, alpha):
        self.alpha = alpha
        self.vertices = [Vertex(0, alpha, None, None)]
        self.root = self.vertices[0]
        
    def size(self):
        return len(self.vertices)
        
    def last(self):
        return self.vertices[-1]
        
    def insert(self, s, idx):
        v = self.root
        n = len(s)
        for i in range(n):
            if v.next[chr_to_num(s[i])] is None:
                self.vertices.append(Vertex(self.size(), self.alpha, v, s[i]))
                v.next[chr_to_num(s[i])] = self.last()
            v = v.next[chr_to_num(s[i])]
        v.is_terminal = True
        v.idx = idx
        
    def contains(self, s):
        v = self.root
        n = len(s)
        for i in range(n):
            if v.next[chr_to_num(s[i])] is None:
                return False
            v = v.next[chr_to_num(s[i])]
        return v.is_terminal
        
    def get_link(self, v):
        if v.sufflink is None:
            if v == self.root or v.parent == self.root:
                v.sufflink = self.root
            else:
                v.sufflink = self.go(self.get_link(v.parent), v.pchar)
        return v.sufflink
        
    def go(self, v, c):
        if v.go[chr_to_num(c)] is None:
            if v.next[chr_to_num(c)] is not None:
                v.go[chr_to_num(c)] = v.next[chr_to_num(c)]
            elif v == self.root:
                v.go[chr_to_num(c)] = self.root
            else:
                v.go[chr_to_num(c)] = self.go(self.get_link(v), c)
        return v.go[chr_to_num(c)]
        
    def get_up(self, v):
        if v.up is None:
            if self.get_link(v).is_terminal:
                v.up = self.get_link(v)
            elif self.get_link(v) == self.root:
                v.up = self.root
            else:
                v.up = self.get_up(self.get_link(v))
        return v.up
        
    def find_on_text(self, text, m):
        bool_mask = [False] * m
        v = self.root
        for i in range(len(text)):
            v = self.go(v, text[i])
            u = v
            while u != self.root:
                if u.is_terminal:
                    bool_mask[u.idx] = True
                u = self.get_up(u)
        return bool_mask

trie = Trie(LEN_ALPHABET)

text = input()
m = int(input())
for i in range(m):
    trie.insert(input(), i)

bool_mask = trie.find_on_text(text, m)
print(*['Yes' if x else 'No' for x in bool_mask], sep='\n')
