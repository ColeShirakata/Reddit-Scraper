import lucene
import os

from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import FSDirectory
from java.nio.file import Paths

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

def index_query(query):
    current_directory = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(os.path.realpath(__file__)))), "indexed")
    index_dir = FSDirectory.open(Paths.get(current_directory))
    index_reader = DirectoryReader.open(index_dir)

    index_searcher = IndexSearcher(index_reader)

    query_string = query

    analyzer = StandardAnalyzer()

    query_parser = QueryParser("title", analyzer)
    query = query_parser.parse(query_string)

    top_docs = index_searcher.search(query, 10)

    for score_doc in top_docs.scoreDocs:
        doc = index_searcher.doc(score_doc.doc)
        print(doc.get('title'))
        print(score_doc.score)

    index_reader.close()

while(True):
    user_query = str(input("\nEnter your query: "))

    if(user_query == "0"):
        break

    else:
        index_query(user_query)