import lucene
import json
import os
from java.io import StringReader
from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import FSDirectory
from java.nio.file import Paths
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory


def index(input_dir, dir):
	lucene.initVM(vmargs=['-Djava.awt.headless=true'])

	# test = "this is how we do it."
	# tokenizer = StandardTokenizer()
	# tokenizer.setReader(StringReader(test))
	# tokenizer.setReader(StringReader(test))

	# charTermAttrib = tokenizer.getAttribute(CharTermAttribute.class_)
	# tokenizer.reset()

	# tokens = []

	# while tokenizer.incrementToken():
	#     tokens.append(charTermAttrib.toString())

	# print(tokens)
	store = FSDirectory.open(Paths.get(dir))
	analyzer = StandardAnalyzer()
	config = IndexWriterConfig(analyzer)
	config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
	writer = IndexWriter(store, config)

	# indexed, not tokenized, stored (example: reddit username)
	metaType1 = FieldType()
	metaType1.setStored(True)
	metaType1.setTokenized(False)
	metaType1.setIndexOptions(IndexOptions.DOCS)

	# indexed, tokenized, stored (example: Title, abstract)
	metaType2 = FieldType()
	metaType2.setStored(True)
	metaType2.setTokenized(True)
	metaType2.setIndexOptions(IndexOptions.DOCS)

	# indexed, tokenized, not stored (example: Body)
	metaType3 = FieldType()
	metaType3.setStored(False)
	metaType3.setTokenized(True)
	metaType3.setIndexOptions(IndexOptions.DOCS)

	print(os.listdir(os.path.dirname(os.path.realpath(__file__))))
	filePath = os.path.join(
	 os.path.dirname(os.path.realpath(os.path.dirname(
	  os.path.realpath(__file__)))), "reddit_posts/ucr_1.json")
	print(
	 os.listdir(
	  os.path.dirname(
	   os.path.realpath(os.path.dirname(os.path.realpath(__file__))))))
	with open(filePath, 'r') as handle:
		text_data = handle.read()
		text_data = '[' + text_data[1:] + ']'
		json_data = json.loads(text_data)

	for dictionary in json_data:
		# print(dict.get("name"))
		title = dictionary.get("title")
		body = dictionary.get("selftext")
		id = dictionary.get("id")
		url = dictionary.get("url")
		created_utc = dictionary.get("created_utc")
		score = dictionary.get("score")
		permalink = dictionary.get("permalink")
		# comments = dictionary.get("comments")
		# URLs = dictionary.get("URLs")
		# html_title = dictionary.get("html_title")

		doc = Document()
		doc.add(Field('title', title,
		              TextField.TYPE_STORED))  #Indexed, tokenized, stored.
		doc.add(Field('body', body,
		              TextField.TYPE_NOT_STORED))  #Indexed, tokenized, not stored
		doc.add(Field('id', id,
		              StringField.TYPE_STORED))  #Indexed, not tokenized, stored
		doc.add(Field('url', url,
		              StringField.TYPE_STORED))  #Indexed, not tokenized, stored
		doc.add(Field('created_utc', str(created_utc),
		              TextField.TYPE_STORED))  #Indexed, tokenized, stored.
		doc.add(Field('score', score,
		              TextField.TYPE_STORED))  #Indexed, tokenized, stored.
		doc.add(Field('permalink', permalink,
		              StringField.TYPE_STORED))  #Indexed, not tokenized, stored
		# doc.add(Field('comments', comments, metaType1))

		writer.addDocument(doc)

	writer.close()


index("reddit_posts", "indexed")

############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################


def perform_search(query, ordering='relevance'):
	lucene.initVM(vmargs=['-Djava.awt.headless=true'])
	store = FSDirectory.open(Paths.get("indexed"))
	reader = DirectoryReader.open(store)
	searcher = IndexSearcher(reader)
	analyzer = StandardAnalyzer()

	lucene_query = QueryParser("body", analyzer).parse(query)
	hits = searcher.search(lucene_query, 10).scoreDocs

	results = []
	for hit in hits:
		doc = searcher.doc(hit.doc)
		result = {
		 'id': doc.get('id'),
		 'title': doc.get('title'),
		 'url': doc.get('url'),
		 'created_utc': doc.get('created_utc'),
		 'score': doc.get('score'),
		 'permalink': doc.get('permalink'),
		 'match_score': hit.score  # we get the match_score directly from the hit
		}
		results.append(result)

	# sorting the results based on the provided ordering
	if ordering == 'votes':
		results.sort(key=lambda x: int(x['score']),
		             reverse=True)  # assuming score is a string of integer
	elif ordering == 'time':
		results.sort(key=lambda x: x['created_utc'], reverse=True)
	elif ordering == 'relevance':
		results.sort(key=lambda x: x['match_score'], reverse=True)
	elif ordering == 'combination':
		# You can define your own combination logic here. As an example:
		results.sort(key=lambda x: (0.5 * x['match_score']) +
		             (0.3 * int(x['score'])) + (0.2 * float(x['created_utc'])),
		             reverse=True)
	else:  # Default to sorting by relevance
		results.sort(key=lambda x: x['match_score'], reverse=True)

	return results


#For 'votes' ordering, it assumes that the 'score' field in your document is a string representation of an integer. If it's already an integer, you won't need the int() conversion.
#For 'time' ordering, it assumes that 'created_utc' is a sortable value. Depending on your data, you may need to convert it to a proper datetime or timestamp for accurate sorting.
#For 'combination' ordering, it calculates a weighted combination of relevance ('match_score'), votes ('score'), and time ('created_utc'). You may need to adjust these weights and fields depending on your data and requirements.
#The 'match_score' field is taken directly from the hit.score value provided by PyLucene, which represents the relevance of the document to the query.


def perform_pagerank(query, ordering='relevance'):
	# Perform PageRank-based search logic here... For now, return dummy data:
	return [{
	 'title': 'Dummy Title 1',
	 'score': 'Dummy Score 1',
	 'url': 'Dummy URL 1',
	 'created_utc': 'Dummy Time 1'
	}, {
	 'title': 'Dummy Title 2',
	 'score': 'Dummy Score 2',
	 'url': 'Dummy URL 2',
	 'created_utc': 'Dummy Time 2'
	}, {
	 'title': 'Dummy Title 3',
	 'score': 'Dummy Score 3',
	 'url': 'Dummy URL 3',
	 'created_utc': 'Dummy Time 3'
	}]
