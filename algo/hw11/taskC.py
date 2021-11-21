INF = 10 ** 9
MAX_W = 10 ** 5

def floyd(edges, n):
    dist = [INF] * n
    dist[0] = 0
    p = [-1] * n
    
    num_edges = len(edges)
    for i in range(n):
        next = -1
        for j in range(num_edges):
            u, v, w = edges[j]
            if dist[v] > dist[u] + w:
                dist[v] = max(-INF, dist[u] + w)
                p[v] = u
                next = v
    if -1 == next:
        return

    y = next
    for _ in range(n):
        y = p[y]
    path = [y + 1]    
    cur = p[y]
    while cur != y:
        path.append(cur + 1)
        cur = p[cur]
    return path[::-1]

n = int(input())
edges = []
for i in range(n):
    for j, w in enumerate(map(int, input().split())):
        if w != MAX_W:
            edges.append((i, j, w))
res = floyd(edges, n)
if res:
    print('YES')
    print(len(res))
    print(*res)
else:
    print('NO')
