LEN_ALPHABET = 26
     
n, m, k = map(int, input().split())
array = []
for _ in range(n):
    array.append(str(input()))
        
for i in range(k):
    cnt = [0] * LEN_ALPHABET
    p = [0] * LEN_ALPHABET
    array_sorted = [0] * n
        
    for j in range(n):
        cnt[ord(array[j][m - i - 1]) - ord('a')] += 1
     
    for j in range(1, LEN_ALPHABET):
        p[j] = p[j - 1] + cnt[j - 1]
     
    for j in range(n):
        array_sorted[p[ord(array[j][m - i - 1]) - ord('a')]] = array[j]
        p[ord(array[j][m - i - 1]) - ord('a')] += 1
        
    array = array_sorted.copy()
        
print(*array, sep = '\n')
