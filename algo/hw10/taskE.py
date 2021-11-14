from sys import setrecursionlimit
import threading

def dfs(v, used, tin, up, time, parent, ans, V):
    used[v] = True
    time += 1
    tin[v] = up[v] = time
    child = 0
    for u in V[v]:
        if u == parent:
            continue
        if used[u]:
            up[v] = min(up[v], tin[u])
        else:
            dfs(u, used, tin, up, time, v, ans, V)
            child += 1
            up[v] = min(up[v], up[u])
            if (up[u] >= tin[v]) and (parent != -1):
                ans.add(v + 1)
    if -1 == parent and child > 1:
        ans.add(v + 1)

def main():
    n, m = map(int, input().split())
    V = [[] for _ in range(n)]
    for _ in range(m):
        b, e = map(int, input().split())
        b, e = b - 1, e - 1
        V[b].append(e)
        V[e].append(b)
    
    used = [False] * n
    tin, up = [0] * n, [0] * n
    ans = set()
    time = 0
    
    for v in range(n):
        if not used[v]:
            dfs(v, used, tin, up, time, -1, ans, V)
    
    print(len(ans))
    print(*sorted(ans))

setrecursionlimit(10 ** 9)
threading.stack_size(2 ** 26)
thread = threading.Thread(target=main)
thread.start()
