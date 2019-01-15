#encoding=utf-8
import os
import jieba
from pathlib import Path

# add in own dictionary of jargon and specific exceptions
jieba.load_userdict("/Users/Thomas/Dropbox/Doctoraat/ideophone_scripts/hanchi/ideoslist.csv")

# project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
#DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
TARGET_DIR = os.path.join(f"{PROJECT_ROOT}/segmented/")
SOURCE_DIR = os.path.join(f"{PROJECT_ROOT}/results/")
#print(SOURCE_DIR)

def segmenter (sourcename):
    with open(f"{SOURCE_DIR}{sourcename}", encoding='utf8') as fp:
        for line in fp:
            #seg = jieba.lcut(line, cut_all=False)
            segspace = jieba.cut(line, cut_all=False)
            seg = " ".join(segspace)
            #print(seg)
            if not os.path.exists(TARGET_DIR):
                os.makedirs(TARGET_DIR)
            with open(f"{TARGET_DIR}{sourcename}", mode = 'a', encoding='utf8') as gp:
                print(seg, file = gp)
    
###### run function


sourcename = []
for root, dirs, files in os.walk(SOURCE_DIR):
    for file in files:
        if file.endswith(".txt"):
            #print(file)
            sourcename.append(file)

#print(sources)


for source in sourcename:
    segmenter(source)





