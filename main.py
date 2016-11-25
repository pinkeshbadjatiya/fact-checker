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

def check_fact(lis):
    for i, word in enumerate(lis):
        if KG.has_key(word):
            for j, word2 in enumerate(lis):
                if word2 in KG[word]:
                    return True
    return False


def process(TITLE, sentences, train):
    if len(sentences) < 1:
        return
        
    for sent in sentences:
        text = word_tokenize(sent.lower())
        tagged = nltk.pos_tag(text)
        lis = []
        for i, (word, tag) in enumerate(tagged):
            word = word.lower()
            if tag in KG_tag_set:
                if tag == 'PRP':
                    lis.append(TITLE)
                else:
                    lis.append(word)
        if(train==1):
            print(lis)
            insert_fact(lis)
        else:
            print(lis)
            return check_fact(lis)
            

def get_sentences(text):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    return sent_detector.tokenize(text.strip().lower())


def create_data():
    title = "Tom"
    data = ["Tom is a boy", "he likes to play football", "he is a good basket ball player"]
    return title, data


def main():
    if not TRAIN_DIR[-1] == "/":
        sys.exit(1)

    if CUSTOM_DATA:
        tit, data = create_data()
        process(tit, data, 1)
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
                    process(title, sentences, 1)
    
                    title = line
                    isTitle = False
                    pdb.set_trace()
                    sentences = []
    
                if REGEX_document_start.match(line) and not isTitle:
                    isTitle = True
                else:
                    sentences += get_sentences(line)
    
    sentence = "Start!"
    while(1):
        sentence = raw_input('Enter a query. Press Q to quit\n')
        if sentence == 'Q':
            break
        answer = process('',[sentence],0)
        print(answer)

if __name__ == "__main__":
    main()
    #pdb.set_trace()




