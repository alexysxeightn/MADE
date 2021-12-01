INF = 10 ** 9

def dist(u, v, points):
    if u == v:
        return INF
    u, v = points[u], points[v]
    return ((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2) ** 0.5
    
n = int(input())
points = [None] * n
for i in range(n):
    x, y = map(int, input().split())
    points[i] = (x, y)
    
answer = 0
used = [False] * n
min_edge = [INF] * n
select_edge = [-1] * n

for _ in range(n):
    v = -1
    for j in range(n):
        if not used[j] and (v == -1 or min_edge[j] < min_edge[v]):
            v = j
    used[v] = True
    if select_edge[v] != -1:
        answer += dist(v, select_edge[v], points)
    for u in range(n):
        distance = dist(u, v, points)
        if distance < min_edge[u]:
            min_edge[u] = distance
            select_edge[u] = v

print(answer)
