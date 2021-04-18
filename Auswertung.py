import glob
import os
import spacy

'''Open files in directory and subdirectory'''
result = []
all_text=""
way = input("Dateipfad:") #F:\Uni\14_SoSe_21\Praktikum Text2Scene\Traning
for x in os.walk(way):
    for y in glob.glob(os.path.join(x[0], '*.xml')):
        result.append(y)
        z = open(y, "r", encoding="utf8")
        all_text+= z.read() + " "
#print(len(result))

'''Tokenizer'''
nlp = spacy.load("en_core_web_sm")
nlp.max_length=5000000
doc = nlp(all_text)
for token in doc:
    print(token.text)
