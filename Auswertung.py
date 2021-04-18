import glob
import os
import spacy

way = input("Dateipfad Input:") #F:\Uni\14_SoSe_21\Praktikum Text2Scene\Traning
#folder = input("Dateipfad Output:")
text=""
result=[]

def open_this(way):
    '''Open files in directory and subdirectory'''
    print(way)
    all_text=""
    for x in os.walk(way):
        for y in glob.glob(os.path.join(x[0], '*.xml')):
            print(y)
            result.append(y)
            file_input = open(y, "r", encoding="utf8")
            all_text+= file_input.read() + " "
            #print(all_text)
    return all_text
                
def doc(t):
    '''Tokenizer'''
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length=5000000
    doc = nlp(t)
    for token in doc:
        print(token.text)
    
    #for token in doc:
    #    print(token.text)

def print_tokens(doc):
    for token in doc:
        print(token.text)

def print_pos(doc)
    for token in doc:
        print(token.pos_

def do_this():
    all_text = open_this(way)
    print("3")
    doc = doc(all_text)
    print("4")



do_this()
#Counter POS Tags
#Counter ISO
#Counter QsLink Types
#how many words in sentence how often? x=length, y:how often 0-???
#which links with which preposition
#top 5 motion verbs and how often

