import requests
import collections
from bs4 import BeautifulSoup
from time import sleep
from anytree import Node, RenderTree

def crawl(url, optional_keyphrase=""):
    subURLList = []
    subURLList = builtsoup(url, optional_keyphrase)
    return subURLList

def builtsoup(url, optional_keyphrase=""):
    source = requests.get(url)
    soup = BeautifulSoup(source.text,'lxml')
    subURLList = getSubUrls(soup, optional_keyphrase)
    return subURLList

def checkURLAnchorForKeyPhrase(subURlAnchorText, subURl, optional_keyphrase):
    flag = False
    subURlAnchor = subURlAnchorText.split(" ")
    for ss in subURlAnchor:
       ss = ''.join(chr for chr in ss if chr not in '(){}[]')
       if(ss.startswith("rain") or ss.endswith("rain") or ss.startswith("Rain")):
           flag = True
    if(not flag):
        ss = subURl[subURl.rfind("/")+1:]
        if("_" in ss):
            ssl = ss.split("_")
            for ssll in ssl:
                ssll = ''.join(chr for chr in ss if chr not in '(){}[]')
                if(ssll.startswith("rain") or ssll.endswith("rain") or ssll.startswith("Rain")):
                    flag = True
        else:
            ss = ''.join(chr for chr in ss if chr not in '(){}[]')
            if(ss.startswith("rain") or ss.endswith("rain") or ss.startswith("Rain")):
                flag = True
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
                if(checkURLAnchorForKeyPhrase(subURlAnchorText, subURl, optional_keyphrase) and ("https://en.wikipedia.org" + subURl) not in subURLList):  
                    subURLList.append("https://en.wikipedia.org" + subURl)
            else:
                if(("https://en.wikipedia.org" + subURl) not in subURLList):  
                    subURLList.append("https://en.wikipedia.org" + subURl)
    return subURLList

def writeURLDictToFile(urlDict):
    valueList = urlDict.items()
    with open("urllist.txt","w") as file_obj:
        for key, list1 in valueList:
            file_obj.write("Key: ["+key+"]: \n") 
            for urls in list1:
                file_obj.write(urls+",\n")
            
def writeUrlsToFile(visited):
    with open("visitedURLs.txt","w") as file_obj:
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
    
def buildSublist(urlDict, visited):
    subURLList = []
    keySet = urlDict.values()
    for keyList in keySet:
        for keyVal in keyList:
            if keyVal not in visited:
                subURLList.append(keyVal)
    return subURLList
                        
def main(url,optional_keyphrase=""):
    subURLList = []
    urlDict = collections.OrderedDict()
    visited = []
    subURLList.append(url);
    flag = False
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
            visited.append(url_1)
            if(len(visited) == 1000):
                flag = True
                break
            #print("%d"%(len(visited)))
            #sleep(1)
        if flag:
            break
    #writeURLDictToFile(urlDict)
    writeUrlsToFile(visited)
    #buildTree(urlDict, url)
    print("*****done*****")  

main("https://en.wikipedia.org/wiki/Tropical_cyclone")