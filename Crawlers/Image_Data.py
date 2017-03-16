"""
Description:

Image_data.py store the detailed information about the images
"""

__author__ = "Manav Kedia"

class Image():
    def __init__(self, style):
        self._image_url = None
        self._hashtags = []
        self._items = []
        self._brands = []
        self._user = {}
        self._style = style
        self.json_data = {}

    def print_details(self):
        print (self._style)
        print (self._image_url)
        print (self._hashtags)
        print (self._items)
        print (self._brands)
        print (self._user)

    def build_json(self):
        self.json_data["style"] = self._style
        self.json_data["image_url"] = self._image_url
        self.json_data["hashtags"] = self._hashtags
        self.json_data["items"] = self._items
        self.json_data["brands"] = self._brands
        self.json_data["user"] = self._user

    def get_json(self):
        return self.json_data



