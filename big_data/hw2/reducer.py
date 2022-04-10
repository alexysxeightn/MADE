#! /usr/bin/python

import sys
from random import randint

NOT_EOF = True
while NOT_EOF:
    string = []
    for _ in range(randint(1, 5)):
        line = sys.stdin.readline().strip()
        if line == "":
            NOT_EOF = False
            break
        string.append(line.split('_')[1])
    if len(string) > 0:
        print(','.join(string), sep='')
