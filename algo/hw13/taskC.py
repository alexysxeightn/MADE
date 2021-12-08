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
    while len(queue) != 0:
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

def dfs(v, graph, edges, used):
    used[v] = True
    for i in graph[v]:
        edge = edges[i]
        if not used[edge.to] and edge.f < edge.c:
            dfs(edge.to, graph, edges, used)

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
    
    flow = 0
    scale = 1 << log2_U
    while scale >= 1:
        while bfs(s, t, graph, edges, n, scale):
            pass
        scale //= 2
        
    return flow

n, m = map(int, stdin.readline().split())
graph = [[] for _ in range(n)]
edges = []
U = -1
for _ in range(m):
    a, b, c = map(int, stdin.readline().split())
    U = max(U, c)
    add_edge(graph, edges, a - 1, b - 1, c)

flow = find_max_flow(0, n - 1, graph, edges, n, U)

used = [False] * n
dfs(0, graph, edges, used)
min_cut = []
for i in range(0, 2 * m, 2):
    if used[edges[i].from_] and not used[edges[i].to] or \
       used[edges[i].to] and not used[edges[i].from_]:
        min_cut.append(i // 2 + 1)
 
print(len(min_cut), flow)
print(*min_cut)
