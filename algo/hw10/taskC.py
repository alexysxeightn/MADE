from sys import setrecursionlimit
import threading

has_cycle = False

def dfs(v, used, ans, V):
    used[v] = True
    for u in V[v]:
        if not used[u]:
            dfs(u, used, ans, V)
    ans.append(v + 1)
    
def dfs_check_cycle(v, color, V):
    global has_cycle
    color[v] = 1
    for u in V[v]:
        if color[u] == 0:
            dfs_check_cycle(u, color, V)
        elif color[u] == 1:
            has_cycle = True
            return
    color[v] = 2

def main():
    n, m = map(int, input().split())
    V = [[] for _ in range(n)]
    for _ in range(m):
        b, e = map(int, input().split())
        b, e = b - 1, e - 1
        V[b].append(e)
    
    color = [0] * n
    for v in range(n):
        if color[v] == 0:
            dfs_check_cycle(v, color, V)
                
    if not has_cycle:
        used = [False] * n
        ans = []
        for v in range(n):
            if not used[v]:
                dfs(v, used, ans, V)
        print(*ans[::-1])
    else:
        print('-1')
        
setrecursionlimit(10 ** 9)
threading.stack_size(2 ** 26)
thread = threading.Thread(target=main)
thread.start()
