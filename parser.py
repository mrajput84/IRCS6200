import os
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup
import re
import timeit
import operator
import collections

def cleanMarkups(content):
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.style = True
    cleaner.comments = True
    cleaner.links = True
    cleaner.meta = True
    cleaner.embedded = True
    cleaner.frames = True
    cleaner.forms = True
    cleaner.annoying_tags = True
    cleaner.remove_unknown_tags = True
    cleaner.processing_instructions = True
    cleaner.kill_tags = ['script', 'img', 'semantics', 'math', 'sup', 'noscript', 'table', 'li', 'ul', 'label', 'ol', 'sub', 'a']
    cleaner.remove_tags = ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'b', 'span', 'u', 'i', 'body']
    
    cleanObj = cleaner.clean_html(content)
    cleanText = BeautifulSoup(cleanObj, 'lxml').get_text()
    cleanText = ' '.join(cleanText.split())
    cleanText = cleanText.replace('html ', '')
    return cleanText

def removePunctuation(cleanText):
    cleanText = ''.join(chrs for chrs in cleanText if chrs not in ',.:""}{][)(\/><=')
    p = re.compile(r"(\b[-']\b)|[\W_]")
    cleanText = p.sub(lambda m: (m.group(1) if m.group(1) else " "), cleanText)
    cleanText = ' '.join(cleanText.split())
    return cleanText

def caseFolding(cleanText):
    return cleanText.lower();

def cleanHTMLRawData():
    src_dict = ("./urlDocsBFS/")
    #src_dict = ("./oneFile/")
    parentTitle = ''
    for allfiles in os.listdir(src_dict):
        with open(src_dict + allfiles, 'r', encoding='utf8', errors="ignore") as input_file:
            fileTitle = input_file.readline().rstrip("\n")
            content = input_file.read()
            input_file.readline()
            parentTitle = fileTitle[fileTitle.rfind("/") + 1:]
            cleanText = cleanMarkups(content)
            cleanText = removePunctuation(cleanText)
            cleanText = caseFolding(cleanText)
            # cleanText = cleanText.replace(' ','\n')
            with open("./cleanCorpus/" + parentTitle + ".txt", "wb") as file_obj:
                file_obj.write(cleanText.encode(encoding='utf_8', errors='ignore'))

def makeTrigramIndex(courpusDict):
    trigramDict = {}
    for docId, text in courpusDict.items():
        for term in zip(text.split(" ")[:-1], text.split(" ")[1:], text.split(" ")[2:]):
            if term in trigramDict:
                if docId in trigramDict[term]:
                    trigramDict[term][docId] += 1
                else:
                    trigramDict[term][docId] = 1
            else:
                trigramDict[term] = {docId: 1}
    return trigramDict
    
    
def makeBigramIndex(courpusDict):
    bigramDict = {}
    for docId, text in courpusDict.items():
        for term in zip(text.split(" ")[:-1], text.split(" ")[1:]):
            if term in bigramDict:
                if docId in bigramDict[term]:
                    bigramDict[term][docId] += 1
                else:
                    bigramDict[term][docId] = 1
            else:
                bigramDict[term] = {docId: 1}
    return bigramDict
          
    
def makeUnigramIndex(courpusDict):
    unigramDict = {}
    for docId, text in courpusDict.items():
        for term in text.split():
            if term in unigramDict:
                if docId in unigramDict[term]:
                    unigramDict[term][docId] += 1
                else:
                    unigramDict[term][docId] = 1
            else:
                unigramDict[term] = {docId: 1}
    return unigramDict

    
def getCorpusDict():
    courpusDict = {}
    src_dict = ("./cleanCorpus/")
    for allfiles in os.listdir(src_dict):
        with open(src_dict + allfiles, 'r', encoding='utf8', errors="ignore") as input_file:
            docId = allfiles[0:allfiles.rfind(".")]
            fileContent = input_file.read()
        courpusDict[docId] = fileContent
    return courpusDict


def generateTrigramTermFreq(trigramDictCount, courpusDict):
    trigramDict = makeTrigramIndex(courpusDict)
    for i in trigramDict:
        trigramDictCount[i] = sum(trigramDict[i].values())
    
    trigramDictCount = sorted(trigramDictCount.items(), key=operator.itemgetter(1))
    trigramDictCount.reverse()
    with open("./indexes/trigramTermFreq.txt", "wb") as file_obj:
        stri = '{0:40} {1:60}\n'.format("Term", "Term Frequency")
        file_obj.write(stri.encode(encoding='utf_8', errors='ignore'))
        for val in trigramDictCount:
            strii = '{0:40} {1:60}\n'.format("".join(str(val[0])), "".join(str(val[1])))
            file_obj.write(strii.encode(encoding='utf_8', errors='ignore')) 
            

def generateBigramTermFreq(bigramDictCount, courpusDict):
    bigramDict = makeBigramIndex(courpusDict)
    for i in bigramDict:
        bigramDictCount[i] = sum(bigramDict[i].values())
    
    bigramDictCount = sorted(bigramDictCount.items(), key=operator.itemgetter(1))
    bigramDictCount.reverse()
    with open("./indexes/bigramTermFreq.txt", "wb") as file_obj:
        stri = '{0:40} {1:40}\n'.format("Term", "Term Frequency")
        file_obj.write(stri.encode(encoding='utf_8', errors='ignore'))
        for val in bigramDictCount:
            strii = '{0:40} {1:40}\n'.format("".join(str(val[0])), "".join(str(val[1])))
            file_obj.write(strii.encode(encoding='utf_8', errors='ignore'))        


def generateUnigramTermFreq(unigramDictCount, courpusDict):
    unigramDict = makeUnigramIndex(courpusDict)
    for i in unigramDict:
        unigramDictCount[i] = sum(unigramDict[i].values())
    
    unigramDictCount = sorted(unigramDictCount.items(), key=operator.itemgetter(1))
    unigramDictCount.reverse()
    with open("./indexes/unigramTermFreq.txt", "wb") as file_obj:
        stri = '{0:40} {1:40}\n'.format("Term", "Term Frequency")
        file_obj.write(stri.encode(encoding='utf_8', errors='ignore'))
        for val in unigramDictCount:
            strii = '{0:40} {1:40}\n'.format("".join(str(val[0])), "".join(str(val[1])))
            file_obj.write(strii.encode(encoding='utf_8', errors='ignore'))

def main():    
    start_time = timeit.default_timer() 
    unigramDictCount = collections.OrderedDict()
    bigramDictCount = collections.OrderedDict()
    trigramDictCount = collections.OrderedDict()
    
    #cleanHTMLRawData()
    courpusDict = getCorpusDict()
    
    generateUnigramTermFreq(unigramDictCount, courpusDict)
    generateBigramTermFreq(bigramDictCount, courpusDict)
    generateTrigramTermFreq(trigramDictCount, courpusDict)
        
    print("Time taken in seconds: ",timeit.default_timer() - start_time) 

main()

