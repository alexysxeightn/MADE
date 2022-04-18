#!/usr/bin/env python3
import sys


current_year, current_tag, current_count = None, None, 0

for line in sys.stdin:
    year, tag, counts = line.split('\t')
    counts = int(counts)

    if year == current_year and tag == current_tag:
        current_count += counts
    else:
        if current_year and current_tag:
            print(current_year, current_tag, current_count, sep='\t')
        current_year, current_tag, current_count = year, tag, counts

if current_year and current_tag:
    print(current_year, current_tag, current_count, sep='\t')
