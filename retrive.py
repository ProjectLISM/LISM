import lucene
import sys
from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexSearcher, Version, QueryParser
from redis import *
from ConfigParser import *

def recommend(top,search):
	f = open('/home/shreemay/Reco.html','w')
	f.write('<HTML><HEAD><TITLE></TITLE></HEAD><BODY>Product<BR><IMG SRC = "/home/shreemay/Images/')
	temp = search.replace(' ','')
	f.write(temp)
	f.write('.jpg" HEIGHT = 200 WIDTH = 200><BR>')
	f.write(search + '<BR>Recommendations<BR>')
	for item in top:
		string = '<IMG SRC = "/home/shreemay/Images/'
		temp = item.replace(' ','')
		string = string + temp + '.jpg" HEIGHT = 200 WIDTH = 200>'
		f.write(string)
		f.write(item)

config = ConfigParser()
config.read('config.ini')
r_server = Redis('localhost')
lst = []
search = str(sys.argv[1])
if __name__ == "__main__":
    lucene.initVM()
    indexDir = "/tmp/luceneindex"
    dir = SimpleFSDirectory(File(indexDir))
    analyzer = StandardAnalyzer(Version.LUCENE_30)
    searcher = IndexSearcher(dir)

    query = QueryParser(lucene.Version.LUCENE_CURRENT, "text", analyzer).parse(search)
    MAX = 1000
    hits = searcher.search(query, MAX)

    #print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)

    for hit in hits.scoreDocs:
        if hit.score >= 0.0:
            #print hit.score, hit.doc, hit.toString()
            doc = searcher.doc(hit.doc)
            #print doc.get("text").encode("utf-8")
            items = doc.get("text").encode("utf-8").split(config.get('counting','delimiter'))
            for item in items:
                if item == search:
                    pass
                elif item not in lst:
                    lst.append(item)
reco = []
reco2 = []
for i in range(0,len(lst)):
	if r_server.hexists('pair',search + config.get('counting','delimiter') + lst[i]):
		reco.append(str(lst[i]))
		reco2.append(float(r_server.hget('pair',search + config.get('counting','delimiter') + lst[i])))
		if r_server.hexists('bridge',str(lst[i])):
			reco2[len(reco2)-1] *= float(config.get('recommendation','bridge'))
	elif r_server.hexists('pair',lst[i] + config.get('counting','delimiter') + search):
		reco.append(str(lst[i]))
		reco2.append(float(r_server.hget('pair',lst[i] + config.get('counting','delimiter') + search)))
		if r_server.hexists('bridge',str(lst[i])):
			reco2[len(reco2)-1] *= float(config.get('recommendation','bridge'))
top = []
for i in range(0,len(reco)):
	if len(top) < int(config.get('recommendation','products')):
		top.append(reco[i])
	else:
		minimum = 1.0
		index = -1
		for j in range(0,len(top)):
			ind = reco.index(top[j])
			if reco2[ind] < minimum:
				index = j
				minimum = reco2[ind]
		if index is not -1 and reco2[ind] > minimum:
			top[index] = reco[i]
print top
#recommend(top,search)
