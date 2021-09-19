M = 100 + 1
cnt = [0] * M
array = [*map(int, input().split())]

for i in array:
    cnt[i] += 1

i = 0
for j in range(M):
    while cnt[j] > 0:
        array[i] = j
        i += 1
        cnt[j] -= 1
        
print(*array)
