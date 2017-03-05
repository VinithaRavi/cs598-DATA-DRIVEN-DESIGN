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

    def print_details(self):
        print (self._style)
        print (self._image_url)
        print (self._hashtags)
        print (self._items)
        print (self._brands)
        print (self._user)
