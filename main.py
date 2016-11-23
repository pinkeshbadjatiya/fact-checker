#!/usr/bin/python

from nltk.tokenize import word_tokenize
import nltk
import pdb
import os
import re
import sys

TRAIN_DIR = "./wiki_files/"
CUSTOM_DATA = True

KG_tag_set = ['NN', 'NNP', 'NNPS', 'PRP']
KG = {}


REGEX_document_start = re.compile(r'<doc *(id="([0-9]{1,})")? *(url=".*")? *(title=".*")?>')


def insert_fact(lis):
    for i, word in enumerate(lis):
        if not i:
            continue

        prev = lis[i-1]
        if not KG.has_key(prev):
            KG[prev] = []
        KG[prev].append(word)


def process(TITLE, sentences):
    if len(sentences) <= 1:
        return
        
    for sent in sentences:
        text = word_tokenize(sent)
        tagged = nltk.pos_tag(text)
        lis = []
        for i, (word, tag) in enumerate(tagged):
            if tag in KG_tag_set:
                if tag == 'PRP':
                    lis.append(TITLE)
                else:
                    lis.append(word)
        insert_fact(lis)


def get_sentences(text):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    return sent_detector.tokenize(text.strip())


def create_data():
    title = "Tom"
    data = ["Tom is a boy", "He likes to play football", "He is a good basket ball player"]
    return title, data


def main():
    if not TRAIN_DIR[-1] == "/":
        sys.exit(1)

    if CUSTOM_DATA:
        tit, data = create_data()
        process(tit, data)
    else:
        for f in os.listdir(TRAIN_DIR):
            print "Creating Knowledge GRAPH"
            # Get title
            sentences = []
            text = open(TRAIN_DIR + f).readlines()
            isTitle, title = False, ""
            for line in text:
                line = line.decode("UTF-8")
                if isTitle:
                    print title
                    process(title, sentences)
    
                    title = line
                    isTitle = False
                    pdb.set_trace()
                    sentences = []
    
                if REGEX_document_start.match(line) and not isTitle:
                    isTitle = True
                else:
                    sentences += get_sentences(line)


if __name__ == "__main__":
    main()
    pdb.set_trace()




