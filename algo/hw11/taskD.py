from sys import stdin

INF = 10e18

def find_ways(edges, dist, s, n):
    dist[s] = 0
    for i in range(n):
        for u, v, w in edges:
            if dist[u] < INF and dist[v] > dist[u] + w:
                dist[v] = max(-INF, dist[u] + w)
                
def dfs(v, used, graph):
    used[v] = True
    for u in graph[v]:
        if not used[u]:
            dfs(u, used, graph)
            
n, m, s = map(int, stdin.readline().split())
s -= 1
graph = [[] for _ in range(n)]
edges = []
for _ in range(m):
    u, v, w = map(int, stdin.readline().split())
    u, v = u - 1, v - 1
    graph[u].append(v)
    edges.append((u, v, w))
dist = [INF] * n
used = [False] * n

find_ways(edges, dist, s, n)
for i in range(n):
    for u, v, w in edges:
        if dist[u] < INF and dist[v] > dist[u] + w and not used[v]:
            dfs(v, used, graph)

answer = [0] * n
for i in range(n):
    if dist[i] == INF: answer[i] = '*'
    elif used[i]: answer[i] = '-'
    else: answer[i] = dist[i]
print(*answer, sep='\n')
