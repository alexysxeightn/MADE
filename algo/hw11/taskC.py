    INF = 10 ** 5
     
    def floyd(d, n):
        next = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in range(n):
                next[u][v] = v
        
        for k in range(n):
            for u in range(n):
                for v in range(n):
                    if d[u][k] == INF or d[k][v] == INF:
                        continue
                    if d[u][v] > d[u][k] + d[k][v]:
                        d[u][v] = max(-INF, d[u][k] + d[k][v])
                        next[u][v] = next[u][k]
                        if u == v and d[u][v] < 0:
                            path = [v + 1]
                            cur = next[v][v]
                            while cur != v:
                                path.append(cur + 1)
                                cur = next[cur][v]
                            return path
        return False
     
    n = int(input())
    graph = [0] * n
    for i in range(n):
        graph[i] = [*map(int, input().split())]
    res = floyd(graph, n)
    if res:
        print('YES')
        print(len(res))
        print(*res)
    else:
        print('NO')
