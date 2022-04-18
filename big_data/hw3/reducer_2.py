#!/usr/bin/env python3
import sys


TOP = 10
years = {
    '2010': 0,
    '2016': 0,
}

for line in sys.stdin:
    year, tag, counts = line.strip().split('\t')
    if not (years.get(year) is None) and years[year] < TOP:
        print(year, tag, counts, sep='\t')
        years[year] += 1
    else:
        continue
