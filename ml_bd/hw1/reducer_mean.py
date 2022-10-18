#!/usr/bin/python3

import sys

mean_all, cnt_all = 0, 0

for line in sys.stdin:
    cnt_prices, mean_prices = map(float, line.strip().split())

    mean_all = (cnt_prices * mean_prices + cnt_all * mean_all) / (cnt_prices + cnt_all)
    cnt_all += cnt_prices

print(mean_all)