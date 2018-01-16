import os
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup
import re
import timeit
import collections
import util
import unigram
import bigram
import trigram


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
    cleaner.kill_tags = ['script', 'img', 'semantics', 'math', 'sup', 'noscript', 'table', 'li', 'ul', 'label', 'ol', 'sub']
    cleaner.remove_tags = ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'b', 'span', 'u', 'i', 'body', 'a']
    
    soup = BeautifulSoup(content,"html.parser")
    soup.find('div',class_='mw-jump').decompose()
    soup.find('div',class_='printfooter').decompose()
    soup.find('div',id='siteSub').decompose()
    title = soup.find('title')
    body = soup.find('div', id='bodyContent')
    
    cleanObj = cleaner.clean_html(str(title) + " " +str(body))
    cleanText = BeautifulSoup(cleanObj, 'lxml').get_text()
    cleanText = ' '.join(cleanText.split())
    cleanText = cleanText.replace('html ', '')
    return cleanText

def removePunctuation(cleanText):
    cleanText = ''.join(chrs for chrs in cleanText if chrs not in ',.:""}{][)(\/><=')
    cleanText = re.sub('([.,!-\'$])', r'\1', cleanText)
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
                
def main():    
    start_time = timeit.default_timer() 
    
    util.checkDirectories()
    
    cleanHTMLRawData()
    courpusDict = util.getCorpusDict()
    
    unigramDictCount = collections.OrderedDict()
    unigram.generateUnigramTermFreq(unigramDictCount, courpusDict)
    unigram.generateUnigramStopWordsNltk(unigramDictCount)
    
    bigramDictCount = collections.OrderedDict()
    bigram.generateBigramTermFreq(bigramDictCount, courpusDict)
    
    trigramDictCount = collections.OrderedDict()
    trigram.generateTrigramTermFreq(trigramDictCount, courpusDict)
    
    print("Time taken in seconds: ",timeit.default_timer() - start_time) 

main()

