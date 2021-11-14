from sys import setrecursionlimit
import threading

def dfs(v, color, cur, V):
    color[v] = cur
    for u in V[v]:
        if 0 == color[u]:
            dfs(u, color, cur, V)

def main():
    n, m = map(int, input().split())
    V = [[] for _ in range(n)]
    for _ in range(m):
        b, e = map(int, input().split())
        b, e = b - 1, e - 1
        V[b].append(e)
        V[e].append(b)
    
    count = 0
    color = [0] * n
    for v in range(n):
        if 0 == color[v]:
            count += 1
            dfs(v, color, count, V)
            
    print(count)
    print(*color)
    
setrecursionlimit(10 ** 9)
threading.stack_size(2 ** 26)
thread = threading.Thread(target=main)
thread.start()
