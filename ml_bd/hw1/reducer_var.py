#!/usr/bin/python3

import sys

var_all, mean_all, cnt_all = 0, 0, 0

for line in sys.stdin:
    cnt_prices, mean_prices, var_prices = map(float, line.strip().split())

    var_all = (cnt_prices * var_prices + cnt_all * var_all) / (cnt_prices + cnt_all)
    var_all += cnt_prices * cnt_all * ((mean_prices - mean_all) / (cnt_prices + cnt_all)) ** 2

    mean_all = (cnt_prices * mean_prices + cnt_all * mean_all) / (cnt_prices + cnt_all)
    cnt_all += cnt_prices

print(var_all)