from sys import setrecursionlimit
import threading

def dfs_first(v, used, order, V):
    used[v] = True
    for u in V[v]:
        if not used[u]:
            dfs_first(u, used, order, V)
    order.append(v)
    
def dfs_second(v, color, cur, V):
    color[v] = cur
    for u in V[v]:
        if color[u] == 0:
            dfs_second(u, color, cur, V)

def main():
    n, m = map(int, input().split())
    V = [[] for _ in range(n)]
    V_inv = [[] for _ in range(n)]
    for _ in range(m):
        b, e = map(int, input().split())
        b, e = b - 1, e - 1
        V[b].append(e)
        V_inv[e].append(b)
    
    order = []
    used = [False] * n
    for v in range(n):
        if not used[v]:
            dfs_first(v, used, order, V)
    order = order[::-1]
    
    color = [0] * n
    count = 0
    for v in order:
        if color[v] == 0:
            count += 1
            dfs_second(v, color, count, V_inv)
    
    s = set()
    for v in range(n):
        for u in V[v]:
            if color[v] != color[u]:
                s.add((color[v], color[u]))
    print(len(s))

setrecursionlimit(10 ** 9)
threading.stack_size(2 ** 26)
thread = threading.Thread(target=main)
thread.start()
