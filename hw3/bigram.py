import timeit
import collections
import util
import operator

def makeBigramIndex(courpusDict):
    bigramDict = collections.OrderedDict()
    for docId, text in courpusDict.items():
        for term in zip(text.split(" ")[:-1], text.split(" ")[1:]):
            if term in bigramDict:
                if docId in bigramDict[term]:
                    bigramDict[term][docId] += 1
                else:
                    bigramDict[term][docId] = 1
            else:
                bigramDict[term] = {docId: 1}
    
    util.writeIndexesToFile(bigramDict,'bigramIndexes')
            
    return bigramDict

def generateBigramTermFreq(bigramDictCount, courpusDict):
    bigramDict = makeBigramIndex(courpusDict)
    for i in bigramDict:
        bigramDictCount[i] = sum(bigramDict[i].values())
    
    util.generateTermDocumentFrequencyCount(bigramDict, 'bigramTermDocIdFreq')
    
    bigramDictCount = sorted(bigramDictCount.items(), key=operator.itemgetter(1))
    bigramDictCount.reverse()
    with open("./Task3/bigramTermFreq.txt", "wb") as file_obj:
        stri = '{0:40} {1:40}\n'.format("Term", "Term Frequency")
        file_obj.write(stri.encode(encoding='utf_8', errors='ignore'))
        for val in bigramDictCount:
            strii = '{0:40} {1:40}\n'.format("".join(str(val[0])), "".join(str(val[1])))
            file_obj.write(strii.encode(encoding='utf_8', errors='ignore'))        


def main():    
    start_time = timeit.default_timer() 
    
    courpusDict = util.getCorpusDict()
    
    bigramDictCount = collections.OrderedDict()
    generateBigramTermFreq(bigramDictCount, courpusDict)
    
    print("Time taken in seconds: ",timeit.default_timer() - start_time) 

