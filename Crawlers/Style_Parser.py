"""
Description:

Style_parser.py crawls a list of URLs for obtaining detailed information about the images
"""

__author__ = "Manav Kedia"

from bs4 import BeautifulSoup
import urllib.request
from Crawlers.Image_Data import Image

url = "http://lookbook.nu/look/8626543-Zara-Blazer-Rayban-Sunnies-Scarf-Shirt-Cropped"

#TO-DO: Handle exceptions if any of the following are not present

class Style():
    def __init__(self, url, style):
        """
        Initializes the variables and creates the soup object
        :param url: The url of the image that is to be crawled
        """
        self._url = url
        self._soup = None
        self._image_data = Image(style)

        self.create_soup()
        self.populate_image_data()
        self._image_data.print_details()

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
        hashtags =  self._soup.find("p", {"id":"look_descrip"}).text
        hashtags = hashtags.split("#")

        return hashtags[1:]


    def get_image_url(self):
        """
        Extract the url of the image from the url
        TO-DO could have the case of multiple images in the webpage
        :return: a string of image url
        """
        image_div = self._soup.find("div", {"id":"look_photo_container"}).attrs["style"]
        image_url = image_div.split("background-image:url('")[1].split("');")[0]

        return image_url


    def get_items(self):
        """
        Finds the list of items in the URL
        :return: a list of strings containing the items
        """

        items_divs = self._soup.find("div", {"class":"look-items-list"}).contents
        items = []

        for item_div in items_divs:
            if item_div.name=="div":
                item = " ".join(item_div.text.split())
                #This line removes the number in the beginning of the list
                item = " ".join(item.split(" ")[1:])
                items.append(item)

        return items


    def get_user_details(self):
        """
        Get the user and his/her instagram url from the page
        :return: A dictionary of user_name and user_url
        """
        user_div = self._soup.find("div", {"class":"user-summary"}).contents
        user = {}

        for content in user_div:
            if content.name=="a":
                user["name"] = content.attrs["title"]
                user["url"] = content.attrs["href"]
                break

        return user


    def get_brands(self):
        """
        Get the list of brands on the url
        :return: A list of strings which are the available brands on the page url
        """
        brand_divs = self._soup.find_all("div", {"class":"spotlight-user"})
        brands = []

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



        return brands


if __name__=="__main__":
    s = Style(url, "Futuristic")