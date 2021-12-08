from collections import deque
from sys import stdin

INF = 10 ** 9

class Edge:
    def __init__(self, from_, to, c, f):
        self.from_ = from_
        self.to = to
        self.c = c
        self.f = f

def bfs(s, t, graph, edges, n, scale):
    global flow
    dist = [INF] * n
    p = [-1] * n
    dist[s] = 0
    queue = deque()
    queue.append(s)
    while len(queue):
        v = queue.popleft()
        for i in graph[v]:
            edge = edges[i]
            if dist[edge.to] > dist[v] + 1 and edge.f < edge.c and edge.c >= scale:
                dist[edge.to] = dist[v] + 1
                queue.append(edge.to)
                p[edge.to] = i
            
    if INF == dist[t]:
        return False
    
    v = t
    delta = INF
    while v != s:
        delta = min(delta, edges[p[v]].c - edges[p[v]].f)
        v = edges[p[v]].from_
    flow += delta
    
    v = t
    while v != s:
        edges[p[v]].f += delta
        edges[p[v] ^ 1].f -= delta
        v = edges[p[v]].from_
        
    return True

def add_edge(graph, edges, u, v, c):
    graph[u].append(len(edges))
    edges.append(Edge(u, v, c, 0))
    graph[v].append(len(edges))
    edges.append(Edge(v, u, c, 0))

def find_max_flow(s, t, graph, edges, n, U):
    global flow
    
    log2_U = 0
    while U != 0:
        U = U >> 1
        log2_U += 1
    log2_U -= 1
    
    scale = 1 << log2_U
    
    flow = 0
    while scale >= 1:
        while bfs(s, t, graph, edges, n, scale):
            pass
        scale //= 2
    
    return flow

n = int(stdin.readline())
m = int(stdin.readline())
graph = [[] for _ in range(n)]
edges = []

U = -1
for _ in range(m):
    a, b, c = map(int, stdin.readline().split())
    U = max(U, c)
    add_edge(graph, edges, a - 1, b - 1, c)

print(find_max_flow(0, n - 1, graph, edges, n, U))
print(*[edges[i].f for i in range(0, 2 * m, 2)], sep='\n')
