import glob
import os
import spacy
from itertools import chain
from collections import Counter
import matplotlib.pyplot as plt
plt.style.use('ggplot')

import numpy as np


text=""
result=[]

def open_folder(way):
    '''Open files in directory and subdirectory'''
    print(way)
    all_text=""
    for x in os.walk(way):
        for y in glob.glob(os.path.join(x[0], '*.xml')):
            print(y)
            result.append(y)
            file_input = open(y, "r", encoding="utf8")
            all_text+= file_input.read() + " "
            all_text.replace("\n", " ")
            #print(all_text)
    return all_text

def open_file(way):
    print(way)
    all_text=""
    file_input = open(way, "r", encoding="utf8")
    all_text = file_input.read()
    all_text.replace("\n", " ")
    #print(all_text)
    return all_text
                
def doc(t):
    '''Tokenizer'''
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length=5000000
    doc = nlp(t)
    """for token in doc:
        print(token.text)"""
    return doc

def save_tokens(path, liste):
    print(path)
    f = open(path + "\\tokens.txt", "w")
    for token in liste:
        f.write(token.text + "\n")

def save_pos(path, liste):
    print(path)
    f = open(path + "\\pos.txt", "w")
    for token in liste:
        f.write(token.pos_ + "\n")
    f.close()
    f=open(path + "\\tokens_and_pos.txt", "w")
    for token in liste:
        f.write(token.text + "  " + token.pos_ + "\n")
    f.close()

def save_sentences(path, liste):
    print(path)
    f = open(path + "\\sentences.txt", "w")
    sentences = [sent.text + "\n" for sent in liste.sents]
    for i in range(len(sentences)):
        f.write(sentences[i] + "\n")
    f.close

def counter_pos(liste):
    tags=["ADJ", "ADP", "ADV", "AUX", "CONJ", "DET", "INTJ", "NOUN", "NUM", "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB", "X"]
    counter=[]
    for i in range(len(tags)):
        counter1=[tags[i], 0]
        counter.append(counter1)
    for token in liste:
        for i in range(len(counter)):
            if token.pos_ == counter[i][0]:
                counter[i][1]+=1
    return counter

def counter_ios(liste):
    tags=["SPATIAL_ENTITY", "PLACE", "MOTION", "LOCATION", "SIGNAL", "QSLINK", "OLINK"]
    counter=[]
    for i in range(len(tags)):
       counter1=[tags[i], 0]
       counter.append(counter1)
    for token in liste:
        for i in range(len(counter)):
            if token.text == counter[i][0]:
                counter[i][1]+=1
    return counter

def counter_qslink(liste):
    tags=["DC", "EC", "PO", "EQ", "TPP", "NTTP", "IN"]
    counter=[]
    for i in range(len(tags)):
        tags[i]='relType="' + tags[i]
    print(tags)
    for i in range(len(tags)):
       counter1=[tags[i], 0]
       counter.append(counter1)
    for token in liste:
        for i in range(len(counter)):
            if token.text == counter[i][0]:
                counter[i][1]+=1
    return counter

def sentence_length(liste):
    counter_len=[]
    sentences = [sent.text + "\n" for sent in liste.sents]
    for i in range(len(sentences)):
        counter_len.append(len(sentences[i]))
    counter_len.sort()
    counter_length=Counter(counter_len)
    dictionary = Counter(counter_len)
    plt.bar(list(dictionary.keys()), dictionary.values(), color='red')
    plt.xlabel('Anzahl Wörter')
    plt.ylabel('Anzahl Vorkommen')
    plt.show()

def do_this():
    choice=""
    way=""
    while choice!="ORDNER" and choice!="DOKUMENT":
        choice=input("ORDNER oder DOKUMENT auswerten?")
        if choice == "ORDNER":
            way=input("Geben Sie den Dateipfad an:")
            all_text = open_folder(way)
        elif choice == "DOKUMENT":
            way=input("Geben Sie den Dateipfad an:")
            print(way)
            all_text=open_file(way)
        else:
            print("Bitte treffen Sie eine gültige Wahl.")
            continue
    print("3")
    document = doc(all_text)
    print("4")
    """
    while choice !="NEIN":
        choice=input("Möchten Sie Ihre Ergebnisse abspeichern? JA NEIN")
        if choice=="JA":
            path=input("Geben Sie einen Speicherordner an:")
            save_tokens(path, document)
            save_pos(path, document)
    """
    #counterpos=counter_pos(document)
    #print(counterpos)
    #counterios=counter_ios(document)
    #print(counterios)
    #counterqs=counter_qslink(document)
    #print(counterqs)
    sentence_length(document)
    print("#################################################################################")
    print(document)
    
            
    
    



do_this()
#save dictionarry with x y or as nested list
#how many words in sentence how often? x=length, y:how often 0-???
#which links with which preposition
#top 5 motion verbs and how often

