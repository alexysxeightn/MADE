from collections import deque

INF = 10e9

def bfs(s, t, n):
    dist = [[INF] * n for _ in range(n)]
    p = [[None] * n for _ in range(n)]
    used = [[False] * n for _ in range(n)]
    delta = [(-2, -1),
             (-2, 1),
             (-1, -2),
             (-1, 2),
             (1, -2),
             (1, 2),
             (2, -1),
             (2, 1)]
    queue = deque()
    
    dist[s[0]][s[1]] = 0
    used[s[0]][s[1]] = True
    
    queue.append(s)
    while len(queue) != 0:
        x, y = queue.popleft()
        for dx, dy in delta:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and not used[nx][ny]:
                dist[nx][ny] = dist[x][y] + 1
                p[nx][ny] = (x, y)
                used[nx][ny] = True
                queue.append((nx, ny))

    cur = t
    path = []
    while cur:
        path.append((cur[0] + 1, cur[1] + 1))
        cur = p[cur[0]][cur[1]]
    path = path[::-1]
    return path

n = int(input())
x_1, y_1 = map(lambda x: int(x) - 1, input().split())
x_2, y_2 = map(lambda x: int(x) - 1, input().split())
path = bfs((x_1, y_1), (x_2, y_2), n)
print(len(path))
for x, y in path:
    print(x, y)
