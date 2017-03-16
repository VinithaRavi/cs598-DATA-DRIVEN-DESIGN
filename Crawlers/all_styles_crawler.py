"""
Description:

all_styles_crawler.py crawls a list of URLs for obtaining detailed information about the images
"""

__author__ = "Manav Kedia"

from Crawlers.Style_Parser import Style
from os import walk

path = "../results/"

if __name__=="__main__":

    filenames = []
    for(dirpath, dirnames, files) in walk(path):
        filenames.extend(files)

    print (len(filenames))

    total_images = 0

    for file in filenames:
        category = file.split(".txt")[0]
        urls = open(path+file, 'r')
        #print("Number of URLs : ", len(urls))
        count = 0

        for url in urls:
            count += 1
            url = url.strip()
            #print (count, url)
            total_images += 1
            #s = Style(url, category, count)
        print (category, count)
        #exit()

    print (total_images)