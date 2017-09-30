import requests
import collections
import os
import sys
from bs4 import BeautifulSoup
from time import sleep
from anytree import Node, RenderTree

def checkStringForRain(searchStr):
    searchStr = ''.join(chr for chr in searchStr if chr not in '(){}[]')
    if(searchStr.startswith("rain") or searchStr.endswith("rain") or searchStr.startswith("Rain")):
        return True
    else:
        return False

def checkURLAnchorForKeyPhrase(subURlAnchorText, subURl, optional_keyphrase):
    flag = False
    subURlAnchor = subURlAnchorText.split(" ")
    for ss in subURlAnchor:
       flag = checkStringForRain(ss)
    if(not flag):
        ss = subURl[subURl.rfind("/")+1:]
        if("_" in ss):
            ssl = ss.split("_")
            for ssll in ssl:
                flag = checkStringForRain(ssl)
        else:
            flag = checkStringForRain(ss)
    return flag
    
def getSubUrls(soup, optional_keyphrase=""):
    subURLList = []
    for link in soup.find_all('a', href=True):
        subURl = link['href']
        subURlAnchorText = link.text
        if("Main_Page" not in subURl and ":" not in subURl and subURl.startswith("/wiki/")):
            if("#" in subURl):
                subURl = subURl[0: subURl.index("#")]
            if(optional_keyphrase != "" and len(optional_keyphrase) > 0):
                flag = checkURLAnchorForKeyPhrase(subURlAnchorText, subURl, optional_keyphrase)
            else:
                flag = True
            if(flag and ("https://en.wikipedia.org" + subURl not in subURLList)):
                subURLList.append("https://en.wikipedia.org" + subURl)
                #if(len(subURLList) == 3):
                #    break
    return subURLList

def writeUrlSourceToText(url,soup):
    strFileName = "urlDocumentData/" + url[url.rfind("/")+1:] + ".txt"
    with open(strFileName,"wb") as file_obj:
        file_obj.write((url+"\n").encode('utf-8'))
        for txt in soup:
            file_obj.write(txt.encode('utf-8'))

def buildsoup(url, optional_keyphrase=""):
    source = requests.get(url)
    soup = BeautifulSoup(source.text,'lxml')
    writeUrlSourceToText(url,soup);
    subURLList = getSubUrls(soup, optional_keyphrase)
    return subURLList

def writeURLDictToFile(urlDict):
    valueList = urlDict.items()
    with open("urllist.txt","w") as file_obj:
        for key, list1 in valueList:
            file_obj.write("Key: ["+key+"]: \n") 
            for urls in list1:
                file_obj.write(urls+",\n")
            
def writeUrlsToFile(visited, optional_keyphrase=""):
    if(optional_keyphrase != "" and len(optional_keyphrase) > 0):
        strFileName = "visitedUrl/visitedURLsKeyPhrase.txt"
    else:
        strFileName = "visitedUrl/visitedURLs.txt"
    with open(strFileName,"w") as file_obj:
        for url in visited:
            file_obj.write(url+"\n") 
            
def buildTree(urlDict, url):
    valueList = urlDict.items()
    startNode = Node(url)
    for key, list1 in valueList:
        parentNode = Node(key, parent=startNode)
        for urls in list1:
            childNode = Node(urls, parent=parentNode)
    for pre, fill, node in RenderTree(startNode):
        print("%s%s" % (pre, node.name))
        
def crawl(url, optional_keyphrase=""):
    subURLList = []
    subURLList = buildsoup(url, optional_keyphrase)
    return subURLList
    
def buildSublist(urlDict, visited):
    subURLList = []
    keySet = urlDict.values()
    for keyList in keySet:
        for keyVal in keyList:
            if keyVal not in visited:
                subURLList.append(keyVal)
    return subURLList

def checkDirectories():
    if(not os.path.exists("./visitedUrl")):
        os.makedirs("./visitedUrl")
    if(not os.path.exists("./urlDocumentData")):
        os.makedirs("./urlDocumentData")
                        
def main(args):
#def main(url,optional_keyphrase=""):
    #args = ""
    optional_keyphrase = ""
    if(args != ""):
        if(len(args) == 2 or len(args) == 3):
            print("proceed to crawl: ",args)
            url = args[1]
            if(len(args) == 3):
                optional_keyphrase = args[2]
        else:
            print("Error in calling, format: python webCrawler.py \"seedurl\" \"keyword[optional]\"")
            return
    depth = 0;
    flag = False
    visited = set()
    subURLList = []
    urlDict = collections.OrderedDict()
    subURLList.append(url);
    checkDirectories()
    for i in range(1,7):
        if(len(urlDict) > 0):
            subURLList = []
            subURLList = buildSublist(urlDict, visited)
        for url_1 in subURLList:
            subURLList1 = []
            try:
                subURLList1 = crawl(url_1, optional_keyphrase)
            except requests.exceptions.RequestException as conErr:
                print("Error: %s, URL: %s"%(conErr.args[0], url_1))
                sleep(1)
                continue
            subURLList1 = list(set(subURLList1))
            urlDict[url_1] = subURLList1;
            visited.add(url_1)
            if(len(visited) == 1000):
                flag = True
                break
            #print("%d"%(len(visited)))
            sleep(1)
        depth = i;
        if flag:
            break
    writeURLDictToFile(urlDict)
    writeUrlsToFile(visited,optional_keyphrase)
    #buildTree(urlDict, url)
    print("Done, depth reached: ",depth)

#main("https://en.wikipedia.org/wiki/Tropical_cyclone")
if __name__ == "__main__":
    main(sys.argv)