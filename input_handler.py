import nltk
from nltk.stem.porter import PorterStemmer
import numpy

def tokenize(input=str):
    return nltk.word_tokenize(input)

def stem(word=str):
    return PorterStemmer().stem(word.lower())
    
def word_bag(token_input, all_words):
    token_input = [stem(word) for word in token_input]
    bag = numpy.zeros(len(all_words), dtype=numpy.float32)

    for idx, w in enumerate(all_words):
        if w in token_input:
            bag[idx] = 1.0

    return bag