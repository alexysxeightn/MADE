import time
from time import sleep


def sleep_add(x, y):
	sleep(3)
	z = x + y
	return z


def sleep_multiply(x, y):
	time.sleep(5)
	z = x * y
	return z


def deepest_sleep_function(x, y):
	z = sleep_add(x, y)
	w = sleep_multiply(x, y)
	outcome = z + w
	return outcome
