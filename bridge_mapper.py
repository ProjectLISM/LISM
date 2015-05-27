#!/usr/bin/env python
"""
This code gives all occurences of single items
"""
import sys
from ConfigParser import *


def loop(items):
	"""
	This function loops each item and append count to one and prints it into file by hadoop.
	Args:
		items (List): It contains items filtered by filt()
	"""
	for item in items:
		print '%s%s%s' % (item,config.get('counting','delimiter'),1)

config = ConfigParser()
config.read('config.ini')
for line in sys.stdin:
    line = line.strip()
    item,count = line.split(config.get('counting','separator'),1)
    items = item.split(config.get('counting','delimiter'))
    loop(items)
