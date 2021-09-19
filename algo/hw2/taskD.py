LEN_ALPHABET = 26
     
n, m = map(int, input().split())
s, t = str(input()), str(input())
     
cnt = [0] * LEN_ALPHABET
result = 0
     
for i in range(m):
    cnt[ord(t[i]) - ord('a')] += 1
        
i, j = 0, 0
while j < n:
    if cnt[ord(s[j]) - ord('a')]:
        cnt[ord(s[j]) - ord('a')] -= 1
        j += 1
        result += j - i
    else:
        cnt[ord(s[i]) - ord('a')] += 1
        i += 1
     
print(result)
