from heapq import heappop, heappush
from sys import stdin

INF = 10e9

def dijkstra(graph, n, s):
    dist = [INF] * n
    dist[s] = 0
    used = [False] * n
    queue = [(0, s)]
    while len(queue) != 0:
        next = heappop(queue)[1]
        if used[next]:
            continue
        used[next] = True
        for u, w in graph[next]:
            if dist[u] > dist[next] + w:
                dist[u] = dist[next] + w
                heappush(queue, (dist[u], u))
    return dist

n, m = map(int, stdin.readline().split())
graph = [[] for _ in range(n)]
for _ in range(m):
    u, v, w = map(int, stdin.readline().split())
    u, v = u - 1, v - 1
    graph[u].append((v, w))
    graph[v].append((u, w))
print(*dijkstra(graph, n, 0))
