import lucene
import sys
from ConfigParser import *
from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexWriter, Version

config = ConfigParser()
config.read('config.ini')
#f = open('clique','r')
f = open(str(sys.argv[1]),'r')
if __name__ == "__main__":
    lucene.initVM()
    indexDir = "/tmp/luceneindex"
    dir = SimpleFSDirectory(File(indexDir))
    analyzer = StandardAnalyzer(lucene.Version.LUCENE_CURRENT)
    writer = IndexWriter(dir, analyzer, True, IndexWriter.MaxFieldLength(512))

    print >> sys.stderr, "Currently there are %d documents in the index..." % writer.numDocs()

    print >> sys.stderr, "Reading lines from sys.stdin..."
    for line in f:
        line = line.replace('\t','')
        line = line.replace('\r','')
        line = line.replace('\n','')
        line = line.replace(config.get('counting','separator'),'')
        doc = Document()
        doc.add(Field("text", line, Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc)

    print >> sys.stderr, "Indexed lines from stdin (%d documents in index)" % (writer.numDocs())
    print >> sys.stderr, "About to optimize index of %d documents..." % writer.numDocs()
    writer.optimize()
    print >> sys.stderr, "...done optimizing index of %d documents" % writer.numDocs()
    print >> sys.stderr, "Closing index of %d documents..." % writer.numDocs()
    writer.close()
    print >> sys.stderr, "...done closing index of %d documents" % writer.numDocs()
