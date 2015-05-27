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
		items (list): It contains items filtered by filt()
	"""
	lst = items.split(config.get('counting','delimiter'))
	print "%s%s%s"%(lst[0],config.get('counting','separator'),lst[1])
	print "%s%s%s"%(lst[1],config.get('counting','separator'),lst[0])

config = ConfigParser()
config.read('config.ini')
for line in sys.stdin:
    line = line.strip()
    items,count = line.split(config.get('counting','separator'),1)
    loop(items)
