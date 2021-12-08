from collections import deque
from sys import stdin, setrecursionlimit
import threading

INF = 10 ** 9

class Edge:
    def __init__(self, from_, to, c, f, x=None, y=None, rev=None):
        self.from_ = from_
        self.to = to
        self.c = c
        self.f = f
        self.reversed = None
        
        if x is None:
            self.x = -1
            self.y = -1
            self.rev = True
        else:
            self.x = x
            self.y = y
            self.rev = rev
            
def get_input_index(i, j):
    global m
    return i * m + j
    
def get_output_index(i, j):
    global n, m
    return i * m + j + n * m
    
def bfs(s, t, edges, size):
    global dist
    dist = [-1] * size
    dist[s] = 0
    queue = deque()
    queue.append(s)
    while len(queue) != 0:
        v = queue.popleft()
        for edge in edges[v]:
            if dist[edge.to] == -1 and edge.f < edge.c:
                dist[edge.to] = dist[v] + 1
                queue.append(edge.to)
            
    return dist[t] != -1

def push_flow(v, t, cur_flow, edges, p):
    global dist
    if v == t:
        return cur_flow
    while p[v] < len(edges[v]):
        edge = edges[v][p[v]]
        if dist[edge.to] == dist[v] + 1 and edge.f < edge.c:
            next_flow = min(cur_flow, edge.c - edge.f)
            delta = push_flow(edge.to, t, next_flow, edges, p)
            if delta:
                edge.f += delta
                if edge.rev:
                    edge.reversed.f -= delta
                return delta
        p[v] += 1
    return 0

def dfs(v, edges, used, visited):
    used[v] = True
    visited.append(v)
    for edge in edges[v]:
        if not used[edge.to] and edge.f < edge.c:
            dfs(edge.to, edges, used, visited)

def add_edge(edges, v, u, c):
    edges[v].append(Edge(v, u, c, 0))
    edges[u].append(Edge(u, v, 0, 0))
    edges[u][-1].reversed = edges[v][-1]
    edges[v][-1].reversed = edges[u][-1]
    
def find_max_flow(s, t, edges, size):
    flow = 0
    while bfs(s, t, edges, size):
        p = [0] * size
        while True:
            delta = push_flow(s, t, INF, edges, p)
            if delta:
                flow += delta
            else:
                break
    return flow
    
def find_min_cut(s, edges, country, size):
    used = [False] * size
    visited = []
    dfs(s, edges, used, visited)
    for v in visited:
        for edge in edges[v]:
            if not used[edge.to] and 1 == edge.f:
                country[edge.x][edge.y] = '+'
                break

def main():
    global dist, n, m
    n, m = map(int, input().split())
    size = 2 * n * m
    edges = [[] for _ in range(size)]
    country = [[None] * m for _ in range(n)]
    
    for i in range(n):
        string = input()
        for j in range(m):
            country[i][j] = string[j]
            
            v = get_input_index(i, j)
            u = get_output_index(i, j)
            
            if '#' == string[j]:
                edges[v].append(Edge(v, u, 0, 0, i, j, False))
            elif '.' == string[j]:
                edges[v].append(Edge(v, u, 1, 0, i, j, False))
            elif '-' == string[j]:
                edges[v].append(Edge(v, u, INF, 0, i, j, False))
            elif 'A' == string[j]:
                s = u
            elif 'B' == string[j]:
                t = v
                
    for i in range(n - 1):
        for j in range(m - 1):
            add_edge(edges, get_output_index(i, j), get_input_index(i + 1, j), INF)
            add_edge(edges, get_output_index(i + 1, j), get_input_index(i, j), INF)
            add_edge(edges, get_output_index(i, j), get_input_index(i, j + 1), INF)
            add_edge(edges, get_output_index(i, j + 1), get_input_index(i, j), INF)
    
    for i in range(n - 1):
        add_edge(edges, get_output_index(i, m - 1), get_input_index(i + 1, m - 1), INF)
        add_edge(edges, get_output_index(i + 1, m - 1), get_input_index(i, m - 1), INF)
    
    for j in range(m - 1):
        add_edge(edges, get_output_index(n - 1, j), get_input_index(n - 1, j + 1), INF)
        add_edge(edges, get_output_index(n - 1, j + 1), get_input_index(n - 1, j), INF)
    
    flow = find_max_flow(s, t, edges, size)
    find_min_cut(s, edges, country, size)
    
    if flow >= INF:
        print(-1)
    else:
        print(flow)
        for i in range(n):
            for j in range(m):
                print(country[i][j], end = '')
            print()
            
setrecursionlimit(10 ** 9)
threading.stack_size(2 ** 26)
thread = threading.Thread(target=main)
thread.start()
