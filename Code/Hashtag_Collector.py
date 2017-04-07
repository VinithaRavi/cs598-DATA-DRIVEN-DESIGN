"""
Description:

Hashtag_Crawler.py parses the crawling results and builds a list of hastags associated with each image
"""

__author__ = "Vinitha Ravichandran"

import os
import json

from collections import defaultdict

path = "../crawling_results/data"

if __name__ == "__main__":
    hastags=defaultdict(list)
    try:
        for (dirpath, dirnames, files) in os.walk(path):
            ##hastags[dirnames+"_"+files]=[]
            #print(files)
            for file in files:
                id= os.path.basename(dirpath)+"_"+os.path.splitext(file)[0]
                fullpath = os.path.join(dirpath, file)
                with open(fullpath, 'r') as f:
                    json_data=json.load(f)
                    tags=json_data["hashtags"]
                    hastags[id]=tags
    except:
        print("fullpath"+fullpath)
        raise



    with open("hashtags.json",'w') as f:
        json.dump(hastags,f,sort_keys="True")


