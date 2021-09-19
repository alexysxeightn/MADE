n = int(input())
L = list(map(int, input().split()))
     
count_of_inverse = 0
     
def merge(left_arr, right_arr):
    global count_of_inverse
        
    n, m = len(left_arr), len(right_arr)
    i, j = 0, 0
    merge_arr = [0] * (n + m)
        
    while i + j < n + m:
        if j == m or (i < n and left_arr[i] < right_arr[j]):
            merge_arr[i + j] = left_arr[i]
            i += 1
        else:
            merge_arr[i + j] = right_arr[j]
            count_of_inverse += n - i
            j += 1
        
    return merge_arr
     
def merge_sort(arr):
    n = len(arr)
    if n == 1:
        return arr
            
    median = n // 2
    left_arr, right_arr = arr[:median], arr[median:]
    left_arr, right_arr = merge_sort(left_arr), merge_sort(right_arr)
        
    return merge(left_arr, right_arr)
     
L = merge_sort(L)
     
print(count_of_inverse)
