import lucene
from java.io import StringReader
from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

test = "this is how we do it."
tokenizer = StandardTokenizer()
tokenizer.setReader(StringReader(test))
tokenizer.setReader(StringReader(test))

charTermAttrib = tokenizer.getAttribute(CharTermAttribute.class_)
tokenizer.reset()

tokens = []

while tokenizer.incrementToken():
    tokens.append(charTermAttrib.toString())

print(tokens)