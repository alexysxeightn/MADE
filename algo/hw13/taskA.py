INF = 10 ** 9

class Edge:
    def __init__(self, from_, to, c, f):
        self.from_ = from_
        self.to = to
        self.c = c
        self.f = f

def push_flow(v, t, cur_flow, graph, edges, used):
    used[v] = True
    if v == t:
        return cur_flow
    for i in graph[v]:
        edge = edges[i]
        if not used[edge.to] and edge.f < edge.c:
            next_flow = min(cur_flow, edge.c - edge.f)
            delta = push_flow(edge.to, t, next_flow, graph, edges, used)
            if delta:
                edges[i].f += delta
                edges[i ^ 1].f -= delta
                return delta
    return 0

def add_edge(graph, edges, u, v, c):
    graph[u].append(len(edges))
    edges.append(Edge(u, v, c, 0))
    graph[v].append(len(edges))
    edges.append(Edge(v, u, c, 0))

def find_max_flow(s, t, graph, edges, n):
    flow = 0
    while True:
        used = [False] * n
        delta = push_flow(0, n - 1, INF, graph, edges, used)
        if delta:
            flow += delta
        else:
            return flow

n = int(input())
m = int(input())
graph = [[] for _ in range(n)]
edges = []
for _ in range(m):
    a, b, c = map(int, input().split())
    add_edge(graph, edges, a - 1, b - 1, c)

print(find_max_flow(0, n - 1, graph, edges, n))
