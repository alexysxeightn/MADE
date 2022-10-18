#!/usr/bin/python3

import csv
import sys

cnt_prices, sum_prices = 0, 0
for row in csv.reader(sys.stdin, delimiter=','):
    if row[9].isdigit():
        sum_prices += float(row[9])
        cnt_prices += 1

print(cnt_prices, sum_prices/cnt_prices, sep='\t')