#!/usr/bin/env python

# based on: Natural Language Processing Specialization deeplearning.ai

import nltk
import re
import string
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def process_doc(text):
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text) #clean hyperlinks
    text = re.sub(r'\n-', '', text) # clean afbreekstreepjes
    tokens = nltk.word_tokenize(text) #tokenize
    stop_words = stopwords.words('dutch')
    keywords = [word for word in tokens if not word in stop_words and not word in string.punctuation]
    stemmer = PorterStemmer()
    text_stem = [stemmer.stem(word) for word in keywords]
    return text_stem


def build_freqs(docs, ys):
    """Build frequencies.
    Arguments:
        docs: a list of documents
        ys: an m x 1 array with the 'to keep or not' label of each document
    Returns:
        freqs: a dictionary mapping each (word, label) pair to its
        frequency

    example output:
        # "belangrijk" appears 98 times in the 'to keep' document
        ('belangrijk', 1.0): 98
    """
    # Convert np array to list since zip needs an iterable.
    yslist = np.squeeze(ys).tolist()

    # Start with an empty dictionary and populate it by looping over all docs
    # and over all processed words in each doc.
    freqs = {}
    for y, document in zip(yslist, docs):
        for word in process_doc(document):
            pair = (word, y)
            if pair in freqs:
                freqs[pair] += 1
            else:
                freqs[pair] = 1

    return freqs
