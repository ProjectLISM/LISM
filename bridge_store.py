from redis import *
from ConfigParser import *

r_server = Redis('localhost')
r_server.delete('bridge')
config = ConfigParser()
config.read('config.ini')
f = open('bridge','r')
for line in f:
	line = line.replace('\n','')
	line = line.replace('\t','')
	line = line.replace('\r','')
	items,count = line.split(config.get('counting','separator'),1)
	r_server.hset('bridge',items,count)
