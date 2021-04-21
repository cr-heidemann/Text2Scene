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
            #result.append(y)
            file_input = open(y, "r", encoding="utf8")
            lines = open(y, "r", encoding="utf8").read().splitlines()
            print(lines)
            result.append(lines)
            all_text+= file_input.read() + " "
            #all_text.replace("\n", " ")
    #print(all_text)
    return all_text, result

def open_file(way):
    print(way)
    all_text=""
    file_input = open(way, "r", encoding="utf8")
    lines = open(way, "r", encoding="utf8").read().splitlines()
    result=[lines]
    all_text = file_input.read()
    all_text.replace("\n", " ")
    #print(all_text)
    return all_text, result
                
def doc(t):
    '''Tokenizer'''
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length=5000000
    doc = nlp(t)
    """for token in doc:
        print(token.text)"""
    return doc

def make_sentences(liste):
    print(liste)
    print(liste.sents)
    sentences = [sent.text for sent in range(len(liste.sents))]
    return sentences

def save_tokens(path, liste):
    print(path)
    f = open(path + "\\tokens.txt", "w",encoding="utf8")
    for token in liste:
        f.write(token.text + "\n")

def save_pos(path, liste):
    print(path)
    f = open(path + "\\pos.txt", "w", encoding="utf8")
    for token in liste:
        f.write(token.pos_ + "\n")
    f.close()
    f=open(path + "\\tokens_and_pos.txt", "w", encoding="utf8")
    for token in liste:
        f.write(token.text + "  " + token.pos_ + "\n")
    f.close()

def save_sentences(path, liste):
    print(path)
    f = open(path + "\\sentences.txt", "w", encoding="utf8")
    sentences = make_sentences(liste)
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
    plt.bar(list(dictionary.keys()), dictionary.values(), color="blue")
    plt.xlabel("Anzahl Wörter")
    plt.ylabel("Anzahl Vorkommen")
    plt.show()

def extract(liste, d, i,  s, e):
    s= liste[d][i].find(s) + len(s)
    e=liste[d][i].find(e)
    word=liste[d][i][s:e]
    return word

def prepositions(sentences, liste):
    s_id={}
    qs_s=[]
    o_s=[]
    lines = sentences
    for doc in range(len(lines)):
        for line in range(len(lines[doc])):
        # each doc is list of string in list, so each string is a line
        #if line contains <SPATIAL_SIGNAL, save id and text
            """if "<SPATIAL_SIGNAL" in lines[line]:
            start= lines[line].find('id="') + len('id="')
            end=lines[line].find('" start="')
            key=lines[line][start:end]
            start= lines[line].find('text="') + len('text="')
            end=lines[line].find('" cluster="')
            value=lines[line][start:end]
            s_id[key]=value"""
            if "<SPATIAL_SIGNAL" in lines[doc][line]:
                key=extract(lines, doc, line, 'id="', '" start="')
                value=extract(lines, doc, line, 'text="', '" cluster="')
                s_id[key]=value
            if "<QSLINK" in lines[doc][line]:
                word=extract(lines, doc, line, 'trigger="', '" comment="')
                qs_s.append(word)
            if "<OLINK" in lines[doc][line]:
                word=extract(lines,doc, line, 'trigger="', '" frame_type="')
                o_s.append(word)
    qs_s[:] = [i for i in qs_s if i]
    o_s[:] = [i for i in o_s if i]
    # for each id in the lists, repalce it with value(text)
    qs_s = [s_id.get(i, i) for i in qs_s]
    qs_s=Counter(qs_s)
    o_s = [s_id.get(i, i) for i in o_s]
    o_s=Counter(o_s)
    return qs_s, o_s

def motion(sentences, liste):
    verbs=[]
    lines = sentences
    for doc in range(len(lines)):
        for line in range(len(lines[doc])):
            if "<MOTION id" in lines[doc][line]:
                word=extract(lines, doc, line, 'text="', '" domain="')
                verbs.append(word)
    verbs = Counter(verbs)
    verbs=verbs.most_common(5)
    return verbs

                   
def do_this():
    choice=""
    way=""
    document=""
    sentences=[]
    print("1")
    while choice!="ORDNER" and choice!="DOKUMENT":
        choice=input("ORDNER oder DOKUMENT auswerten?")
        if choice == "ORDNER":
            way=input("Geben Sie den Dateipfad an:")
            all_text, sentences = open_folder(way)
            document = doc(all_text)
        elif choice == "DOKUMENT":
            way=input("Geben Sie den Dateipfad an:")
            #print(way)
            all_text, sentences=open_file(way)
            document = doc(all_text)
        else:
            print("Bitte treffen Sie eine gültige Wahl.")
            continue
    print("2")
    print(sentences)
    print("3")
    
    while choice !="NEIN" and choice !="JA":
        choice=input("Möchten Sie Ihre Ergebnisse abspeichern? JA NEIN")
        if choice=="JA":
            path=input("Geben Sie einen Speicherordner an:")
            save_tokens(path, document)
            save_pos(path, document)
            save_sentences(path,document)
    
    #counterpos=counter_pos(document)
    #print(counterpos)
    #counterios=counter_ios(document)
    #print(counterios)
    #counterqs=counter_qslink(document)
    #print(counterqs)
    #sentence_length(document)
    #prep=prepositions(sentences, document)
    #print(prep)
    #motions=motion(sentences,document)
    #print(motions)
    print("#################################################################################")
    #print(document)
    
            
    
    

# F:\Uni\14_SoSe_21\Praktikum Text2Scene\Traning\ANC\WhereToJapan\
#F:\Uni\14_SoSe_21\Praktikum Text2Scene\Output

do_this()
#sentenizer als 2. Funktion oderlisten split füer beide arten einfügen
