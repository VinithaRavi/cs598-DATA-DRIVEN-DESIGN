
from bs4 import BeautifulSoup
import urllib.request
from IPython.display import HTML

myURLS=[]



#opfile=file()
def addURLs(seedURL,tag,classname,classvalue,attr):
    page=urllib.request.urlopen(seedURL)
    souppage=BeautifulSoup(page)
    mytags = souppage.findAll(tag, {classname: classvalue})
    #print(mytags)
    for tag in mytags:
        #print(tag.attrs[attr])
        myURLS.append((tag.attrs[attr]).split("/")[2])


URLs=["http://lookbook.nu/explore/styles","http://lookbook.nu/explore/trending","http://lookbook.nu/explore/occasions"]

def crawl(URLs):

    for x in URLs:
        addURLs(x,"a","class","square-window","href")



crawl(URLs)
with open("../categories/UpdatedCategories.txt", "w") as myfile:
    for url in myURLS:
        myfile.write(url+"\n")



#r = urllib.request.urlopen('http://lookbook.nu/explore/styles')
'''soup = BeautifulSoup(r)
#print (type(soup))
#print (soup)

mytags = soup.findAll("a", { "class" : "square-window" })
#print(mytags)
myURLS=[]

for tag in mytags:
    myURLS.append(tag.attrs['href'])
print(myURLS)
print(len(myURLS))'''


