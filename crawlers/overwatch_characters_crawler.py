
import os
import requests
import crawler_utils
from lxml import html

URL = "https://playoverwatch.com/en-us/heroes/"
IMAGES_PATH = "../resources/images"

def download_overwatch_characters():
    response = requests.get(URL)
    if not response.ok:
        return None
    tree = html.fromstring(response.content)
    image_urls = tree.xpath('//img[@class="portrait"]/@src')
    character_names = tree.xpath('//span[@class="portrait-title"]/text()')
    characters_images = dict(zip(character_names, image_urls))
    for character_name, character_image_url in characters_images.items():
        print("Downloading image for {0} ({1})".format(character_name, character_image_url))
        image_path = os.path.join(IMAGES_PATH, "{0}.png".format(character_name))
        crawler_utils.download_image(character_image_url, image_path)
