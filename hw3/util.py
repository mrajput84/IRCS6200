import operator
import collections
import os

def checkDirectories():
    if(not os.path.exists("./cleanCorpus")):
        os.makedirs("./cleanCorpus")
    if(not os.path.exists("./Task2")):
        os.makedirs("./Task2")
    if(not os.path.exists("./Task3")):
        os.makedirs("./Task3")
        
        
def getCorpusDict():
    courpusDict = collections.OrderedDict()
    src_dict = ("./cleanCorpus/")
    for allfiles in os.listdir(src_dict):
        with open(src_dict + allfiles, 'r', encoding='utf8', errors="ignore") as input_file:
            docId = allfiles[0:allfiles.rfind(".")]
            fileContent = input_file.read()
        courpusDict[docId] = fileContent
    return courpusDict

def generateTermDocumentFrequencyCount(dic, fileName):
    with open("./Task3/"+fileName+".txt", "wb") as file_obj:
        stri = '{0:40} {1:40} {2:45}\n'.format("Term", "DocumentFrequency", "DocumentIds")
        file_obj.write(stri.encode(encoding='utf_8', errors='ignore'))
        for term in sorted(dic):
            valDict = dic[term]
            docVals = ""
            count = 0
            for valKey in valDict:
                docVals = docVals + str(valKey) + ", "
                count += 1
            strii = '{0!s:40s} {1!s:40s} {2!s:45s}\n'.format(term, count, docVals)
            file_obj.write(strii.encode(encoding='utf_8', errors='ignore'))
       

def writeIndexesToFile(unigramDict, filenm):
    with open("./Task2/"+filenm+".txt", "wb") as file_obj:
        for term in unigramDict:
            innerDict = unigramDict[term]
            innerDict = sorted(innerDict.items(), key=operator.itemgetter(1))
            innerDict.reverse()
            str1 = str(term) + ' --> '
            file_obj.write(str1.encode(encoding='utf_8', errors='ignore'))
            strii = ''
            for lis in innerDict:
                strii = strii + '(' + str(lis[0]) + ', ' + str(lis[1]) + '), '
            
            file_obj.write(strii.encode(encoding='utf_8', errors='ignore'))
            file_obj.write('\n'.encode(encoding='utf_8', errors='ignore'))