INF = 10 ** 9

class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w
        
class GraphNode:
    def __init__(self, root, num_of_edges, w):
        self.root = root
        self.num_of_edges = num_of_edges
        self.w = w

def dfs(v, used, graph, zero_strategy):
    if not used[v]:
        used[v] = True
        for u in graph[v]:
            if 0 == u.w or not zero_strategy:
                dfs(u.root, used, graph, zero_strategy)
    
def out_dfs(v, used, graph, out_time):
    if not used[v]:
        used[v] = True
        for u in graph[v]:
            if 0 == u.w:
                out_dfs(u.root, used, graph, out_time)
        out_time.insert(0, v)

def dfs_color(v, color, cur, graph):
    if 0 == color[v]:
        color[v] = cur
        for u in graph[v]:
            if 0 == u.w:
                dfs_color(u.root, color, cur, graph)
                
def exist_MST(graph, n, zero_strategy):
    global root
    used = [False] * n
    dfs(root, used, graph, zero_strategy)
    for x in used:
        if not x:
            return False
    return True

def get_reversed_graph(graph, n):
    reversed_graph = [[] for _ in range(n)]
    for v in range(n):
        for u in graph[v]:
            reversed_graph[u.root].append(GraphNode(v, u.num_of_edges, u.w))
    return reversed_graph

def get_reversed_condensation(graph, edges, n):
    global root
    used = [False] * n
    out_time = []
    color = [0] * n
    cur_color = 1
    
    out_dfs(root, used, graph, out_time)
    for v in range(n):
        out_dfs(v, used, graph, out_time)
    
    condensation = get_reversed_graph(graph, n)
    
    for v in out_time:
        if 0 == color[v]:
            dfs_color(v, color, cur_color, condensation)
            cur_color += 1
    
    root = color[root]
    root -= 1
    cur_color -= 1
    
    reversed_condensation = [[] for _ in range(cur_color)]
    
    for v in range(n):
        for u in graph[v]:
            if color[v] != color[u.root]:
                reversed_condensation[color[v] - 1].append(GraphNode(
                    color[u.root] - 1,
                    u.num_of_edges,
                    u.w
                ))
    
    return reversed_condensation, cur_color
    
def find_MST(graph, edges, n):
    global answer
    while True:
        for v in range(n):
            min_edge = INF
            
            for u in graph[v]:
                min_edge = min(min_edge, u.w)
                
            for u in graph[v]:
                u.w -= min_edge
                
            if v != root:
                answer += min_edge
        if exist_MST(get_reversed_graph(graph, n), n, True):
            break
        graph, n = get_reversed_condensation(graph, edges, n)
        
root = 0
answer = 0

n, m = map(int, input().split())
    
edges = [None] * m
graph = [[] for _ in range(n)]
inverse_graph = [[] for _ in range(n)]
for i in range(m):
    a, b, w = map(int, input().split())
    a, b = a - 1, b - 1
    edges[i] = Edge(a, b, w)
    graph[a].append(GraphNode(b, i, w))
    inverse_graph[b].append(GraphNode(a, i, w))
    
if exist_MST(graph, n, False):
    print('YES')
    find_MST(inverse_graph, edges, n)
    print(answer)
else:
    print('NO')
