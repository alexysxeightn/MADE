from collections import defaultdict
from sys import setrecursionlimit
import threading

AUTHOR = 'polycarp'
max_length = -1

def dfs(v, used, length, V):
    global max_length
    used[v] = True
    for u in V[v]:
        if not used[u]:
            dfs(u, used, length + 1, V)
    if length > max_length:
        max_length = length

def main():
    n = int(input())
    V = defaultdict(list)
    used = dict()
    for _ in range(n):
        repost = input().split()
        user_1, user_2 = repost[2].lower(), repost[0].lower()
        V[user_1].append(user_2)
        V[user_2] = []
        used[user_1], used[user_2] = False, False
    dfs(AUTHOR, used, 1, V)
    
    print(max_length)
    
setrecursionlimit(10 ** 9)
threading.stack_size(2 ** 26)
thread = threading.Thread(target=main)
thread.start()
