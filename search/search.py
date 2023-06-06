import lucene
import json
import os
from java.io import StringReader
from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from java.nio.file import Paths
from org.apache.lucene.document import Document, Field, FieldType, TextField, StringField


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
    filePath = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(os.path.realpath(__file__)))), "reddit_posts/ucr_1.json")
    print(os.listdir(os.path.dirname(os.path.realpath(os.path.dirname(os.path.realpath(__file__))))))
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
        doc.add(Field('title', title, TextField.TYPE_STORED)) #Indexed, tokenized, stored.
        doc.add(Field('body', body, TextField.TYPE_NOT_STORED)) #Indexed, tokenized, not stored
        doc.add(Field('id', id,  StringField.TYPE_STORED)) #Indexed, not tokenized, stored
        doc.add(Field('url', url, StringField.TYPE_STORED)) #Indexed, not tokenized, stored
        doc.add(Field('created_utc', str(created_utc), TextField.TYPE_STORED)) #Indexed, tokenized, stored.
        doc.add(Field('score', score, TextField.TYPE_STORED)) #Indexed, tokenized, stored.
        doc.add(Field('permalink', permalink, StringField.TYPE_STORED)) #Indexed, not tokenized, stored
        # doc.add(Field('comments', comments, metaType1))

        writer.addDocument(doc)
    
    writer.close()

index("reddit_posts", "indexed")