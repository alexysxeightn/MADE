#!/usr/bin/python3

import csv
import sys
from statistics import mean, variance

prices = []
for row in csv.reader(sys.stdin, delimiter=','):
    if row[9].isdigit():
        prices.append(float(row[9]))

print(len(prices), mean(prices), variance(prices), sep='\t')