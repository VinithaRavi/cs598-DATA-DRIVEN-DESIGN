from bs4 import BeautifulSoup
import urllib.request

url = "http://lookbook.nu/look/8626543-Zara-Blazer-Rayban-Sunnies-Scarf-Shirt-Cropped"


class Style():
    """
    Initializes the variables and creates the soup object
    """
    def __init__(self, url):
        self.url = url
        self.soup = self.create_soup()

        self.get_hashtags()
        self.get_image_url()
        self.get_items()
        self.get_user_name()
        self.get_brands()


    """
    Returns soup created using the url
    """
    def create_soup(self):
        lookshop_file = urllib.request.urlopen(self.url)
        lookshop_html = lookshop_file.read()
        lookshop_file.close()

        return BeautifulSoup(lookshop_html, 'html.parser')

    def get_hashtags(self):
        hashtags =  self.soup.find("p", {"id":"look_descrip"}).text
        hashtags = hashtags.split("#")

        self.hashtags = hashtags[1:]


    def get_image_url(self):
        image_div = self.soup.find("div", {"id":"look_photo_container"}).attrs["style"]
        image_url = image_div.split("background-image:url('")[1]
        image_url = image_url.split("');")[0]

        self.image_url = image_url


    def get_items(self):
        items_class = self.soup.find("div", {"class":"look-items-list"}).contents

        self.item_lists = []

        for item in items_class:
            if item.name=="div":
                temp = " ".join(item.text.split())
                temp = " ".join(temp.split(" ")[1:])
                self.item_lists.append(temp)


    def get_user_name(self):
        user_name = self.soup.find("div", {"class":"user-summary"}).contents

        self.user = {}

        for content in user_name:
            if content.name=="a":
                self.user["name"] = content.attrs["title"]
                self.user["url"] = content.attrs["href"]
                break

    def get_brands(self):
        brands = self.soup.find_all("div", {"class":"spotlight-user"})

        for brand in brands:
            for temp in brand.contents:
                if temp.name=="div":
                    print (temp.text)


if __name__=="__main__":
    print ("HER")
    s = Style(url)