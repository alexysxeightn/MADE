from collections import deque
from sys import stdin, setrecursionlimit
import threading

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

def dfs(v, t, path, graph, edges, used):
    path.append(v + 1)
    if v == t:
        return
    for i in graph[v]:
        u = edges[i].to
        if not used[i] and 1 == edges[i].f:
            used[i] = True
            dfs(u, t, path, graph, edges, used)
            break

def add_edge(graph, edges, u, v):
    graph[u].append(len(edges))
    edges.append(Edge(u, v, 1, 0))
    graph[v].append(len(edges))
    edges.append(Edge(v, u, 0, 0))

def find_max_flow(s, t, graph, edges, n):
    flow = 0
    while True:
        used = [False] * n
        delta = push_flow(s, t, INF, graph, edges, used)
        if delta:
            flow += delta
        else:
            return flow

def main():
    n, m, s, t = map(int, input().split())
    s, t = s - 1, t - 1
    graph = [[] for _ in range(n)]
    edges = []
    for _ in range(m):
        a, b = map(int, stdin.readline().split())
        add_edge(graph, edges, a - 1, b - 1)
    
    flow = find_max_flow(s, t, graph, edges, n)
    
    if flow < 2:
        print('NO')
    else:
        print('YES')
        used = [False] * (2 * m)
        for _ in range(2):
            path = []
            dfs(s, t, path, graph, edges, used)
            print(*path)
    
setrecursionlimit(10 ** 9)
threading.stack_size(2 ** 26)
thread = threading.Thread(target=main)
thread.start()
