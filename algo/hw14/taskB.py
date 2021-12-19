def z_function_with_print(s):
    n, left, right = len(s), 0, 0
    z = [0] * n
    for i in range(1, n):
        z[i] = max(0, min(right - i, z[i - left]))
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
        print(z[i], end = ' ')
    
z_function_with_print(input())
