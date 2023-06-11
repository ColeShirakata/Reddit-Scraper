from flask import Flask, render_template, request, jsonify
import lucene
import os
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import FSDirectory
from java.nio.file import Paths

app = Flask(__name__)

@app.route("/")
def index(name=None):
    return render_template('index.html', name=name)

@app.route("/css")
def css():
    return render_template('styles.css')

@app.route("/search", methods=["POST"])
def search():

    lucene.getVMEnv().attachCurrentThread()

    current_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "indexed")
    
    index_dir = FSDirectory.open(Paths.get(current_directory))
    index_reader = DirectoryReader.open(index_dir)
    index_searcher = IndexSearcher(index_reader)
    analyzer = StandardAnalyzer()

    query = request.form.get("query")
    ordering = request.form.get("ordering")
    rank_by = request.form.get("rank_by")
    
    query_parser = QueryParser("title", analyzer)
    lucene_query = query_parser.parse(query)
    
    top_docs = index_searcher.search(lucene_query, 10)
    
    results = []
    
    for score_doc in top_docs.scoreDocs:
        doc = index_searcher.doc(score_doc.doc)
        title = doc.get("title")
        score = score_doc.score
        result = {
            "title": title,
            "score": score
        }
        results.append(result)

    return jsonify(results)

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

if __name__ == "__main__":
    app.run()
