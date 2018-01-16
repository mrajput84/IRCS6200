import timeit
import collections
import operator
import util
from nltk.corpus import stopwords


def generateUnigramStopWordsNltk(unigramDictCount):
    words = unigramDictCount.keys()
    stop_words = set(stopwords.words('english'))
    with open("./Task3/stopWordsNltk.txt", "wb") as file_obj:
        for word in words:
            if word in stop_words:
                strii = '{0:40} {1:40}\n'.format("".join(str(word)), "".join(str(unigramDictCount[word])))
                file_obj.write(strii.encode(encoding='utf_8', errors='ignore'))

def makeUnigramIndex(courpusDict):
    unigramDict = collections.OrderedDict()
    for docId, text in courpusDict.items():
        for term in text.split():
            if term in unigramDict:
                if docId in unigramDict[term]:
                    unigramDict[term][docId] += 1
                else:
                    unigramDict[term][docId] = 1
            else:
                unigramDict[term] = {docId: 1}
    
    util.writeIndexesToFile(unigramDict,'unigramIndexes')
    
    return unigramDict


def generateUnigramTermFreq(unigramDictCount, courpusDict):
    unigramDict = makeUnigramIndex(courpusDict)
    for i in unigramDict:
        unigramDictCount[i] = sum(unigramDict[i].values())
        
    util.generateTermDocumentFrequencyCount(unigramDict, 'unigramTermDocIdFreq')
    
    unigramDictCount = sorted(unigramDictCount.items(), key=operator.itemgetter(1))
    unigramDictCount.reverse()
    with open("./Task3/unigramTermFreq.txt", "wb") as file_obj:
        stri = '{0:40} {1:40}\n'.format("Term", "Term Frequency")
        file_obj.write(stri.encode(encoding='utf_8', errors='ignore'))
        for val in unigramDictCount:
            strii = '{0:40} {1:40}\n'.format("".join(str(val[0])), "".join(str(val[1])))
            file_obj.write(strii.encode(encoding='utf_8', errors='ignore'))

def main():    
    start_time = timeit.default_timer() 
    
    courpusDict = util.getCorpusDict()
    
    unigramDictCount = collections.OrderedDict()
    generateUnigramTermFreq(unigramDictCount, courpusDict)
    generateUnigramStopWordsNltk(unigramDictCount)
    
    print("Time taken in seconds: ",timeit.default_timer() - start_time) 

