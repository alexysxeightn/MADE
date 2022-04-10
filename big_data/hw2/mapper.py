#! /usr/bin/python

import sys
from random import randint

START_INDEX_FOR_PREFIX = 1
END_INDEX_FOR_PREFIX = 10 ** 5 - 1

for line in sys.stdin:
    prefix = randint(START_INDEX_FOR_PREFIX, END_INDEX_FOR_PREFIX)
    print(f'{prefix}_{line.strip()}')
