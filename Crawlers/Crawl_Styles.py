
from bs4 import BeautifulSoup
import urllib.request



#opfile=file()
def addURLs(style):

   num = 1;  # starting page
   foundEnd = False;

   while not foundEnd and num < 100:         # right now web addresses does not work above 100

        myURLS = []
        page=urllib.request.urlopen('http://lookbook.nu/search?page=' + str(num) + '&amp;q=%11' + style)
        soup=BeautifulSoup(page)
        mytags = soup.find_all("h3", class_="bigger force_wrap")

        if not mytags:              # stops iterating when there is no more results
            foundEnd = True
        #print('mytags: ' + str(not mytags))


        f = open(style + '.txt', 'a')

        #print(mytags)
        for tag in mytags:
           #print(tag.attrs[attr])
           myURLS.append(tag.find('a').attrs['href'])
           f.write('http://lookbook.nu' + tag.find('a').attrs['href'] + '\n')
        print("style: " + style + " page: " + str(num))

        num += 1


lines = []
with open("categories.txt") as file:
    for line in file:
        line = line.strip()  # or someother preprocessing
        addURLs(line)

