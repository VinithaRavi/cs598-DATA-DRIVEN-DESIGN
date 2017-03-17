"""
Description:

Style_parser.py crawls a URLs for obtaining detailed information about the images
"""

__author__ = "Manav Kedia"

from bs4 import BeautifulSoup
import urllib.request
from Crawlers.Image_Data import Image
import os
import json

url = "http://lookbook.nu/look/8626543-Zara-Blazer-Rayban-Sunnies-Scarf-Shirt-Cropped"

image_path = "../crawling_results/images/"
data_path = "../crawling_results/data/"

def check_dir_exists(dir_path):
    """
    Checks if the directory exists, if not creates it
    :param dir_path: the directory path
    """

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

#TO-DO: Handle exceptions if any of the following are not present
class Style():
    def __init__(self, url, category, count):
        """
        Initializes the variables and creates the soup object
        :param url: The url of the image that is to be crawled
        """
        self._url = url
        self._soup = None
        self._image_data = Image(category)
        self._category = category
        self._count = count

        #Check if path exists
        check_dir_exists(image_path + self._category)
        check_dir_exists(data_path + self._category)

        self.create_soup()
        self.populate_image_data()
        #self._image_data.print_details()
        self._image_data.build_json()
        self.save_data()


    def save_data(self):
        data_filename = data_path + self._category + "/" + str(self._count) + ".json"
        data = self._image_data.get_json()
        with open(data_filename, 'w') as f:
            json.dump(data, f)


    def populate_image_data(self):
        """
        Populate the Image class by crawling the page and filling in relevant information
        :return: None
        """
        self._image_data._hashtags = self.get_hashtags()
        self._image_data._items = self.get_items()
        self._image_data._image_url = self.get_image_url()
        self._image_data._brands = self.get_brands()
        self._image_data._user = self.get_user_details()


    def create_soup(self):
        """
        Create the soup object
        :return: None
        """
        lookshop_file = urllib.request.urlopen(self._url)
        lookshop_html = lookshop_file.read()
        lookshop_file.close()

        self._soup = BeautifulSoup(lookshop_html, 'html.parser')


    def get_hashtags(self):
        """
        Extract the hashtags from the URL
        :return: The list of hashtags
        """
        hashtags = []

        try:
            hashtags =  self._soup.find("p", {"id":"look_descrip"}).text
            hashtags = hashtags.split("#")[1:]
        except:
            print ("Error: No hashtags found for " + self._url)

        return hashtags


    def get_image_url(self):
        """
        Extract the url of the image from the url
        TO-DO could have the case of multiple images in the webpage
        :return: a string of image url
        """
        image_url = ""

        try:
            image_div = self._soup.find("div", {"id":"look_photo_container"}).contents

            for img in image_div:
                if img.name == "a":
                    image_url = "https:" + img.contents[0].attrs["src"][:-2]

            #Download this image locally
            if image_url != None:
                local_filename = image_path  + self._category + "/" + str(self._count) + ".jpg"
                urllib.request.urlretrieve(image_url, local_filename)
        except:
            print ("Error: No image url found for " + self._url)

        return image_url


    def get_items(self):
        """
        Finds the list of items in the URL
        :return: a list of strings containing the items
        """

        items = []

        try:

            items_divs = self._soup.find("div", {"class":"look-items-list"})
            if items_divs == None:
                return items

            item_divs = items_divs.content

            for item_div in items_divs:
                if item_div.name=="div":
                    item = " ".join(item_div.text.split())
                    #This line removes the number in the beginning of the list
                    item = " ".join(item.split(" ")[1:])
                    items.append(item)
        except:
            print ("Error: No items found for " + self._url)

        return items


    def get_user_details(self):
        """
        Get the user and his/her instagram url from the page
        :return: A dictionary of user_name and user_url
        """
        user = {}

        try:
            user_div = self._soup.find("div", {"class":"user-summary"}).contents

            for content in user_div:
                if content.name=="a" and content.attrs["class"][1] == "user-avatar":
                    user["name"] = content.attrs["title"]
                    user["url"] = "https://lookbook.nu" + content.attrs["href"]
                if content.name == "div" and content.attrs["class"][0] == "info":
                    div_contents = content.contents
                    for temp in div_contents:
                        if temp.name == "p":
                            if temp.attrs["class"][0] == "byline":
                                info = " ".join(temp.text.split())
                                user["info"] = info
                            elif temp.attrs["class"][0] == "location":
                                user["location"] = temp.contents[3].contents[0]
        except:
            print("Error: No user found for " + self._url)

        return user


    def get_brands(self):
        """
        Get the list of brands on the url
        :return: A list of strings which are the available brands on the page url
        """

        brands = []

        try:
            brand_divs = self._soup.find_all("div", {"class":"spotlight-user"})

            flag = False
            for brand_div in brand_divs:
                for brand in brand_div.contents:
                    if brand.name=="div":
                        if flag==True:
                            brand_cur = " ".join(brand.text.split())
                            brand_cur = brand_cur.split(" Fanned Fan")
                            brands.append(brand_cur[0])
                            flag=False

                        elif "data-page-track" in brand.attrs and "brand" in brand.attrs["data-page-track"]:
                            flag = True
        except:
            print("Error: No brands found for " + self._url)

        return brands


if __name__=="__main__":
    s = Style(url, "Futuristic", 1)