def lower_bound(array, n, x):
    left, right = -1, n - 1
    while left < right - 1:
        m = (left + right) // 2
        if x <= array[m]:
            right = m
        else:
            left = m
    return right

n, k = map(int, input().split())
array = [*map(int, input().split())]
queries = [*map(int, input().split())]

for query in queries:

    lb, ub = lower_bound(array, n, query), lower_bound(array, n, query + 1)
    
    if array[lb] != query and lb != 0:
        lb -= 1
    
    if abs(array[lb] - query) <= abs(array[ub] - query):
        print(array[lb])
    else:
        print(array[ub])
