#!/usr/bin/env python3
import sys
import re

from lxml import etree

YEARS = (2010, 2016)

for line in sys.stdin:
    line = line.strip()

    if line.startswith('<row'):
        root = etree.fromstring(line)
        year = int(root.attrib.get('CreationDate')[:4])

        if year in YEARS:
            tags = root.attrib.get('Tags')
            if tags:
                tags = re.split('<|><|>', tags)[1:-1]
                for tag in tags:
                    print(year, tag, 1, sep='\t')
