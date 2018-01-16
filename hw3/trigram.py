import timeit
import collections
import util
import operator

def makeTrigramIndex(courpusDict):
    trigramDict = collections.OrderedDict()
    for docId, text in courpusDict.items():
        for term in zip(text.split(" ")[:-1], text.split(" ")[1:], text.split(" ")[2:]):
            if term in trigramDict:
                if docId in trigramDict[term]:
                    trigramDict[term][docId] += 1
                else:
                    trigramDict[term][docId] = 1
            else:
                trigramDict[term] = {docId: 1}
    
    util.writeIndexesToFile(trigramDict,'trigramIndexes')           

    return trigramDict

def generateTrigramTermFreq(trigramDictCount, courpusDict):
    trigramDict = makeTrigramIndex(courpusDict)
    for i in trigramDict:
        trigramDictCount[i] = sum(trigramDict[i].values())
        
    util.generateTermDocumentFrequencyCount(trigramDict, 'trigramTermDocIdFreq')
    
    trigramDictCount = sorted(trigramDictCount.items(), key=operator.itemgetter(1))
    trigramDictCount.reverse()
    with open("./Task3/trigramTermFreq.txt", "wb") as file_obj:
        stri = '{0:40} {1:60}\n'.format("Term", "Term Frequency")
        file_obj.write(stri.encode(encoding='utf_8', errors='ignore'))
        for val in trigramDictCount:
            strii = '{0:40} {1:60}\n'.format("".join(str(val[0])), "".join(str(val[1])))
            file_obj.write(strii.encode(encoding='utf_8', errors='ignore')) 

def main():    
    start_time = timeit.default_timer() 
    
    courpusDict = util.getCorpusDict()
    
    trigramDictCount = collections.OrderedDict()
    generateTrigramTermFreq(trigramDictCount, courpusDict)
    
    print("Time taken in seconds: ",timeit.default_timer() - start_time) 

