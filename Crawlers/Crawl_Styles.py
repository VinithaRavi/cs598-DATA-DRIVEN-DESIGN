from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
import os

path = "../categories_url/"


def check_dir_exists(dir_path):
    """
    Checks if the directory exists, if not creates it
    :param dir_path: the directory path
    """

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def addURLs(style):

   num = 1
   myURLS = []

   while True:

        try:
            #Use this to crawl for hashtags
            #page=urllib.request.urlopen('http://lookbook.nu/search?page=' + str(num) + '&amp;q=%11' + style)

            #Use this to crawl for urls in the respective categories
            web_page = 'http://lookbook.nu/explore/' + style + '?page=' + str(num)
            print (web_page)
            page = urllib.request.urlopen(web_page)

        except HTTPError:
            break

        soup=BeautifulSoup(page, 'html.parser')
        mytags = soup.find_all("a", {"class": "look-image-link"})
        #mytags = soup.find_all("h3", class_="bigger force_wrap")

        if not mytags:
            break

        for tag in mytags:
           #myURLS.append(tag.find('a').attrs['href'])
           myURLS.append(tag.attrs['href'])

        print("style: " + style + " page: " + str(num))
        num += 1

   with open(path + style + ".txt", 'w') as f:
       for url in myURLS:
           #f.write('http://lookbook.nu' + url + '\n')
           f.write(url + '\n')


if __name__ == "__main__":

    check_dir_exists(path)

    with open("../categories/categories.txt") as file:
        for line in file:
            line = line.strip()
            addURLs(line)

