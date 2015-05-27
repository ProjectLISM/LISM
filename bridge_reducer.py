#!/usr/bin/env python
"""
This code reduces input to generate all distinct items and their counts
"""

import sys
from ConfigParser import *

current_item = None
current_count = 0
item = None
config = ConfigParser()
config.read('config.ini')
for line in sys.stdin:
    line = line.strip()
    item,count = line.split(config.get('counting','delimiter'), 1)
    try:
        count = int(count)
    except ValueError:
        continue

    if current_item == item:
        current_count += count
    else:
        if current_item and current_count > 0:
		print "%s%s%s"%(current_item,config.get('counting','separator'),current_count)
        current_count = count
        current_item = item
if current_item == item and current_count > 0:
    print "%s%s%s"%(current_item,config.get('counting','separator'),current_count)
