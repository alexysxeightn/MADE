from random import randint

def split(array, left, right, x):
	m = left
	for i in range(left, right):
		if array[i] < x:
			array[i], array[m] = array[m], array[i]
			m += 1
	return m

def find(array, k, left, right):
	if right - left == 1:
		return array[k]
	x = array[randint(left, right - 1)]
	m = split(array, left, right, x)
	if k < m:
		return find(array, k, left, m)
	else:
		return find(array, k, m, right)

n = int(input())
clones = [*map(int, input().split())]
m = int(input())
for _ in range(m):
	i, j, k = map(int, input().split())
	print(find(clones[i - 1:j], k - 1, 0, j - i + 1))
