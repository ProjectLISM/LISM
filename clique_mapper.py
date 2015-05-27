#!/usr/bin/env python

import sys
from itertools import *
from ConfigParser import *

def list_to_string(lst):
    """
    This function converts list items into a single comma separated string
    Args:
        lst (list): list of items
    Returns: string (string): comma separated items into string
    """
    string = ''
    for i in range(0,len(lst)):
        if string == '':
            string = lst[i]
        else:
            string = string + config.get('counting','delimiter') + lst[i]
    return string

config = ConfigParser()
config.read('config.ini')
for line in sys.stdin:
    line = line.strip()
    try:
        node,item = line.split(config.get('counting','separator'),1)
    except ValueError:
        node = line
        item = ''
    items = item.split(config.get('counting','delimiter'))
    for i in range(0,len(items)):
        clique_lst = node.split(config.get('counting','delimiter'))
        clique_lst.append(items[i])
        clique_lst.sort()
        clique = list_to_string(clique_lst)
        string = ''
        for j in range(0,len(items)):
            if j is not i:
                if string == '':
                    string = items[j]
                else:
                    string = string + config.get('counting','delimiter') + items[j]
        print "%s%s%s"%(clique,config.get('counting','separator'),string)
