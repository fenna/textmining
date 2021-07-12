#!/usr/bin/env python3

"""
This code is based on the Textrank algorithm for text summaries
1. The document is read and split into sentences.
2. Stop words and weird characters are removed.
3. Each sentence is converted into a vector (word embedding).
4. A matrix of m x m sentences is created in which the similarity is calculated between the sentence vectors using cosine similarity
5. The matrix is converted to a graph network where the sentences are the nodes and the similarity score is a connection.
6. The ranking order is calculated based on the scores and the location in the network.
7. The N-highest sentences are selected for the summary. 
"""


__source__ = "https://github.com/edubey/text-summarizer"

#import libraries
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx



def get_cleaned_sentences(file_name):
    """generate clean sentences from the file"""
    file = open(file_name, "r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    
    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(file_name, top_n=5):
    stop_words = stopwords.words('dutch')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences =  get_cleaned_sentences(file_name)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))
    
    # Step 5 - output the summarize text
    return ". ".join(summarize_text)
    